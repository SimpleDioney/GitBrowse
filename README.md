# GitBrowse

## Visão Geral
**GitBrowse** é uma ferramenta de linha de comando para navegar e interagir com repositórios do GitHub. A ferramenta permite aos usuários listar repositórios, visualizar e baixar arquivos, e clonar repositórios diretamente para a máquina local.

## Requisitos
- **Python**: 3.6 ou superior
- **Bibliotecas**: `requests`, `bs4` (BeautifulSoup4), `colorama`, `threading`

## Funcionalidades

### 1. Comandos de Limpeza do Terminal
Ajusta o comando de limpeza do terminal com base no sistema operacional do usuário.

### 2. Download de Arquivos
Permite o download de arquivos do GitHub, criando diretórios necessários automaticamente.

### 3. Obtenção do Ramo Padrão de Repositórios
Recupera o ramo padrão de qualquer repositório GitHub usando a API do GitHub.

### 4. Busca de Arquivos em Repositórios
Recupera arquivos de um repositório específico no GitHub.

### 5. Busca e Listagem de Repositórios
Lista repositórios de um usuário GitHub, com suporte para navegação por páginas.

### 6. Listagem Recursiva de Arquivos de Repositório
Lista todos os arquivos e diretórios dentro de um repositório de forma recursiva.

### 7. Interface de Usuário
Inclui uma interface de linha de comando para navegação e interação com repositórios.

## Como Usar
1. Execute o script no terminal.
2. Siga as instruções na tela para listar repositórios ou interagir com arquivos específicos.

## Desenvolvimento Futuro
- Melhoria contínua da interface do usuário para facilitar a navegação.
- Adição de suporte a autenticação para acesso a repositórios privados.
- Otimização no manuseio de threads para operações simultâneas e mais eficientes.

## Contribuições
Contribuições são bem-vindas! Para contribuir, faça um fork do repositório, crie um branch com sua feature ou correção de bugs e envie um pull request.

## Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
