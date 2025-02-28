<div align="center">
  <h1>GitBrowse</h1>
  <p><strong>GitBrowse</strong> is a powerful command-line tool designed to navigate and interact with GitHub repositories directly from your terminal. Browse, view, download, and clone repositories with simplicity and efficiency.</p>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License"/>
</div>

---

## 🌎 Language | Idioma

- [English](#-features)
- [Português](#-funcionalidades)

---

## ✨ Features

- **Repository Exploration**: Browse repositories and their file structures with an intuitive interface
- **Content Viewing**: View files with syntax highlighting directly in your terminal
- **Smart Downloads**: Download individual files or entire directories while preserving structure
- **Repository Cloning**: Clone repositories with a single command
- **Offline Detection**: Automatically detects internet connectivity and provides appropriate options
- **Multilingual Support**: Full support for English and Portuguese (easily extensible)
- **Beautiful Interface**: Colorful, intuitive terminal user interface with rich formatting
- **Pagination**: Efficiently navigate through long lists of repositories and files
- **Local Caching**: Speeds up repeated operations by caching repository data

## 🎬 Demo Videos

- **Viewing and downloading specific files:**
  [Watch Demo](https://www.youtube.com/watch?v=IiTA-VvYQ_E)

- **Cloning an entire repository:**
  [Watch Demo](https://www.youtube.com/watch?v=2BZZOhzVzQg)

## 📋 Requirements

- **Python**: 3.8 or higher
- **Required libraries**:
  - `requests`: For HTTP requests
  - `beautifulsoup4`: For HTML parsing
  - `colorama`: For terminal text styling
  - `pygments`: For code syntax highlighting
  - `rich`: For enhanced terminal rendering
  - `tqdm`: For progress bars
  - `click`: For command-line interface

## 🚀 Installation

```bash
# Install from PyPI
pip install gitbrowse

# Or install from source
git clone https://github.com/user/gitbrowse.git
cd gitbrowse
pip install -e .
```

## 💻 Usage

### Basic Usage

```bash
# Start the interactive browser
gitbrowse

# Or directly browse a specific user's repositories
gitbrowse browse USERNAME
```

### Examples

```bash
# List repositories for a specific user
gitbrowse list microsoft

# View a specific file from a repository
gitbrowse view microsoft/vscode README.md

# Download a specific file
gitbrowse download microsoft/vscode package.json

# Clone a repository
gitbrowse clone microsoft/vscode
```

## 🧩 Advanced Features

- **Authentication**: Use GitHub tokens for accessing private repositories and increased API limits
- **Custom Themes**: Choose from built-in themes or create your own
- **Configurable Settings**: Customize behavior through configuration files
- **Path Completion**: Tab completion for repository and file paths
- **Favorites**: Save frequently accessed repositories for quick access

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/user/gitbrowse.git
cd gitbrowse

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Project Structure

- `gitbrowse/`: Main package
  - `api/`: GitHub API interaction
  - `ui/`: User interface components
  - `models/`: Data models
  - `services/`: Core functionality
  - `utils/`: Helper utilities

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Make your changes and add tests
4. Ensure all tests pass and code is formatted according to the style guide
5. Submit a pull request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Support

To support continued development and improvements, consider becoming a sponsor:

[![Support on Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://patreon.com/SimpleDioney)

---

## 🌟 Funcionalidades

- **Exploração de Repositórios**: Navegue por repositórios e suas estruturas de arquivos com uma interface intuitiva
- **Visualização de Conteúdo**: Veja arquivos com destaque de sintaxe diretamente no seu terminal
- **Downloads Inteligentes**: Baixe arquivos individuais ou diretórios inteiros preservando a estrutura
- **Clonagem de Repositórios**: Clone repositórios com um único comando
- **Detecção Offline**: Detecta automaticamente a conectividade com a internet e fornece opções apropriadas
- **Suporte Multilíngue**: Suporte completo para inglês e português (facilmente extensível)
- **Interface Bonita**: Interface de usuário de terminal colorida e intuitiva com formatação rica
- **Paginação**: Navegue eficientemente por longas listas de repositórios e arquivos
- **Cache Local**: Acelera operações repetidas com cache de dados de repositório

## 🎬 Vídeos de Demonstração

- **Visualizando e baixando arquivos específicos:**
  [Assista à Demonstração](https://www.youtube.com/watch?v=IiTA-VvYQ_E)

- **Clonando um repositório inteiro:**
  [Assista à Demonstração](https://www.youtube.com/watch?v=2BZZOhzVzQg)

## 📋 Requisitos

- **Python**: 3.8 ou superior
- **Bibliotecas necessárias**:
  - `requests`: Para requisições HTTP
  - `beautifulsoup4`: Para análise de HTML
  - `colorama`: Para estilização de texto no terminal
  - `pygments`: Para destaque de sintaxe de código
  - `rich`: Para renderização aprimorada de terminal
  - `tqdm`: Para barras de progresso
  - `click`: Para interface de linha de comando

## 🚀 Instalação

```bash
# Instale do PyPI
pip install gitbrowse

# Ou instale a partir do código-fonte
git clone https://github.com/user/gitbrowse.git
cd gitbrowse
pip install -e .
```

## 💻 Uso

### Uso Básico

```bash
# Inicie o navegador interativo
gitbrowse

# Ou navegue diretamente nos repositórios de um usuário específico
gitbrowse browse NOME_USUARIO
```

### Exemplos

```bash
# Liste repositórios para um usuário específico
gitbrowse list microsoft

# Visualize um arquivo específico de um repositório
gitbrowse view microsoft/vscode README.md

# Baixe um arquivo específico
gitbrowse download microsoft/vscode package.json

# Clone um repositório
gitbrowse clone microsoft/vscode
```

## 🧩 Recursos Avançados

- **Autenticação**: Use tokens GitHub para acessar repositórios privados e aumentar limites de API
- **Temas Personalizados**: Escolha entre temas integrados ou crie o seu próprio
- **Configurações Personalizáveis**: Personalize o comportamento através de arquivos de configuração
- **Completamento de Caminho**: Preenchimento automático para caminhos de repositório e arquivo
- **Favoritos**: Salve repositórios acessados frequentemente para acesso rápido

## 🛠️ Desenvolvimento

### Configurando o Ambiente de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/user/gitbrowse.git
cd gitbrowse

# Instale as dependências de desenvolvimento
pip install -e ".[dev]"

# Execute testes
pytest
```

### Estrutura do Projeto

- `gitbrowse/`: Pacote principal
  - `api/`: Interação com a API do GitHub
  - `ui/`: Componentes da interface do usuário
  - `models/`: Modelos de dados
  - `services/`: Funcionalidade principal
  - `utils/`: Utilitários auxiliares

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. Faça suas alterações e adicione testes
4. Certifique-se de que todos os testes passam e o código está formatado de acordo com o guia de estilo
5. Envie um pull request

## 📄 Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.

## 🙏 Apoio

Para apoiar o desenvolvimento contínuo e melhorias, considere se tornar um patrocinador:

[![Apoie no Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://patreon.com/SimpleDioney)
