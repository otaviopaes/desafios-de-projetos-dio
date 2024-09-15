import textwrap

def menu():
    menu = """\n
    **** Escolha uma operação ****

    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tAbrir Conta
    [5]\tListar Contas
    [6]\tCadastrar Usuário
    [0]\tSair

    ******************************
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"\nDepósito: R$ {valor:.2f} realizado com sucesso!\n")
    else:
        print("Valor informado não aceito para depósito, favor repita a operação.")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    if excedeu_saldo:
        print("Saldo insuficiente, verifique seu extrato.")
    elif excedeu_limite:
        print("Valor informado excede o seu limite. Repita a operação e informe novo valor para saque.")
    elif excedeu_saques:
        print("Operação não realizada. Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\nSaque: R$ {valor:.2f} realizado com sucesso!\n")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nCPF já cadastrado! Apenas 1 usuário por CPF é permitido. Refaça a operação.")
        return
    
    nome = input ("Informe o nome completo: ")
    data_nascimento = input ("Informe a data de nascimento (dd-mm-aaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print ("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input ("\nInforme o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\nConta criada com sucesso")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print ("\nUsuário não encontrado, confirme o cadastro do usuário.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios= []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
            input("\nPressione <ENTER> para continuar...")
                
        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            input("\nPressione <ENTER> para continuar...")
            
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
            input("\nPressione <ENTER> para continuar...")
        
        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
            input("\nPressione <ENTER> para continuar...")
        
        elif opcao == "5":
            listar_contas(contas)
            input("\nPressione <ENTER> para continuar...")
        
        elif opcao == "6":
            criar_usuario(usuarios)
            input("\nPressione <ENTER> para continuar...")

        elif opcao == "0":
            print("\n\n**** Operação encerrada. Obrigado por usar nosso sistema! ****\n\n")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()
