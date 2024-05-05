<div align="center">
    <h1>GitBrowse</h1>
    <p text-align="justify"><strong>GitBrowse</strong> é uma ferramenta de linha de comando robusta projetada para navegar e interagir com repositórios do GitHub diretamente do seu terminal. Com GitBrowse, você pode facilmente listar repositórios, visualizar e baixar arquivos, e até mesmo clonar repositórios inteiros com simplicidade e eficiência.</p>
</div>

<h2>Requisitos</h2>
<ul>
    <li><strong>Python</strong>: Versão 3.6 ou superior.</li>
    <li><strong>Bibliotecas Python</strong>:
        <ul text-align="justify">
            <li><code>requests</code>: Para requisições HTTP.</li>
            <li><code>bs4</code> (BeautifulSoup4): Para parsing de HTML.</li>
            <li><code>colorama</code>: Para estilização de texto no terminal.</li>
            <li><code>threading</code>: Para processamento paralelo.</li>
        </ul>
    </li>
</ul>

<h2 text-align="justify">Funcionalidades</h2>
<ul>
    <li><strong>Limpeza do Terminal</strong>: Ajusta o comando de limpeza de tela com base no sistema operacional.</li>
    <li><strong>Download de Arquivos</strong>: Facilita o download de arquivos do GitHub, gerenciando automaticamente a criação de diretórios.</li>
    <li><strong>Obtenção do Ramo Padrão de Repositórios</strong>: Utiliza a API do GitHub para determinar o ramo padrão de repositórios.</li>
    <li><strong>Busca de Arquivos em Repositórios</strong>: Permite a recuperação de arquivos dentro de um repositório especificado.</li>
    <li><strong>Listagem de Repositórios</strong>: Exibe repositórios de um usuário do GitHub com opções de navegação paginada.</li>
    <li><strong>Listagem Recursiva de Arquivos de Repositório</strong>: Mostra todos os arquivos e diretórios de um repositório de maneira recursiva.</li>
    <li><strong>Interface de Usuário na Linha de Comando</strong>: Oferece uma interface interativa para facilitar a navegação e interação.</li>
</ul>

<h2>Como Usar</h2>
<ol text-align="justify">
    <li>Abra seu terminal.</li>
    <li>Execute o script principal com Python.</li>
    <li>Siga as instruções interativas para explorar repositórios ou realizar ações específicas, como listar arquivos ou clonar repositórios.</li>
</ol>

<h2>Desenvolvimento Futuro</h2>
<ul text-align="justify">
    <li>Aprimoramento da interface do usuário para uma navegação mais intuitiva.</li>
    <li>Implementação de autenticação para acessar repositórios privados.</li>
    <li>Melhoria na eficiência do uso de threads para operações mais rápidas e menos bloqueantes.</li>
</ul>

<h2>Contribuições</h2>
<p>Contribuições para melhorar GitBrowse são sempre bem-vindas! Para contribuir:</p>
<ol text-align="justify">
    <li>Faça um fork do repositório.</li>
    <li>Crie um novo branch para sua feature ou correção.</li>
    <li>Desenvolva e teste suas mudanças.</li>
    <li>Envie um pull request.</li>
</ol>

<h2>Apoio</h2>
<p>Para apoiar o desenvolvimento contínuo e melhorias, considere tornar-se um patrocinador no Patreon:</p>
<p><a href="https://patreon.com/SimpleDioney"><img src="https://patreon.com/SimpleDioney?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink" alt="Apoie no Patreon"></a></p>

<h2>Licença</h2>
<p>Distribuído sob a licença MIT. Veja o arquivo <code>LICENSE</code> para mais detalhes.</p>
