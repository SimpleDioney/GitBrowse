# GitBrowse

**GitBrowse** é uma ferramenta de linha de comando robusta projetada para navegar e interagir com repositórios do GitHub diretamente do seu terminal. Com GitBrowse, você pode facilmente listar repositórios, visualizar e baixar arquivos, e até mesmo clonar repositórios inteiros com simplicidade e eficiência.

## Requisitos
- **Python**: Versão 3.6 ou superior.
- **Bibliotecas Python**:
  - `requests`: Para requisições HTTP.
  - `bs4` (BeautifulSoup4): Para parsing de HTML.
  - `colorama`: Para estilização de texto no terminal.
  - `threading`: Para processamento paralelo.

## Funcionalidades

- **Limpeza do Terminal**: Ajusta o comando de limpeza de tela com base no sistema operacional.
- **Download de Arquivos**: Facilita o download de arquivos do GitHub, gerenciando automaticamente a criação de diretórios.
- **Obtenção do Ramo Padrão de Repositórios**: Utiliza a API do GitHub para determinar o ramo padrão de repositórios.
- **Busca de Arquivos em Repositórios**: Permite a recuperação de arquivos dentro de um repositório especificado.
- **Listagem de Repositórios**: Exibe repositórios de um usuário do GitHub com opções de navegação paginada.
- **Listagem Recursiva de Arquivos de Repositório**: Mostra todos os arquivos e diretórios de um repositório de maneira recursiva.
- **Interface de Usuário na Linha de Comando**: Oferece uma interface interativa para facilitar a navegação e interação.

## Como Usar

1. Abra seu terminal.
2. Execute o script principal com Python.
3. Siga as instruções interativas para explorar repositórios ou realizar ações específicas, como listar arquivos ou clonar repositórios.

## Desenvolvimento Futuro

- Aprimoramento da interface do usuário para uma navegação mais intuitiva.
- Implementação de autenticação para acessar repositórios privados.
- Melhoria na eficiência do uso de threads para operações mais rápidas e menos bloqueantes.

## Contribuições

Contribuições para melhorar GitBrowse são sempre bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie um novo branch para sua feature ou correção.
3. Desenvolva e teste suas mudanças.
4. Envie um pull request.

## Apoio

Para apoiar o desenvolvimento contínuo e melhorias, considere tornar-se um patrocinador no Patreon:

[![Apoie no Patreon](https://patreon.com/SimpleDioney?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink)](https://patreon.com/SimpleDioney)

## Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
