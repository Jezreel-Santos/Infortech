# InfoTech - Sistema de Gerenciamento de Manutenções

Projeto desenvolvido como trabalho final da disciplina de Desenvolvimento Web (CSI606) do curso de Sistemas de Informação da Universidade Federal de Ouro Preto (UFOP) - Campus João Monlevade.

## Visão Geral

InfoTech é uma aplicação web desenvolvida em Flask (Python) para auxiliar no gerenciamento do fluxo de recepção e acompanhamento de equipamentos eletrônicos para manutenção. O sistema permite:

* Cadastrar clientes.
* Pesquisar e atualizar dados de clientes.
* Registrar a entrada de equipamentos para manutenção, associando-os a um cliente.
* Acompanhar e atualizar o status de cada serviço de manutenção.
* Pesquisar manutenções por diferentes critérios (ID da Manutenção, ID do Cliente, Status).
* Excluir registros de manutenção.

Esta aplicação foi projetada como parte de um sistema maior, focando no suporte ao setor técnico de uma organização.

## Demonstração

Para uma melhor visualização do funcionamento do sistema, assista ao vídeo de demonstração:

**(Link para o Vídeo de Demonstração)** ➔ [Infortech](https://drive.google.com/file/d/1sTU0SbrDkEGm33tOko8JnueWIgypz6Lh/view?usp=sharing).

## Tecnologias Utilizadas

* **Backend:** Python 3
* **Framework Web:** Flask
* **Banco de Dados:** SQLite 3 (utilizado através do módulo `sqlite3` do Python)
* **Frontend:** HTML5, CSS3, JavaScript

## Pré-requisitos

* **Python:** Versão 3.8 ou superior instalada. Você pode baixar em [python.org](https://www.python.org/).
* **pip:** Gerenciador de pacotes do Python (geralmente vem junto com a instalação do Python).

## Configuração do Ambiente

Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto.

1.  **Clone o Repositório (ou extraia os arquivos):**
    ```bash
    # Se estiver usando Git (opcional)
     git clone git@github.com:Jezreel-Santos/Infortech.git
    # cd Infortech
    ```
    Certifique-se de estar no diretório raiz do projeto (`InfoTech`).

2.  **Navegue até a Pasta do Flask:**
    ```bash
    cd flask
    ```
    *(Todos os comandos seguintes devem ser executados de dentro da pasta `InfoTech/flask`)*

3.  **Crie um Ambiente Virtual:**
    ```bash
    python -m venv venv
    ```

4.  **Ative o Ambiente Virtual:**
    * **Windows (PowerShell/CMD):**
        ```bash
        .\venv\Scripts\activate
        ```
    * **Linux / macOS:**
        ```bash
        source venv/bin/activate
        ```
    *(Você verá `(venv)` no início do prompt do terminal se funcionou)*

5.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(**Nota:** Certifique-se de que o arquivo `requirements.txt` exista na pasta `InfoTech/flask` com o conteúdo abaixo).*

6.  **Inicialize o Banco de Dados (se necessário):**
    Se o arquivo `infotech.db` não existir ou estiver vazio, você pode precisar criar as tabelas. Execute os scripts de criação (certifique-se de que eles criem as tabelas `clientes` e `manutencao` corretamente):
    ```bash
    # Exemplo (ajuste se o nome do script for diferente ou se houver mais scripts)
    python criar_tab_manutencao.py
    # python criar_tab_clientes.py # Se você tiver um script para clientes
    ```

## Executando a Aplicação

1.  **Certifique-se** de que o ambiente virtual (`venv`) está ativado.
2.  **Navegue** (se ainda não estiver) para o diretório `InfoTech/flask` no seu terminal.
3.  **Execute** o arquivo principal do Flask:
    ```bash
    python indexRota.py
    ```
4.  O terminal mostrará algumas informações e um link parecido com `http://127.0.0.1:5000/` ou `http://<seu-ip-local>:5000/`.
5.  **Abra** esse link no seu navegador de preferência para acessar a aplicação.

## Estrutura do Projeto (Simplificada)

InfoTech/
└── flask/
├── static/             # Arquivos estáticos (CSS, JS, Imagens)
│   ├── css/
│   ├── js/
│   └── Imagens/
├── templates/          # Arquivos HTML (Templates Jinja2)
├── venv/               # Ambiente virtual (criado pelo usuário)
├── init.py         # (Pode ser necessário para estrutura de pacotes)
├── indexRota.py        # Arquivo principal da aplicação Flask
├── cadClienteRota.py   # Lógica da rota de cadastro de cliente
├── pesquisarClienteRota.py # Lógica da rota de pesquisa de cliente
├── ...                 # Outros arquivos de rota (.py)
├── criar_tab_manutencao.py # Script para criar tabela
├── infotech.db         # Arquivo do banco de dados SQLite
└── requirements.txt    # Lista de dependências Python

## Agradecimentos

Gostaria de dedicar este trabalho ao Professor Dr. Fernando B. Oliveira (Web - CSI606 - UFOP/JM). Agradeço imensamente pelo encorajamento e apoio durante todo o desenvolvimento, mesmo ciente das dificuldades encontradas em meio à vasta quantidade de conteúdos e tecnologias do desenvolvimento web. Sua orientação foi fundamental para a conclusão deste projeto.

## Autor

* **Jezreel Santos** - *Aluno da disciplina CSI606*


