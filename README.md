Aplicação desenvolvida em Python com Tkinter para realizar e armazenar respostas de uma pesquisa de satisfação.
Inclui:

    Formulário completo com validações

    Banco SQLite

    Tema customizado (Azure)

    Aba de gráficos (Matplotlib)

    Estrutura modular organizada

- Tecnologias utilizadas

    Python 3.10+

    Tkinter (interface gráfica)

    Matplotlib (gráficos)

    SQLite (banco de dados)

    Azure Tkinter Theme (arquivo .tcl)

- Instalação

1. Clone o repositório

    git clone https://github.com/seu-usuario/ProjetoPythonRAD.git

2. Acesse a pasta do projeto

    cd ProjetoPythonRAD

3. Instale as dependências

    pip install -r requirements.txt

    (Instala apenas o Matplotlib, já que Tkinter e SQLite fazem parte da própria instalação Python.)

- Como rodar o projeto

    Execute:
    python main.py

- Estrutura do projeto

    ProjetoPythonRAD/
│
├─ main.py                # Inicialização da interface
├─ db.py                  # Banco SQLite (create, insert, fetch)
├─ theme/
│   └─ azure.tcl          # Tema do Tkinter
│
├─ ui/
│   ├─ form.py            # Aba de formulário
│   ├─ charts.py          # Aba de gráficos
│   ├─ theme.py           # Aplicação do tema
│   └─ __init__.py
│
├─ requirements.txt
│
└─ README.md

- Tema Azure (customização)

    O arquivo azure.tcl deve estar na pasta:

    theme/azure.tcl

    O theme.py carrega automaticamente o tema usando caminho relativo.

- Banco de dados

    O SQLite é criado automaticamente quando o projeto roda pela primeira vez.

    Arquivo gerado:

    pesquisa_estacio.db

- Gráficos

    Os gráficos são carregados apenas quando houver 5 ou mais respostas na base.

    Eles exibem:

    Presença

    Satisfação geral

    Idade

    Distribuição por turno

- Licença

    Projeto acadêmico — uso livre para estudo.