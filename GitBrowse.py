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
import json

# Importa as mensagens do arquivo messages.py para deixar o codigo mais organizado e limpo. / Import messages from messages.py to keep the code more organized and clean.
from messages import *

lock = threading.Lock()  # Mutex para sincronização / Mutex for synchronization
downloaded_file_message = None  # Mensagem de arquivo baixado / Downloaded file message
internet_connected = True  # Estado inicial da conexão com a Internet / Initial state of Internet connection
config_file = "config.json"  # Nome do arquivo de configuração / Configuration file name
language = "en"  # Idioma padrão / Default language

def load_config():
    """Carrega a configuração do idioma, solicita seleção se não encontrada. / Loads language configuration, prompts selection if not found."""
    global language
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            language = config.get("language")  # Sem valor padrão aqui / No default value here
            if language not in ["en", "pt"]:  # Verifica se o idioma é válido / Check for valid language
                raise ValueError("Invalid language in config file")
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        print(f"{message_languages['no_language_or_corrupted']}")
        select_language()
        save_config()

def save_config():
    """Salva a configuração atual / Save the current configuration."""
    config = {"language": language}
    with open(config_file, 'w') as file:
        json.dump(config, file)

def select_language():
    """Seleciona o idioma / Select the language."""
    global language
    while True:
        
        print(f"{message_languages['select_language']}")
        choice = input(f"{message_languages['choice']}")
        if choice == "1":
            language = "en"
            break
        elif choice == "2":
            language = "pt"
            break
        else:
            print(f"{message_languages['invalida']}")
    save_config()

def get_clear_command():
    """Obtém o comando de limpeza para o sistema operacional / Get the clear command for the operating system."""
    if platform.lower() in ["linux", "darwin"]:
        return "clear"
    elif platform.lower() == "win32":
        return "cls"
    return ""


def clear_screen_with_message():
    """Limpa a tela, mas mantém a mensagem de download e o status da conexão no topo. / Clears the screen, but keeps the download message and connection status at the top."""
    
    if not internet_connected:
        if not downloaded_file_message:
            print(f"{messages[language]['no_internet']}")
        else:
            print(f"{messages[language]['no_internet']}")
    elif downloaded_file_message:
        print(downloaded_file_message)

def check_internet_connection():
    """Verifica a conexão com a Internet / Check the Internet connection."""
    global internet_connected
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        if not internet_connected:
            internet_connected = True
            
            print(f"{messages[language]['internet_established']}")
    except OSError:
        internet_connected = False

def download_file(file_url, file_name):
    """Baixa um arquivo da URL fornecida e salva com o nome fornecido. / Downloads a file from the given URL and saves it with the given name."""
    global downloaded_file_message
    try:
        directory = os.path.dirname(file_name) or "./downloads"  # Diretório para downloads / Directory for downloads
        os.makedirs(directory, exist_ok=True)  # Cria o diretório se não existir / Create directory if not exists

        with requests.get(file_url, stream=True, allow_redirects=True) as r:  # Solicita o arquivo / Request the file
            r.raise_for_status()  # Verifica se a solicitação foi bem-sucedida / Check if the request was successful
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        downloaded_file_message = f"{SUCCESS}{file_name}{messages[language]['success']}{RESET}"
        clear_screen_with_message()
    except requests.exceptions.RequestException as e:
        print(f"{messages[language]['download_error']} '{file_name}': {e}{RESET}")

def download_directory(dir_url, dir_name):
    """Baixa um diretório da URL fornecida e o salva com o nome fornecido."""
    # Garantir barra à direita para identificação correta do diretório
    if not dir_url.endswith("/"):
        dir_url += "/"

    download_base_path = os.path.join("./downloads/diretorios", dir_name)
    os.makedirs(download_base_path, exist_ok=True)

    try:
        for item_display_name, item_url, item_type in list_files_recursive(dir_url):
            item_name = item_display_name.split(" (")[0].strip()

            # Criar o caminho de download correto para diretórios aninhados
            item_path = os.path.join(dir_name, item_name)
            download_path = os.path.join("./downloads/diretorios", item_path)

            if item_type == "File":
                download_file(item_url, download_path)
            elif item_type == "Directory":
                # Passa o item_path completo para a chamada recursiva
                download_directory(item_url, item_path)
        print(f"{messages[language]['directory']}{dir_name}{messages[language]['downloaded_directory']}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{messages[language]['error_directory']} '{dir_name}'{RESET}")
    except Exception as e:  
        print(f"{messages[language]['error_directory']} '{dir_name}'{RESET}")

