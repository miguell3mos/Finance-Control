transacoes = []
saldo = 0
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
        print("="*30)
        print("Registrar Transação")
        transacao = {
        "Tipo" : input("Digite o tipo da transação (Despesa/Receita): "),
        "Descrição" : input("Digite a descrição da transação: "),
        "Valor" : float(input("Digite o valor da transação: "))
        }
        if transacao["Tipo"].lower() == "despesa":
            saldo -= transacao["Valor"]
            valido = True
        elif transacao["Tipo"].lower() == "receita":
            saldo += transacao["Valor"]
            valido = True
        else:
            print("="*30)
            print("Tipo de transação inválido! A transação não será registrada.")
            valido = False
        if valido:
            transacoes.append(transacao)
            print("="*30)
            print("Transação registrada com sucesso!")
        else:
            print("="*30)
            print("Transação não registrada.")
    elif resp == 2:
        if not transacoes:
            print("="*30)
            print("Não há transações registradas.")
        else:
            print("="*30)
            print("Consultar Transações")
            for transacao in transacoes:
                print(f"Tipo: {transacao['Tipo']}, Descrição: {transacao['Descrição']}, Valor: {transacao['Valor']:.2f}")
    elif resp == 3:
        print("="*30)
        print("Ver Saldo")
        print(f"Saldo atual: R$ {saldo:.2f}")
    elif resp == 4:
        print("="*30)
        print("Saindo do programa...")
        break
    else: 
        print("="*30)
        print("Opção inválida! Tente novamente.")
print("="*30)
