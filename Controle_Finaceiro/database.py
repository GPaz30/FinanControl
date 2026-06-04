import sqlite3
from datetime import datetime

DB_NAME = "controle_financeiro.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo      TEXT    NOT NULL,
            descricao TEXT    NOT NULL,
            categoria TEXT    NOT NULL,
            valor     REAL    NOT NULL,
            data      TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def adicionar_movimentacao(tipo, descricao, categoria, valor, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movimentacoes (tipo, descricao, categoria, valor, data) VALUES (?, ?, ?, ?, ?)",
        (tipo, descricao, categoria, valor, data),
    )
    conn.commit()
    conn.close()


def listar_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movimentacoes ORDER BY data DESC, id DESC")
    registros = cursor.fetchall()
    conn.close()
    return registros


def atualizar_movimentacao(id_, tipo, descricao, categoria, valor, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE movimentacoes
           SET tipo=?, descricao=?, categoria=?, valor=?, data=?
           WHERE id=?""",
        (tipo, descricao, categoria, valor, data, id_),
    )
    conn.commit()
    conn.close()


def excluir_movimentacao(id_):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimentacoes WHERE id=?", (id_,))
    conn.commit()
    conn.close()


def calcular_resumo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(valor),0) FROM movimentacoes WHERE tipo='Receita'")
    total_receitas = cursor.fetchone()[0]
    cursor.execute("SELECT COALESCE(SUM(valor),0) FROM movimentacoes WHERE tipo='Despesa'")
    total_despesas = cursor.fetchone()[0]
    conn.close()
    saldo = total_receitas - total_despesas
    return total_receitas, total_despesas, saldo
