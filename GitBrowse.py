from multiprocessing import process
from bs4 import BeautifulSoup
from colorama import Fore as F, Back as B, Style as S
from sys import platform

import requests
import subprocess
import threading
import os

RESET = S.RESET_ALL
PREFIX_OUT = RESET + F.LIGHTGREEN_EX + ">> "
PREFIX_IN = RESET + F.GREEN + "<< "

lock = threading.Lock()  # Mutex para sincronização

def get_clear_command():
    if platform.lower() == "linux" or platform.lower() == "darwin":
        return "clear"
    elif platform.lower() == "win32":
        return "cls"
    return ""

def download_file(file_url, file_name):
    try:
        directory = os.path.dirname(file_name) or "./downloads"
        os.makedirs(directory, exist_ok=True)
        response = requests.get(file_url, allow_redirects=True)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"{PREFIX_OUT}Arquivo '{file_name}' baixado com sucesso.")
        else:
            print(f"{PREFIX_OUT}Falha ao baixar o arquivo. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{PREFIX_OUT}Erro ao baixar o arquivo: {e}")

def get_default_branch(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(url)
    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get('default_branch', 'main')
    else:
        print(f"{PREFIX_OUT}Erro ao buscar informações do repositório: Status code {response.status_code}")
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
            repo_list.append({'name': repo_name, 'url': repo_url})
            threading.Thread(target=fetch_repository_files, args=(username, {'name': repo_name, 'url': repo_url}, files_dict)).start()
        page += 1
    return True

def list_files_recursive(repo_url, indent="", default_branch='main'):
    response = requests.get(repo_url)
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
                subdirectory_contents = list_files_recursive(raw_url, indent + "  - ", default_branch)
                files_and_dirs.append((display_name, raw_url, "Directory"))
                files_and_dirs.extend(subdirectory_contents)
            else:
                files_and_dirs.append((display_name, raw_url, "File"))

    return files_and_dirs

def list_repository_files(repo_url, default_branch='main'):
    full_url = f"https://github.com{repo_url}"
    return list_files_recursive(full_url, default_branch=default_branch)

def clone_repository(repo_url, repo_name):
    subprocess.run(["git", "clone", f"https://github.com{repo_url}.git", f"./{repo_name}"])
    print(f"\n{PREFIX_OUT}Repositório '{repo_name}' clonado com sucesso.")

def main():
    clear = lambda: os.system(get_clear_command())
    clear()

    print(f"{F.LIGHTYELLOW_EX}==================== BEM-VINDO AO GitBrowser ====================")
    print(f"{PREFIX_OUT}Para começar, digite o nome do usuário do GitHub:")
    username = input(f"{PREFIX_IN}")

    print(f"{PREFIX_OUT}Procurando o usuário {F.GREEN}{username}{RESET}...")

    repositories = []
    files_dict = {}
    if not fetch_repositories(username, repositories, files_dict):
        print(f"{PREFIX_OUT}{F.RED}Usuário não encontrado.{RESET}")
        return

    print(f"{PREFIX_OUT}Usuário encontrado! Navegue pelas opções abaixo:")
    print(RESET)
    while True:
        print(f"{F.LIGHTYELLOW_EX}------------------------{RESET}")
        print("Opções:\n1. Listar repositórios\n2. Sair")
        print(f"{F.LIGHTYELLOW_EX}------------------------{RESET}")
        option = input("Escolha uma opção: ")

        if option == '1':
            for i, repo in enumerate(repositories, 1):
                print(f"\n{i}. {repo['name']}")
            repo_option = input("\nSelecione um número para ver detalhes ou 'b' para voltar: ")
            if repo_option.isdigit():
                repo_index = int(repo_option) - 1
                repo_name = repositories[repo_index]['name']
                print(f"\nOpções para {repo_name}:\n1. Ver arquivos\n2. Clonar repositório")
                action = input("Escolha uma ação: ")
                if action == '1':
                    if repo_name in files_dict:
                        files = files_dict[repo_name]
                        for i, (display_name, file_url, file_type) in enumerate(files):
                            print(f"{i + 1}. {display_name}")
                        file_option = input("\nEscolha um arquivo para baixar ou 'b' para voltar: ")
                        if file_option.isdigit():
                            file_index = int(file_option) - 1
                            _, file_url, file_type = files[file_index]
                            if file_type == "File":
                                file_name = f"./downloads/{files[file_index][0].split(' (')[0]}"
                                download_file(file_url, file_name)
                    else:
                        print("\nArquivos ainda sendo processados, tente novamente em breve.")
                elif action == '2':
                    repo_url = repositories[repo_index]['url']
                    clone_repository(repo_url, repo_name)
            elif repo_option.lower() == 'b':
                continue
        elif option == '2':
            print("\nEncerrando o programa.")
            break

if __name__ == "__main__":
    main()
