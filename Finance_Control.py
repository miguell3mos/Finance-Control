transacoes = []

saldo = 0

def mostrar_saldo():
    print("="*30)
    print("Ver Saldo")
    print(f"Saldo atual: R$ {saldo:.2f}")

def consultar_transacoes():
    if not transacoes:
        print("="*30)
        print("Não há transações registradas.")
    else:
        print("="*30)
        print("Consultar Transações")
        for transacao in transacoes:
            print(f"Tipo: {transacao['Tipo']}, Descrição: {transacao['Descrição']}, Valor: {transacao['Valor']:.2f}")

def registrar_transacao():
        print("="*30)
        print("Registrar Transação")
        transacao = {
        "Tipo" : input("Digite o tipo da transação (Despesa/Receita): "),
        "Descrição" : input("Digite a descrição da transação: "),
        "Valor" : float(input("Digite o valor da transação: "))
        }
        if transacao["Tipo"].Lower() == "despesa":
            return transacao
        elif transacao["Tipo"].Lower() == "receita":
            return transacao
        else:
            print("="*30)
            print("Tipo de transação inválido! A transação não será registrada.")
            return None

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
    4- Sair"""
    )
    print("="*30)
    resp = int(input("Digite o número da opção desejada: "))
    if resp == 1:
        transacao = registrar_transacao()
        if transacao is not None:
            transacoes.append(transacao)
    elif resp == 2:
        consultar_transacoes()
    elif resp == 3:
        mostrar_saldo()
    elif resp == 4:
        print("="*30)
        print("Saindo do programa...")
        break
    else: 
        print("="*30)
        print("Opção inválida! Tente novamente.")
print("="*30)
