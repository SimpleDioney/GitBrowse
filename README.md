
<div align="center">
    <h1>GitBrowse</h1>
    <p><strong>GitBrowse</strong> é uma ferramenta de linha de comando robusta projetada para navegar e interagir com repositórios do GitHub diretamente do seu terminal. Com GitBrowse, você pode facilmente listar repositórios, visualizar e baixar arquivos, e até mesmo clonar repositórios inteiros com simplicidade e eficiência.</p>
</div>

## Vídeo de Demonstração

- **Visualizando e baixando arquivos especificos e unicos**

<div align="center">
    [![Demonstracao de uso GitBrowse.](https://img.youtube.com/vi/)]([https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=IiTA-VvYQ_E))
</div>

- **Clonando um repositorio completo**

<div align="center">
    [![Demonstracao de uso GitBrowse.](https://img.youtube.com/vi/)]([https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=IiTA-VvYQ_E))
</div>

## Requisitos

- **Python**: Versão 3.6 ou superior.
- **Bibliotecas Python**:
  - `requests`: Para requisições HTTP.
  - `bs4` (BeautifulSoup4): Para parsing de HTML.
  - `colorama`: Para estilização de texto no terminal.
  - `pygments`: Para destacar o código no terminal.
  - `threading`: Para processamento paralelo.

## Funcionalidades

- **Limpeza do Terminal**: Ajusta o comando de limpeza de tela com base no sistema operacional, garantindo uma interface de usuário limpa e clara.
- **Download de Arquivos**: Facilita o download de arquivos do GitHub, gerenciando automaticamente a criação de diretórios, permitindo baixar arquivos individuais de repositórios.
- **Obtenção do Ramo Padrão de Repositórios**: Utiliza a API do GitHub para determinar o ramo padrão de repositórios, garantindo a correta navegação e clonagem de repositórios.
- **Busca de Arquivos em Repositórios**: Permite a recuperação de arquivos dentro de um repositório especificado, facilitando a localização de arquivos específicos.
- **Listagem de Repositórios**: Exibe repositórios de um usuário do GitHub com opções de navegação paginada, incluindo informações sobre estrelas e forks.
- **Listagem Recursiva de Arquivos de Repositório**: Mostra todos os arquivos e diretórios de um repositório de maneira recursiva, permitindo uma visão completa da estrutura do repositório.
- **Visualização de Arquivos**: Permite a visualização de arquivos diretamente no terminal com destaque de sintaxe, utilizando `pygments` para suportar múltiplas linguagens de programação.
- **Interface de Usuário na Linha de Comando**: Oferece uma interface interativa para facilitar a navegação e interação, permitindo a escolha de ações como visualização, download ou clonagem de arquivos e repositórios.
- **Manutenção de Conexão com a Internet**: Verifica constantemente a conexão com a internet e informa ao usuário sobre a disponibilidade de recursos online, permitindo a navegação em repositórios offline quando necessário.

## Como Usar

1. Abra seu terminal.
2. Execute o script principal com Python:
   ```bash
   python gitbrowse.py
   ```
3. Siga as instruções interativas para explorar repositórios ou realizar ações específicas, como listar arquivos ou clonar repositórios.

### Exemplos de Uso

- **Listar Repositórios**:
  Após iniciar o script, digite o nome de usuário do GitHub para listar os repositórios públicos do usuário.
  
- **Visualizar Arquivos**:
  Navegue até o repositório desejado, escolha um arquivo e selecione a opção de visualização para ver o conteúdo do arquivo diretamente no terminal com destaque de sintaxe.

- **Baixar Arquivos**:
  Após selecionar um arquivo, escolha a opção de download para salvar o arquivo localmente no diretório `downloads`.

- **Clonar Repositórios**:
  Escolha a opção de clonagem para copiar todo o repositório para o seu sistema local.

## Desenvolvimento Futuro

- Aprimoramento da interface do usuário para uma navegação mais intuitiva.
- Implementação de autenticação para acessar repositórios privados.
- Melhoria na eficiência do uso de threads para operações mais rápidas e menos bloqueantes.
- Adição de um sistema para temas.
- Deixa-lo mais rapido, o uso de threads nao foi bem otimizado e ele ainda demora um certo tempo para fazer a primeira iteracao (buscar um usuario).

## Contribuições

Contribuições para melhorar GitBrowse são sempre bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie um novo branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Desenvolva e teste suas mudanças.
4. Envie um pull request:
   ```bash
   git push origin minha-feature
   ```

## Apoio

Para apoiar o desenvolvimento contínuo e melhorias, considere tornar-se um patrocinador no Patreon:
[![Apoie no Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://patreon.com/SimpleDioney)

## Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
