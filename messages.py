from colorama import Fore as F, Style as S

RESET = S.RESET_ALL
PREFIX_OUT = RESET + F.LIGHTMAGENTA_EX + ">> "
PREFIX_IN = RESET + F.MAGENTA + "<< "
ERROR = F.RED
SUCCESS = F.GREEN
INFO = F.CYAN
WHITE = F.WHITE
HEADER = F.LIGHTMAGENTA_EX
FOOTER = F.MAGENTA

message_languages = {
    "no_language_or_corrupted": f"{ERROR}Language not selected or file corrupted.\nLinguagem nao selecionada ou arquivo corrompido.{RESET}",
    "select_language": f"\n{WHITE}------------------------{RESET}\n[En] Select Language\n[Pt] Selecione o Idioma\n\n{WHITE}1.{HEADER} English\n{WHITE}2.{HEADER} Português{RESET}\n{WHITE}------------------------{RESET}\n",
    "choice": f"{PREFIX_IN}{WHITE}{RESET}",
    "invalid": f"{ERROR}[En] Invalid option!\n[Pt] Opção inválida!{RESET}"
}

messages = {
    "pt": {
        "no_internet": f"{ERROR}Conexao com internet nao estabelecida. Voce pode visualizar repositorios, mas nao visualizar nem baixar arquivos.{RESET}",
        "internet_established": f"{SUCCESS}Conexao estabelecida.{RESET}",
        "download_error": f"{ERROR}Erro ao baixar",
        "repo_cloned": f"\n{PREFIX_OUT} Repositório {WHITE}",
        "success": f"{HEADER}clonado com sucesso.{RESET}",
        "invalid_option": f"{ERROR}Opção inválida!{RESET}",
        "choose_file": f"{PREFIX_OUT}\nEscolha um arquivo (número) ou 'b' para voltar: {WHITE} {RESET}",
        "welcome": f"{HEADER}==================== BEM-VINDO AO GitBrowse ===================={RESET}\n{PREFIX_OUT} Para começar, digite o nome do usuário do GitHub:",
        "download_prompt": f"{PREFIX_OUT}{WHITE}Deseja baixar o arquivo? (s/n): {RESET}",
        "invalid_file_number": f"{ERROR}Número de arquivo inválido!{RESET}",
        "user_prefix": f"{PREFIX_OUT} Usuário {WHITE}",
        "user_found": f"{HEADER} encontrado! Navegue pelas opções abaixo:{RESET}",
        "user_not_found": f"{PREFIX_OUT} {F.RED}Usuário não encontrado.{RESET}",
        "searching_user": f"{PREFIX_OUT} Procurando o usuário {WHITE}",
        "list_or_exit": f"\n{WHITE}------------------------{RESET}\n{WHITE}Opções:\n\n{WHITE}1.{HEADER} Listar repositórios\n\n{WHITE}2.{HEADER} Mudar idioma\n\n{WHITE}3.{HEADER} Sair{RESET}\n{WHITE}------------------------{RESET}\n",
        "choose_option": f"{PREFIX_OUT} {WHITE}Escolha uma opção:{WHITE} {RESET}",
        "page_details": f"{WHITE}Selecione um {HEADER}número {WHITE}para ver detalhes\nSelecione {HEADER}'p' {WHITE}para próxima página\nSelecione {HEADER}'n' {WHITE}para página anterior\nSelecione {HEADER}'b' {WHITE}para voltar ao menu anterior{WHITE}{RESET}",
        "options_for": f"\n{WHITE}------------------------{RESET}\n\nOpções para",
        "view_or_clone": f":\n\n{WHITE}1.{HEADER} Ver arquivos\n\n{WHITE}2.{HEADER} Clonar repositório{RESET}\n{WHITE}------------------------{RESET}\n",
        "processing": f"\n{ERROR}Arquivos ainda sendo processados, tente novamente em breve.{RESET}\n",
        "cannot_clone_no_internet": f"{ERROR}Não é possível clonar sem conexão com a internet.{RESET}",
        "exiting": f"\n{ERROR}Programa encerrado.{RESET}\n",
        "view_or_download": f"{HEADER}Escolha uma ação:\n\n{WHITE}v{HEADER} - visualizar\n{WHITE}d{HEADER} - baixar\n{WHITE}b{HEADER} - voltar{WHITE}\n\n{PREFIX_IN}{RESET}"
    },
    "en": {
        "no_internet": f"{ERROR}No internet connection established. You can view repositories, but not view or download files.{RESET}",
        "internet_established": f"{SUCCESS}Connection established.{RESET}",
        "download_error": f"{ERROR}Error downloading",
        "repo_cloned": f"\n{PREFIX_OUT} Repository {WHITE}",
        "success": f"{HEADER}successfully cloned.{RESET}",
        "invalid_option": f"{ERROR}Invalid option!{RESET}",
        "choose_file": f"{PREFIX_OUT}\nChoose a file (number) or 'b' to go back: {WHITE} {RESET}",
        "welcome": f"{HEADER}==================== WELCOME TO GitBrowse ===================={RESET}\n{PREFIX_OUT} To start, enter the GitHub username:",
        "download_prompt": f"{PREFIX_OUT}{WHITE}Do you want to download the file? (y/n): {RESET}",
        "invalid_file_number": f"{ERROR}Invalid file number!{RESET}",
        "user_prefix": f"{PREFIX_OUT} User {WHITE}",
        "user_found": f"{HEADER} found! Browse the options below:{RESET}",
        "user_not_found": f"{PREFIX_OUT} {F.RED}User not found.{RESET}",
        "searching_user": f"{PREFIX_OUT} Searching for user {WHITE}",
        "list_or_exit": f"\n{WHITE}------------------------{RESET}\n{WHITE}Options:\n\n{WHITE}1.{HEADER} List repositories\n\n{WHITE}2.{HEADER} Change language\n\n{WHITE}3.{HEADER} Exit{RESET}\n{WHITE}------------------------{RESET}\n",
        "choose_option": f"{PREFIX_OUT} {WHITE}Choose an option:{WHITE} {RESET}",
        "page_details": f"{WHITE}Select a {HEADER}number {WHITE}to view details\nSelect {HEADER}'p' {WHITE}for next page\nSelect {HEADER}'n' {WHITE}for previous page\nSelect {HEADER}'b' {WHITE}to go back to the previous menu{WHITE}{RESET}",
        "options_for": f"\n{WHITE}------------------------{RESET}\n\nOptions for",
        "view_or_clone": f":\n\n{WHITE}1.{HEADER} View files\n\n{WHITE}2.{HEADER} Clone repository{RESET}\n{WHITE}------------------------{RESET}\n",
        "processing": f"\n{ERROR}Files are still being processed, please try again later.{RESET}\n",
        "cannot_clone_no_internet": f"{ERROR}Cannot clone without an internet connection.{RESET}",
        "exiting": f"{ERROR}Program exited.{RESET}",
        "view_or_download": f"{HEADER}Choose an action:\n\n{WHITE}v{HEADER} - view\n{WHITE}d{HEADER} - download\n{WHITE}b{HEADER} - back{WHITE}\n\n{PREFIX_IN}{RESET}"
    }
}
