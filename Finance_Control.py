import banco
from datetime import datetime
banco.criar_tabela()

def mostrar_saldo(saldo):
    print("="*30)
    print("Ver Saldo")
    print(f"Saldo atual: R$ {saldo:.2f}")

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

        if not validar_transacao(tipo,valor):
            print("="*30)
            print("Tipo ou Valor Inválido! A transação não será registrada.")
            return None
        categoria = escolher_categoria()
        if categoria is None:
            print("Categoria Inválida!")
            return None
        
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        transacao = {
            "Tipo": tipo,
            "Descrição": descricao,
            "Valor": valor,
            "Categoria": categoria,
            "Data": data
        }
        
        return transacao

def validar_transacao(tipo,valor):
    if tipo != "despesa" and tipo != "receita":
        return False
    if valor <= 0:
        return False

    return True

def escolher_categoria():
    print("="*30)
    print("Categorias")
    print("1- Alimentação")
    print("2- Transporte")
    print("3- Lazer")
    print("4- Estudos")
    print("5- Salário")
    print("6- Outros")

    try:
        opcao = int(input("Escolha uma categoria: "))
    except ValueError:
        return None

    categorias = {
        1: "alimentação",
        2: "transporte",
        3: "lazer",
        4: "estudos",
        5: "salário",
        6: "outros"
    }
    return categorias.get(opcao)

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
            banco.salvar_transacao(transacao)
    elif resp == 2:
        transacoes = banco.consultar_transacoes()
        if not transacoes:
            print("="*30)
            print("Não há transações registradas.")
        else:
            print("="*30)
            print("Consultar Transações.")
            for transacao in transacoes:
                data_banco = transacao[5]
                data_formatada = datetime.strptime(
                    data_banco,
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d/%m/%Y %H:%M")
                print(
                    f"ID: {transacao[0]},"
                    f" Tipo: {transacao[1]},"
                    f" Descrição: {transacao[2]},"
                    f" Valor: {transacao[3]:.2f},"
                    f" Categoria: {transacao[4]},"
                    f" Data: {data_formatada}"
                )
    elif resp == 3:
        saldo = banco.calcular_saldo()
        mostrar_saldo(saldo)
    elif resp == 4:
        print("="*30)
        try:
            id_transacao = int(input("Digite o ID da transação que deseja excluir: "))
        except ValueError:
            print("Digite um ID valido!")
            continue
        
        excluiu = banco.excluir_transacao(id_transacao)

        if excluiu:
            print("Transação excluída com sucesso.")
        else:
            print("Nenhuma transação encontrada com esse ID.")
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
        if validar_transacao(tipo,valor):
            editou = banco.editar_transacao(id_transacao, tipo, descricao, valor)
            if editou:
                print("Transação atualizada com sucesso.")
            else:
                print("Nenhuma transação foi encontrada com esse ID.")
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
