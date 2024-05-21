from multiprocessing import process
from bs4 import BeautifulSoup
from colorama import Fore as F, Back as B, Style as S
from sys import platform

import requests
import subprocess
import threading
import socket
import os
import pygments
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import TerminalFormatter
import time

RESET = S.RESET_ALL
PREFIX_OUT = RESET + F.LIGHTMAGENTA_EX + ">> "
PREFIX_IN = RESET + F.MAGENTA + "<< "
ERROR = F.RED
SUCCESS = F.GREEN
INFO = F.CYAN
WHITE = F.WHITE
HEADER = F.LIGHTMAGENTA_EX
FOOTER = F.MAGENTA

lock = threading.Lock()  # Mutex para sincronização
downloaded_file_message = None
internet_connected = True  # Estado inicial da conexão com a Internet

def get_clear_command():
    if platform.lower() == "linux" or platform.lower() == "darwin":
        return "clear"
    elif platform.lower() == "win32":
        return "cls"
    return ""

def clear_screen():
    """ Clear the console screen. """
    os.system(get_clear_command())

def clear_screen_with_message():
    """Clears the screen, but keeps the download message and connection status at the top."""
    clear_screen()
    if not internet_connected:
        if not downloaded_file_message:
            print(f"{ERROR}Conexao com internet nao estabelecida. Voce pode visualizar repositorios, mas nao visualizar nem baixar arquivos.{RESET}")
        else:
            print(f"{ERROR}Conexao com internet nao estabelecida. Voce pode visualizar repositorios, mas nao visualizar nem baixar arquivos.{RESET}")
    elif downloaded_file_message:
        print(downloaded_file_message)

def check_internet_connection():
    """Verifica a conexão com a Internet."""
    global internet_connected
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        if not internet_connected:
            internet_connected = True
            clear_screen()
            print(f"{SUCCESS}Conexao estabelecida.{RESET}")
    except OSError:
        internet_connected = False

def download_file(file_url, file_name):
    """Downloads a file from the given URL and saves it with the given name."""
    global downloaded_file_message
    try:
        directory = os.path.dirname(file_name) or "./downloads"  

        with requests.get(file_url, stream=True, allow_redirects=True) as r:  
            r.raise_for_status()  
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        downloaded_file_message = f"{SUCCESS}Arquivo '{file_name}' carregado!{RESET}"
        clear_screen_with_message()
    except requests.exceptions.RequestException as e:
        print(f"{ERROR}Erro ao baixar '{file_name}': {e}{RESET}")