def list_files_recursive(repo_url, indent="", default_branch='main', retry=3):
    """Lists the files of a repository recursively."""
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
                    files_and_dirs.append((display_name, raw_url, type_info))

                    # Only recurse into subdirectories if necessary
                    if type_info == "Directory":
                        subdirectory_contents = list_files_recursive(raw_url, indent + "  - ", default_branch, retry)
                        files_and_dirs.extend(subdirectory_contents) 

            return files_and_dirs

        except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as e:
            time.sleep(2)  # Wait before retrying
    return [] 


def get_default_branch(username, repo_name):
    """Obtém o branch padrão de um repositório do GitHub / Get the default branch of a GitHub repository."""
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(url)
    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get('default_branch', 'main')
    else:
        return 'main'

def fetch_repository_files(username, repo, files_dict):
    """Busca os arquivos de um repositório e os armazena no dicionário / Fetch repository files and store them in the dictionary."""
    repo_name, repo_url = repo['name'], repo['url']
    default_branch = get_default_branch(username, repo_name)
    files = list_repository_files(repo_url, default_branch)
    with lock:
        files_dict[repo_name] = files

def fetch_repositories(username, repo_list, files_dict):
    """Busca os repositórios de um usuário do GitHub e preenche a lista e o dicionário / Fetch GitHub user's repositories and populate the list and dictionary."""
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


def list_repository_files(repo_url, default_branch='main'):
    """Lista os arquivos de um repositório / List repository files."""
    full_url = f"https://github.com{repo_url}"
    return list_files_recursive(full_url, default_branch=default_branch)

def clone_repository(repo_url, repo_name):
    """Clona um repositório / Clone a repository."""
    subprocess.run(["git", "clone", f"https://github.com{repo_url}.git", f"./repositorios/{repo_name}"])
    
    print(f"{messages[language]['repo_cloned']} '{repo_name}' {messages[language]['success']}.")

def print_centered_header(text, total_width=30):
    """Imprime um cabeçalho centralizado / Print a centered header."""
    text_length = len(text)
    if text_length < total_width:
        padding = (total_width - text_length) // 2
        return '-' * padding + text + '-' * (total_width - text_length - padding)
    else:
        return text

def highlight_code(file_path):
    """Destaca o código de um arquivo / Highlight code from a file."""
    with open(file_path, 'r') as file:
        code = file.read()
    lexer = guess_lexer_for_filename(file_path, code)
    formatter = TerminalFormatter()
    highlighted_code = highlight(code, lexer, formatter)
    os.remove(file_path)  # Remove o arquivo temporário / Remove the temporary file
    
    print(f"\n{highlighted_code}\n")

def get_forks_count(soup):
    """Extrai e limpa a contagem de forks do objeto BeautifulSoup / Extract and clean the forks count from the BeautifulSoup object."""
    forks_element = soup.find('a', {'href': lambda href: href and "/forks" in href})
    if forks_element:
        forks_text = forks_element.text.strip().split()[0].replace(',', '')
        try:
            return int(forks_text)
        except ValueError:
            pass  # Ignora a exceção / Ignore the exception
    return 0  # Retorna 0 se não conseguir obter a contagem / Return 0 if unable to get the count

def fetch_repo_additional_info(repo_url):
    """Busca a contagem de estrelas e forks de um repositório / Fetch stars and forks count for a repository."""
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
    """Trata a ação do arquivo (visualizar ou baixar) com base na escolha do usuário. / Handles file action (view or download) based on user choice."""
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)  # Cria o diretório de downloads se não existir / Create the downloads directory if it doesn't exist
    while True:
        clear_screen_with_message()
        if file_type == "Directory":
            print(f"{messages[language]['folder_options']}")
        else:
            print(f"{messages[language]['view_or_download']}")
        action = input(f"{messages[language]['choose_option']}")

        if action == 'd':
            download_path = os.path.join("downloads", file_name)
            if file_type == "File":
                download_file(file_url, download_path)
            elif file_type == "Directory":
                download_directory(file_url, file_name)
            break
        elif action == 'v' and file_type == "File":
            download_file(file_url, file_name)  # Baixa o arquivo antes de visualizar / Download the file before viewing
            highlight_code(file_name)
            download_after_view = input(f"{messages[language]['download_prompt']}")
            if download_after_view.lower() in ('s', 'y'):
                download_file(file_url, os.path.join(downloads_dir, file_name))
            break
        elif action == 'b':
            break
        else:
            print(f"{messages[language]['invalid_option']}")
        downloaded_file_message = None  # Reseta a mensagem após o loop / Reset the message after the loop

