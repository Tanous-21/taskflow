
# TaskFlow

Sistema de gerenciamento de tarefas desenvolvido em Python,
com interface visual utilizando Streamlit e armazenamento
de dados em SQLite.

## Funcionalidades

- Cadastro de tarefas
- Edição e exclusão
- Organização por prioridades
- Controle de status
- Datas de vencimento
- Pesquisa e filtros
- Dashboard com indicadores
- Persistência de dados com SQLite

## Tecnologias

- Python
- Streamlit
- SQLite
- SQL
- Pytest
- Git e GitHub

## Estrutura

```text
gerenciador-de-tarefas/
├── app.py
├── database.py
├── tasks.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
└── tests/
    └── test_tasks.py
```

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd gerenciador-de-tarefas
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executar

```bash
streamlit run app.py
```

## Testes

```bash
pytest -v
```

## Banco de dados

O projeto utiliza SQLite. O banco de dados é criado
automaticamente na primeira execução.

## Autor

Eduardo Tanous Belo
