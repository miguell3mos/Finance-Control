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


def editar_transacao(id_transacao, tipo, descricao, valor, categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE transacoes
    SET tipo = ?, descricao = ?, valor = ?, categoria = ?
    WHERE id = ?
    """,(tipo, descricao, valor, categoria,  id_transacao))

    conexao.commit()

    resultado = cursor.rowcount > 0

    conexao.close()

    return resultado

def buscar_por_categorias(categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM transacoes
    WHERE categoria = ?
    ORDER BY data DESC
    """,(categoria,))

    transacoes = cursor.fetchall()

    conexao.close()
    return transacoes



def resumo_por_categoria():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT categoria, SUM(valor)
    FROM transacoes
    WHERE tipo = 'despesa'
    GROUP BY categoria
    ORDER BY SUM(valor) DESC
    """)
    resumo = cursor.fetchall()
    conexao.close()
    return resumo

def resumo_mensal(ano,mes):
    conexao = conectar()
    cursor = conexao.cursor()

    periodo = f"{ano}-{mes:02d}%"

    cursor.execute("""
    SELECT tipo, SUM(valor)
    FROM transacoes
    WHERE data LIKE ?
    GROUP BY tipo
    """, (periodo,))

    resumo = cursor.fetchall()

    conexao.close()
    return resumo

def buscar_por_periodo(data_inicio,data_fim):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM transacoes
    WHERE data BETWEEN ? AND ?
    ORDER BY data DESC
    """, (data_inicio,data_fim))

    transacoes = cursor.fetchall()
    conexao.close
    return transacoes