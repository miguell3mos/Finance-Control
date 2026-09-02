import sqlite3

def conectar():
    return sqlite3.connect("finance_control.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        descricao TEXT,
        valor REAL,
        categoria TEXT,
        data TEXT
    )
    """)

    conexao.close()

def salvar_transacao(transacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO transacoes (tipo,descricao,valor,categoria,data)
    VALUES (?, ?, ?, ?, ?)
    """,(
        transacao["Tipo"],
        transacao["Descrição"],
        transacao["Valor"],
        transacao["Categoria"],
        transacao["Data"]
    ))

    conexao.commit()
    conexao.close()


def consultar_transacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM transacoes
    ORDER BY data DESC
    """)
    transacoes = cursor.fetchall()

    conexao.close()
    return transacoes

def calcular_saldo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT tipo, valor FROM transacoes")
    transacoes = cursor.fetchall()

    saldo = 0

    for transacao in transacoes:
        tipo = transacao[0]
        valor = transacao[1]

        if tipo == "despesa":
            saldo -= valor
        elif tipo == "receita":
            saldo += valor
    conexao.close()

    return saldo


def excluir_transacao(id_transacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    DELETE FROM transacoes
    WHERE id = ?
    """, (id_transacao,))

    conexao.commit()

    if cursor.rowcount > 0:
        resultado = True
    else:
        resultado = False

    conexao.close()

    return resultado


def editar_transacao(id_transacao, tipo, descricao, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE transacoes
    SET tipo = ?, descricao = ?, valor = ?
    WHERE id = ?
    """,(tipo, descricao, valor, id_transacao))

    conexao.commit()

    if cursor.rowcount > 0:
        resultado = True
    else:
        resultado = False

    conexao.close()

    return resultado