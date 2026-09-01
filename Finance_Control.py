import sqlite3
conexao = sqlite3.connect("finance_control.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    valor REAL
)
""")

conexao.close()

def calcular_saldo():
    conexao = sqlite3.connect("finance_control.db")
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

def salvar_transacao(transacao):
    conexao = sqlite3.connect("finance_control.db")
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO transacoes (tipo,descricao,valor)
    VALUES (?, ?, ?)
    """,(
        transacao["Tipo"],
        transacao["Descrição"],
        transacao["Valor"]
    ))

    conexao.commit()
    conexao.close()

def mostrar_saldo(saldo):
    print("="*30)
    print("Ver Saldo")
    print(f"Saldo atual: R$ {saldo:.2f}")

def consultar_transacoes():
    conexao = sqlite3.connect("finance_control.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM transacoes")
    transacoes = cursor.fetchall()

    if not transacoes:
        print("="*30)
        print("Não há transações registradas.")
    else:
        print("="*30)
        print("Consultar Transações")
        for transacao in transacoes:
            print(f"ID: {transacao[0]}, Tipo: {transacao[1]}, Descrição: {transacao[2]}, Valor: {transacao[3]:.2f}")

    conexao.close()

def registrar_transacao():
        print("="*30)
        print("Registrar Transação")
        
        tipo = input("Digite o tipo da transação (Despesa/Receita): ").strip().lower()
        descricao = input("Digite a descrição da transação: ").strip()

        try:
            valor = float(input("Digite o valor da transação: "))
        except ValueError:
            print("="*30)
            print("Valor Inválido! Digite apenas números.")
            return None

        if valor <= 0:
            print("="*30)
            print("O valor da transação deve ser maior que zero.")
            return None
        
        transacao = {
            "Tipo": tipo,
            "Descrição": descricao,
            "Valor": valor
        }
        
        if transacao["Tipo"] == "despesa" or transacao["Tipo"] == "receita":
            return transacao
        else:
            print("="*30)
            print("Tipo de transação inválido! A transação não será registrada.")
            return None

def excluir_transacao(id_transacao):
    conexao = sqlite3.connect("finance_control.db")
    cursor = conexao.cursor()

    cursor.execute("""
    DELETE FROM transacoes
    WHERE id = ?
    """, (id_transacao,))

    conexao.commit()

    if cursor.rowcount > 0:
        print("Transação excluída com sucesso.")
    else:
        print("Nenhuma Transação encontrada com esse ID.")
    conexao.close()

def editar_transacao(id_transacao, tipo, descricao, valor):
    conexao = sqlite3.connect("finance_control.db")
    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE transacoes
    SET tipo = ?, descricao = ?, valor = ?
    WHERE id = ?
    """,(tipo, descricao, valor, id_transacao))

    conexao.commit()

    if cursor.rowcount > 0:
        print("Transação atualizada com sucesso.")
    else:
        print("Nenhuma transação foi encontrada com esse ID.")

    conexao.close()

while True:
    print("="*30)
    print("      Finance Control")
    print("="*30)
    print("Bem-vindo ao Finance Control!")
    print("="*30)
    print(
        """    1- Registrar Transação
    2- Consultar Transações
    3- Ver Saldo
    4- Excluir Transação
    5- Editar Transação
    6- Sair"""
    )
    print("="*30)
    try:
        resp = int(input("Digite o número da opção desejada: "))
    except ValueError:
        print("="*30)
        print("Digite apenas números!")
        continue

    if resp == 1:
        transacao = registrar_transacao()
        if transacao is not None:
            salvar_transacao(transacao)
    elif resp == 2:
        consultar_transacoes()
    elif resp == 3:
        saldo = calcular_saldo()
        mostrar_saldo(saldo)
    elif resp == 4:
        print("="*30)
        try:
            id_transacao = int(input("Digite o ID da transação que deseja escluir: "))
        except ValueError:
            print("Digite um ID valido!")
            continue

        excluir_transacao(id_transacao)
    elif resp == 5:
        try:
            id_transacao = int(input("Digite o ID da transação que deseja editar: "))
        except ValueError:
            print("ID inválido.")
            continue
        tipo = input("Digite o novo tipo (Despesa/Receita): ").strip().lower()
        descricao = input("Digite a nova descrição: ").strip()
        try:
            valor = float(input("Digite o novo valor: "))
        except ValueError:
            print("Valor inválido.")
            continue
        if valor > 0 and (tipo == "despesa" or tipo == "receita"):
            editar_transacao(id_transacao, tipo, descricao, valor)
        else:
            print("Valor ou Tipo está inválido.")
    elif resp == 6:
        print("="*30)
        print("Saindo do programa...")
        break
    else: 
        print("="*30)
        print("Opção inválida! Tente novamente.")
print("="*30)
