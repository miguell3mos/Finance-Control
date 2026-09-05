#Imporar dados do banco que contém as funções.
import banco

#Importar função para usar datas no software.
from datetime import datetime

#Função de criar tabela para armazenar dados dentro do banco de dados.
banco.criar_tabela()


def mostrar_saldo(saldo):
    """Função que mostra o saldo atual."""
    print("="*30)
    print("Ver Saldo")
    print(f"Saldo atual: R$ {saldo:.2f}")

def registrar_transacao():
        """Função completa contendo todos os input para registrar a transação."""
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
    """Função para validar transação se é despesa ou receita e se o valor é maior que zero."""
    if tipo != "despesa" and tipo != "receita":
        return False
    if valor <= 0:
        return False

    return True

def escolher_categoria():
    """Função para escolher categória da transação."""
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

def mostrar_transacoes(transacoes):
    for transacao in transacoes:
        data_banco = transacao[5]
        data_formatada = datetime.strptime(
            data_banco,
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%d/%m/%Y %H:%M")
        print(
            f"ID: {transacao[0]}, "
            f"Tipo: {transacao[1]}, "
            f"Descrição: {transacao[2]}, "
            f"Valor: {transacao[3]:.2f}, "
            f"Categoria: {transacao[4]}, "
            f"Data: {data_formatada}"
        )

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
    6- Filtrar Categorias
    7- Resumo por Categoria
    8- Resumo Mensal
    9- Buscar por Período
    10- Sair"""
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
            mostrar_transacoes(transacoes)
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
        categoria = escolher_categoria()
        if categoria is None:
            print("Categoria Inválida!")
            continue
        if validar_transacao(tipo,valor):
            editou = banco.editar_transacao(id_transacao, tipo, descricao, valor, categoria)
            if editou:
                print("Transação atualizada com sucesso.")
            else:
                print("Nenhuma transação foi encontrada com esse ID.")
        else:
            print("Valor ou Tipo está inválido.")
    elif resp == 6:
        categoria = escolher_categoria()
        if categoria is None:
            print("Categoria Inválida.")
            continue
        transacoes = banco.buscar_por_categorias(categoria)
        if not transacoes:
            print("Nenhuma transação encontrada nessa categoria.")
        else:
            mostrar_transacoes(transacoes) 
    elif resp == 7:
        resumo = banco.resumo_por_categoria()

        if not resumo:
            print("Não há depesas registradas.")
        else:
            print("="*30)
            print("Resumo por Categoria")
            for categoria, total in resumo:
                print(f"{categoria.title()}: R$ {total:.2f}")
    elif resp == 8:
        try:
            ano = int(input("Digite o ano: "))
            mes = int(input("Digite o mês: "))
        except ValueError:
            print("Ano e Mês precisam ser números.")
            continue
        if mes < 1 or mes > 12:
            print("Mês inválido.")
            continue
        resumo = banco.resumo_mensal(ano,mes)
        receita = 0
        despesa = 0

        for tipo, total in resumo:
            if tipo == "receita":
                receita = total
            elif tipo == "despesa":
                despesa = total
        saldo_mes = receita - despesa

        print("="*30)
        print(f"Resumo de {mes:02d}/{ano}")
        print(f"Receitas: R$ {receita:.2f}")
        print(f"Despesas: R$ {despesa:.2f}")
        print(f"Saldo do mês: R$ {saldo_mes:.2f}")
    elif resp == 9:
        data_inicio = input("Digite a data inicial (dd/mm/aaaa): ").strip()
        data_fim = input("Digite a data final (dd/mm/aaaa): ").strip()
        try:
            inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            fim = datetime.strptime(data_fim, "%d/%m/%Y")
        except ValueError:
            print("Data Inválida: use o formato dd/mm/aaaa.")
            continue
        inicio_banco = inicio.strftime("%Y-%m-%d 00:00:00")
        fim_banco = fim.strftime("%Y-%m-%d 23:59:59")

        transacoes = banco.buscar_por_periodo(inicio_banco,fim_banco)
        if not transacoes:
            print("Nenhuma transação encontrada nesse período.")
        else:
            mostrar_transacoes(transacoes)
    elif resp == 10:
        print("="*30)
        print("Saindo do programa...")
        break
    else: 
        print("="*30)
        print("Opção inválida! Tente novamente.")
print("="*30)
