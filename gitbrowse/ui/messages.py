"""
Internationalized messages for GitBrowse.
"""

from typing import Dict, Any, Optional

# Define all messages for each supported language
MESSAGES = {
    "en": {

        "main_menu": """
        Main Menu:

        1. Browse GitHub Repositories
        2. Change Language
        3. Exit
        """,

        "language_menu": """
        Select Language:

        1. English
        2. Portuguese (Português)
        """,

        "choose_language": "Select language:",
        "language_changed": "Language changed successfully!",
        "no_change": "No changes were made to language settings.",
        "choose_option": "Choose an option:",


        # Connection messages
        "no_internet": "No internet connection established. You can view repositories, but not view or download files.",
        "internet_established": "Internet connection established.",
        
        # File operations
        "download_error": "Error downloading",
        "repo_cloned": "Repository {repo_name} cloned successfully.",
        "file_downloaded": "File {file_name} downloaded successfully.",
        "dir_downloaded": "Directory {dir_name} downloaded successfully.",
        
        # User interactions
        "invalid_option": "Invalid option! Please try again.",
        "choose_file": "Choose a file (number) or 'b' to go back:",
        "welcome": "Welcome to GitBrowse! Explore GitHub repositories from your terminal.",
        "download_prompt": "Do you want to download this file? (y/n):",
        "download_dir_prompt": "Do you want to download this directory? (y/n):",
        "invalid_file_number": "Invalid file number! Please try again.",
        "user_found": "User {username} found! Navigate through the options below:",
        "user_not_found": "User not found. Please check the username and try again.",
        "searching_user": "Searching for user {username}...",
        
        # Navigation options
        "page_instructions": """
Select a number to view repository details
Select 'p' for next page
Select 'n' for previous page
Select 'b' to go back to the previous menu""",
        
        # Repository actions
        "repo_options": """
Options for {repo_name}:

1. View files
2. Clone repository
""",
        "directory_options": """
Choose an action for directory {dir_name}:

v - view contents
d - download entire directory
b - back
""",
        # File actions
        "file_options": """
Choose an action for {file_name}:

v - view
d - download
b - back
""",
        
        # General UI
        "press_enter": "Press Enter to continue...",
        "username_prompt": "Enter a GitHub username:",
        "choose_action": "Choose an action:",
        "loading": "Loading...",
        "success": "Success!",
        "error": "Error",
        "warning": "Warning",
        "operation_cancelled": "Operation cancelled.",
        "goodbye": "Thank you for using GitBrowse. Goodbye!",
        
        # Requirements
        "need_internet_for_files": "Internet connection required to view files.",
        "need_internet_for_clone": "Internet connection required to clone repositories.",
        
        # Language settings
        "select_language": "Select language:",
        "language_changed": "Language changed to English."
    },
    "pt": {

        "main_menu": """
Menu Principal:

1. Navegar Repositórios do GitHub
2. Mudar Idioma
3. Sair
""",

"language_menu": """
Selecione o Idioma:

1. Inglês (English)
2. Português
""",

"choose_language": "Selecione o idioma:",
"language_changed": "Idioma alterado com sucesso!",
"no_change": "Nenhuma alteração foi feita nas configurações de idioma.",
"choose_option": "Escolha uma opção:",


        # Connection messages
        "no_internet": "Conexão com internet não estabelecida. Você pode visualizar repositórios, mas não visualizar nem baixar arquivos.",
        "internet_established": "Conexão com internet estabelecida.",
        
        # File operations
        "download_error": "Erro ao baixar",
        "repo_cloned": "Repositório {repo_name} clonado com sucesso.",
        "file_downloaded": "Arquivo {file_name} baixado com sucesso.",
        "dir_downloaded": "Diretório {dir_name} baixado com sucesso.",
        
        # User interactions
        "invalid_option": "Opção inválida! Tente novamente.",
        "choose_file": "Escolha um arquivo (número) ou 'b' para voltar:",
        "welcome": "Bem-vindo ao GitBrowse! Explore repositórios do GitHub pelo seu terminal.",
        "download_prompt": "Deseja baixar este arquivo? (s/n):",
        "download_dir_prompt": "Deseja baixar este diretório? (s/n):",
        "invalid_file_number": "Número de arquivo inválido! Tente novamente.",
        "user_found": "Usuário {username} encontrado! Navegue pelas opções abaixo:",
        "user_not_found": "Usuário não encontrado. Verifique o nome de usuário e tente novamente.",
        "searching_user": "Procurando o usuário {username}...",
        
        # Navigation options
        "page_instructions": """
Selecione um número para ver detalhes do repositório
Selecione 'p' para próxima página
Selecione 'n' para página anterior
Selecione 'b' para voltar ao menu anterior""",
        
        # Repository actions
        "repo_options": """
Opções para {repo_name}:

1. Ver arquivos
2. Clonar repositório
""",

"directory_options": """
Escolha uma ação para o diretório {dir_name}:

v - visualizar conteúdo
d - baixar diretório inteiro
b - voltar
""",
        
        # File actions
        "file_options": """
Escolha uma ação para {file_name}:

v - visualizar
d - baixar
b - voltar
""",
        
        # General UI
        "press_enter": "Pressione Enter para continuar...",
        "username_prompt": "Digite um nome de usuário do GitHub:",
        "choose_action": "Escolha uma ação:",
        "loading": "Carregando...",
        "success": "Sucesso!",
        "error": "Erro",
        "warning": "Aviso",
        "operation_cancelled": "Operação cancelada.",
        "goodbye": "Obrigado por usar o GitBrowse. Até logo!",
        
        # Requirements
        "need_internet_for_files": "É necessário conexão com a internet para visualizar arquivos.",
        "need_internet_for_clone": "É necessário conexão com a internet para clonar repositórios.",
        
        # Language settings
        "select_language": "Selecione o idioma:",
        "language_changed": "Idioma alterado para Português."
    }
}

# Language selection prompts (bilingual)
LANGUAGE_MESSAGES = {
    "select_language": "\n[En] Select Language\n[Pt] Selecione o Idioma\n\n1. English\n2. Português\n",
    "invalid": "[En] Invalid option!\n[Pt] Opção inválida!",
    "no_language_or_corrupted": "Language not selected or file corrupted.\nLinguagem não selecionada ou arquivo corrompido."
}


class Messages:
    """Class to handle internationalized messages."""
    
    def __init__(self, language: str = "en"):
        """Initialize with the specified language.
        
        Args:
            language: Language code ("en" or "pt")
        """
        self.language = language if language in MESSAGES else "en"
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get a message by key in the current language.
        
        Args:
            key: Message key
            default: Default value if key is not found
            
        Returns:
            The message in the current language
        """
        return MESSAGES[self.language].get(key, default or key)
    
    def set_language(self, language: str) -> None:
        """Set the current language.
        
        Args:
            language: Language code ("en" or "pt")
        """
        if language in MESSAGES:
            self.language = language
    
    def get_language_message(self, key: str) -> str:
        """Get a language selection message (bilingual).
        
        Args:
            key: Message key
            
        Returns:
            The bilingual message
        """
        return LANGUAGE_MESSAGES.get(key, key)