def get_default_branch(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(url)
    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get('default_branch', 'main')
    else:
        return 'main'

def fetch_repository_files(username, repo, files_dict):
    repo_name, repo_url = repo['name'], repo['url']
    default_branch = get_default_branch(username, repo_name)
    files = list_repository_files(repo_url, default_branch)
    with lock:
        files_dict[repo_name] = files

def fetch_repositories(username, repo_list, files_dict):
    page = 1
    while True:
        url = f"https://github.com/{username}?page={page}&tab=repositories"
        response = requests.get(url)
        if response.status_code == 404:
            return False
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        repos = soup.findAll('h3', {'class': 'wb-break-all'})
        if not repos:
            break

        for repo in repos:
            repo_name = repo.a.text.strip()
            repo_url = repo.a['href']
            stars, forks = fetch_repo_additional_info(repo_url)
            repo_list.append({'name': repo_name, 'url': repo_url, 'stars': stars, 'forks': forks})
            threading.Thread(target=fetch_repository_files, args=(username, {'name': repo_name, 'url': repo_url}, files_dict)).start()
        page += 1
    return True

def list_files_recursive(repo_url, indent="", default_branch='main', retry=3):
    for _ in range(retry):
        try:
            response = requests.get(repo_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('tr', class_='react-directory-row')
            files_and_dirs = []

            for item in items:
                icon = item.find('svg')
                type_info = "Directory" if "icon-directory" in icon.get('class', []) else "File"

                link = item.find('a', class_='Link--primary')
                if link:
                    name = link.text.strip()
                    path = link['href']
                    if type_info == "File":
                        parts = path.split('/')
                        raw_url = f"https://raw.githubusercontent.com/{parts[1]}/{parts[2]}/{default_branch}/{'/'.join(parts[5:])}"
                    else:
                        raw_url = f"https://github.com{path}"

                    display_name = f"{indent}{name} ({type_info})"
                    if type_info == "Directory":
                        subdirectory_contents = list_files_recursive(raw_url, indent + "  - ", default_branch, retry)
                        files_and_dirs.append((display_name, raw_url, "Directory"))
                        files_and_dirs.extend(subdirectory_contents)
                    else:
                        files_and_dirs.append((display_name, raw_url, "File"))

            return files_and_dirs
        except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as e:
            time.sleep(2)  # Espera antes de tentar novamente
    return []

def list_repository_files(repo_url, default_branch='main'):
    full_url = f"https://github.com{repo_url}"
    return list_files_recursive(full_url, default_branch=default_branch)

def clone_repository(repo_url, repo_name):
    subprocess.run(["git", "clone", f"https://github.com{repo_url}.git", f"./repositorios/{repo_name}"])
    clear_screen()
    print(f"\n{PREFIX_OUT} Repositório {WHITE}'{repo_name}'{HEADER} clonado com sucesso.{RESET}")

def print_centered_header(text, total_width=30):
    text_length = len(text)
    if text_length < total_width:
        padding = (total_width - text_length) // 2
        return '-' * padding + text + '-' * (total_width - text_length - padding)
    else:
        return text

def highlight_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    lexer = guess_lexer_for_filename(file_path, code)
    formatter = TerminalFormatter()
    highlighted_code = highlight(code, lexer, formatter)
    os.remove(file_path)  # Remover o arquivo após exibição
    clear_screen()
    print(f"\n{highlighted_code}\n")

def get_forks_count(soup):
    """Extract and clean the forks count from the BeautifulSoup object."""
    forks_element = soup.find('a', {'href': lambda href: href and "/forks" in href})
    if forks_element:
        
        forks_text = forks_element.text.strip().split()[0].replace(',', '')
        try:
            return int(forks_text)
        except ValueError:
            pass  
    return 0  

def fetch_repo_additional_info(repo_url):
    """Fetch stars and forks count for a repository."""
    url = f"https://github.com{repo_url}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stars = int(soup.find('a', {'href': f'{repo_url}/stargazers'}).text.strip().split()[0].replace(',', ''))
        forks = get_forks_count(soup)
        return stars, forks
    else:
        return 0, 0
    
def handle_file_action(file_name, file_url, file_type):
    """Handles file action (view or download) based on user choice."""
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)  
    while True:
        clear_screen_with_message()
        action = input("Escolha uma ação (v - visualizar, d - baixar, b - voltar): ")
        if action == 'd':
            download_path = os.path.join(downloads_dir, file_name)
            download_file(file_url, download_path)
            break
        elif action == 'v' and file_type == "File":
            download_file(file_url, file_name) 
            highlight_code(file_name)
            download_after_view = input(f"{PREFIX_OUT}{WHITE}Deseja baixar o arquivo? (s/n): {RESET}")
            if download_after_view.lower() == 's':
                download_file(file_url, os.path.join(downloads_dir, file_name))
            break
        elif action == 'b':
            break
        else:
            print("Opção inválida!")
        downloaded_file_message = None 

def display_repository_files(username, repo_name, files):
    """Displays repository files with interactive menu."""
    clear_screen()
    check_internet_connection()
    print(f"\n{WHITE}{print_centered_header(f'[{username}/{repo_name}]', 50)}{RESET}\n")
    for i, (display_name, file_url, file_type) in enumerate(files):
        print(f"{i + 1}. {display_name}")

    while True:  
        file_option = input(f"{PREFIX_OUT}\nEscolha um arquivo (número) ou 'b' para voltar: {WHITE} {RESET}")
        if file_option.isdigit():
            file_index = int(file_option) - 1
            if 0 <= file_index < len(files):
                _, file_url, file_type = files[file_index]
                file_name = files[file_index][0].split(' (')[0]  
                handle_file_action(file_name, file_url, file_type)
                break  # Exit loop after handling file action
            else:
                print(f"{ERROR}Número de arquivo inválido!{RESET}")
        elif file_option.lower() == 'b':
            return  
        else:
            print(f"{ERROR}Opção inválida!{RESET}")

def main():

    clear = lambda: os.system(get_clear_command())
    clear()

    print(f"{HEADER}==================== BEM-VINDO AO GitBrowse ===================={RESET}")
    print(f"{PREFIX_OUT} Para começar, digite o nome do usuário do GitHub:")
    username = input(f"{PREFIX_IN}{WHITE}")

    check_internet_connection()  
    if not internet_connected:
        clear_screen_with_message()

    print(f"{PREFIX_OUT} Procurando o usuário {WHITE}{username}{HEADER}...{RESET}")

    repositories = []
    files_dict = {}
    if not fetch_repositories(username, repositories, files_dict):  
        print(f"{PREFIX_OUT} {F.RED}Usuário não encontrado.{RESET}")
        return

    clear_screen()
    print(f"{PREFIX_OUT} Usuário {WHITE}{username}{HEADER} encontrado! Navegue pelas opções abaixo:{RESET}")

    current_page = 0
    repos_per_page = 10
    total_pages = (len(repositories) + repos_per_page - 1) // repos_per_page
    header_width = max(30, len(username) + 10)

    while True:
        
        print(f"\n{WHITE}------------------------{RESET}\n")
        print(f"{WHITE}Opções:\n\n{WHITE}1.{HEADER} Listar repositórios\n\n{WHITE}2.{HEADER} Sair{RESET}")
        print(f"\n{WHITE}------------------------{RESET}\n")
        option = input(f"{PREFIX_OUT} {WHITE}Escolha uma opção:{WHITE} {RESET}")

        if option == '1':
            while True:
                clear_screen()
                check_internet_connection()  # Verifica a conexão a cada iteração
                clear_screen_with_message()
                start = current_page * repos_per_page
                end = min(start + repos_per_page, len(repositories))
                print(f"\n{WHITE}{print_centered_header(f'[{username}]', header_width)}{RESET}\n")
                for i in range(start, end):
                    repo = repositories[i]
                    print(f"{i + 1}. {HEADER}{repo['name']:<60}{WHITE}Estrelas: {repo['stars']} | Forks: {repo['forks']}{RESET}")
                print(f"\n{WHITE}{print_centered_header(f'[Página {current_page + 1}/{total_pages}]', header_width)}{RESET}\n")
                print(f"{WHITE}Selecione um {HEADER}número {WHITE}para ver detalhes\nSelecione {HEADER}'p' {WHITE}para próxima página\nSelecione {HEADER}'n' {WHITE}para página anterior\nSelecione {HEADER}'b' {WHITE}para voltar ao menu anterior{WHITE}{RESET}")
                repo_option = input(f"{PREFIX_OUT} {WHITE}Escolha uma ação: {WHITE}{RESET} ")

                if repo_option.isdigit():
                    
                    repo_index = int(repo_option) - 1 + start
                    repo_name = repositories[repo_index]['name']
                    clear_screen()
                    check_internet_connection()  # Verifica a conexão ao selecionar o repositório
                    clear_screen_with_message()
                    
                    print(f"\n{WHITE}------------------------{RESET}\n")
                    print(f"\nOpções para {repo_name}:\n\n{WHITE}1.{HEADER} Ver arquivos\n\n{WHITE}2.{HEADER} Clonar repositório{RESET}")
                    print(f"\n{WHITE}------------------------{RESET}\n")
                    action = input(f"{PREFIX_OUT} {WHITE}Escolha uma ação: {WHITE}{RESET} ")
                    if action == '1':
                        clear_screen()
                        check_internet_connection()  # Verifica a conexão antes de exibir arquivos
                        clear_screen_with_message()
                        if repo_name in files_dict:
                            files = files_dict[repo_name]
                            display_repository_files(username, repo_name, files)
                        else:
                            print(f"\n{ERROR}Arquivos ainda sendo processados, tente novamente em breve.{RESET}\n")
                    elif action == '2':
                        clear_screen()
                        check_internet_connection()  # Verifica a conexão antes de clonar o repositório
                        clear_screen_with_message()
                        if internet_connected:
                            repo_url = repositories[repo_index]['url']
                            clone_repository(repo_url, repo_name)
                        else:
                            print(f"{ERROR}Não é possível clonar sem conexão com a internet.{RESET}")
                elif repo_option.lower() == 'p' and current_page < total_pages - 1:
                    current_page += 1
                elif repo_option.lower() == 'n' and current_page > 0:
                    current_page -= 1
                elif repo_option.lower() == 'b':
                    break
        elif option == '2':
            clear_screen()
            print(f"\n{ERROR}Programa encerrado.{RESET}\n")
            break

if __name__ == "__main__":
    main()