def display_repository_files(username, repo_name, files):
    """Exibe os arquivos do repositório com um menu interativo. / Displays repository files with an interactive menu."""
    
    check_internet_connection()  # Verifica a conexão com a Internet / Check the Internet connection
    print(f"\n{WHITE}{print_centered_header(f'[{username}/{repo_name}]', 50)}{RESET}\n")
    for i, (display_name, file_url, file_type) in enumerate(files):
        print(f"{i + 1}. {display_name}")

    while True:  # Loop para tratar da seleção de arquivos / Loop to handle file selection
        file_option = input(f"{messages[language]['choose_file']}")
        if file_option.isdigit():
            file_index = int(file_option) - 1
            if 0 <= file_index < len(files):
                _, file_url, file_type = files[file_index]
                file_name = files[file_index][0].split(' (')[0]  # Extrai o nome do arquivo / Extract the file name
                handle_file_action(file_name, file_url, file_type)
                break  # Sai do loop após a ação do arquivo / Exit the loop after file action
            else:
                print(f"{messages[language]['invalid_file_number']}")
        elif file_option.lower() == 'b':
            return  # Volta ao menu anterior / Return to the previous menu
        else:
            print(f"{messages[language]['invalid_option']}")

def main():
    """Função principal que executa o programa / Main function that runs the program."""
    clear = lambda: os.system(get_clear_command())
    clear()

    load_config()

    if language not in ["pt", "en"]:
        select_language()

    print(f"{messages[language]['welcome']}")
    username = input(f"{PREFIX_IN}{WHITE}")

    check_internet_connection()  # Verifica a conexão com a Internet / Check the Internet connection
    if not internet_connected:
        clear_screen_with_message()

    print(f"{messages[language]['searching_user']}{username}{HEADER}...{RESET}")

    repositories = []
    files_dict = {}
    if not fetch_repositories(username, repositories, files_dict):  # Busca os repositórios / Fetch the repositories
        print(f"{messages[language]['user_not_found']}")
        return

    
    print(f"{messages[language]['user_prefix']}{username}{messages[language]['user_found']}")

    current_page = 0
    repos_per_page = 10
    total_pages = (len(repositories) + repos_per_page - 1) // repos_per_page
    header_width = max(30, len(username) + 10)

    while True:
        
        
        print(f"{messages[language]['list_or_exit']}")
        option = input(f"{messages[language]['choose_option']}")

        if option == '1':
            while True:
                check_internet_connection()  # Verifica a conexão com a Internet / Check the Internet connection
                clear_screen_with_message()
                start = current_page * repos_per_page
                end = min(start + repos_per_page, len(repositories))
                print(f"\n{WHITE}{print_centered_header(f'[{username}]', header_width)}{RESET}\n")
                for i in range(start, end):
                    repo = repositories[i]
                    print(f"{i + 1}. {HEADER}{repo['name']:<60}{STAR}Stars{WHITE}: {repo['stars']} {WHITE}| {SUCCESS}Forks{WHITE}: {repo['forks']}{RESET}")
                print(f"\n{WHITE}{print_centered_header(f'[Page {current_page + 1}/{total_pages}]', header_width)}{RESET}\n")
                
                print(f"{messages[language]['page_details']}")
                repo_option = input(f"{messages[language]['choose_option']}")

                if repo_option.isdigit():
                    repo_index = int(repo_option) - 1 + start
                    repo_name = repositories[repo_index]['name']
                    
                    check_internet_connection()  # Verifica a conexão com a Internet / Check the Internet connection
                    clear_screen_with_message()
                    
                    print(f"{messages[language]['options_for']} {repo_name}{messages[language]['view_or_clone']}")
                    action = input(f"{messages[language]['choose_option']}")
                    if action == '1':
                        
                        check_internet_connection()  # Verifica a conexão com a Internet / Check the Internet connection
                        clear_screen_with_message()
                        if repo_name in files_dict:
                            files = files_dict[repo_name]
                            display_repository_files(username, repo_name, files)
                        else:
                            print(f"{messages[language]['processing']}")
                    elif action == '2':
                        
                        check_internet_connection()  # Verifica a conexão com a Internet / Check the Internet connection
                        clear_screen_with_message()
                        if internet_connected:
                            repo_url = repositories[repo_index]['url']
                            clone_repository(repo_url, repo_name)
                        else:
                            print(f"{messages[language]['cannot_clone_no_internet']}")
                elif repo_option.lower() == 'p' and current_page < total_pages - 1:
                    current_page += 1
                elif repo_option.lower() == 'n' and current_page > 0:
                    current_page -= 1
                elif repo_option.lower() == 'b':
                    break
        elif option == '2':
            select_language()
            
        elif option == '3':
            
            print(f"{messages[language]['exiting']}")
            break

if __name__ == "__main__":
    main()
