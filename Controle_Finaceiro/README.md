# 💰 FinanControl — Sistema de Controle Financeiro Pessoal

Aplicação desktop desenvolvida em Python com interface gráfica Tkinter e banco de dados SQLite para controle de receitas e despesas pessoais.

---

## 🚀 Como executar

### Pré-requisitos

- Python 3.8 ou superior instalado
- Tkinter já vem incluído na instalação padrão do Python

### Passos

1. Clone ou baixe o repositório:

   ```bash
   git clone https://github.com/seu-usuario/financontrol.git
   cd financontrol
   ```

2. Execute a aplicação:
   ```bash
   python main.py
   ```

> O banco de dados `controle_financeiro.db` será criado automaticamente na primeira execução.

---

## 🗂️ Estrutura do projeto

```
controle_financeiro/
│
├── main.py                   # Interface gráfica (Tkinter)
├── database.py               # Funções de banco de dados (SQLite)
├── README.md                 # Este arquivo
└── controle_financeiro.db    # Banco gerado automaticamente
```

---

## ✅ Funcionalidades

| Funcionalidade        | Descrição                                        |
| --------------------- | ------------------------------------------------ |
| **Cadastrar**         | Registra uma nova receita ou despesa             |
| **Listar**            | Exibe todas as movimentações em tabela ordenada  |
| **Editar**            | Seleciona um registro e atualiza os dados        |
| **Excluir**           | Remove um registro com confirmação               |
| **Resumo financeiro** | Mostra total de receitas, despesas e saldo final |

---

## 🛠️ Tecnologias utilizadas

- **Python 3** — Linguagem principal
- **Tkinter / ttk** — Interface gráfica desktop
- **SQLite3** — Banco de dados local (sem instalação extra)
- **ttk.Treeview** — Tabela visual dos registros

---

## 📋 Tabela do banco de dados

**`movimentacoes`**

| Campo     | Tipo    | Descrição                      |
| --------- | ------- | ------------------------------ |
| id        | INTEGER | Chave primária (autoincrement) |
| tipo      | TEXT    | "Receita" ou "Despesa"         |
| descricao | TEXT    | Descrição da movimentação      |
| categoria | TEXT    | Categoria (ex: Alimentação)    |
| valor     | REAL    | Valor em reais                 |
| data      | TEXT    | Data no formato DD/MM/AAAA     |

---

## 👤 Autor

Nome do aluno e matrícula:
Israel Almeida de Melo Belém 202302884512
Davi Machado de Sousa Rêgo 202408328176
Gabriel Leandro Paz E Silva 202402344358

Disciplina: Desenvolvimento Rápido de Aplicações em Python
