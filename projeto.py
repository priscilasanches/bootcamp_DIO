import textwrap
#estabelecer um limite de 10 transações diárias
#mostrar no extrato data e hora de todas as transações
#criar decorador de log (data e hora e tipo de transação)/ gerador de relatórios /iterador personalizado

def menu():
    menu = f'''
    {"MENU".center(22,"=")}
    [1]\tDepósito
    [2]\tSaque
    [3]\tExtrato
    [4]\tCriar cliente
    [5]\tCriar conta
    [0]\tSair
    
    '''   
    return int(input(textwrap.dedent(menu)))
    
def criar_cliente(clientes):
    cpf = int(input("Informe os dígitos do cpf (apenas números): "))
    if encontrar_cliente(cpf, clientes):
        print("\nCliente já cadastrado!")
        return
    
    nome = input("Digite o nome do cliente: ")
    nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ") 
    logradouro = input("Informe o logradouro: ")
    nro = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Informe a cidade: ")
    estado = input("Informe a sigla do estado: ")
    
    clientes.append({"nome": nome, "dt_nascimento":nascimento, "cpf":cpf, "endereco": f"{logradouro}, {nro} - {bairro} - {cidade}/{estado}" })   
    print("Cliente cadastrado com sucesso!\n", clientes)    

def criar_conta_corrente(agencia, conta, clientes):
    cpf_cliente = int(input("Informe os dígitos do cpf do cliente (apenas números): "))
    
    if encontrar_cliente(cpf_cliente, clientes):
        print("Conta criada com sucesso!\n")
        return {"cpf":cpf_cliente, "agencia":agencia, "nro":conta}
            
    print("Cliente não cadastrado. Realizar o cadastramento antes da abertura da conta.")     
        
def encontrar_cliente(cpf, clientes):
    cliente = [cliente for cliente in clientes if cliente.get("cpf") == cpf]
    return cliente[0] if cliente else None

def depositar(saldo:float, valor:float, extrato:list, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: \tR$ {valor: 8.2f}") 
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nValor informado inválido")
    return (saldo, extrato)
    
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): 
    saldo_insuficiente = saldo < valor
    excedeu_valor_saque = valor > limite
    excedeu_numero_saques = numero_saques >= limite_saques
    
    if saldo_insuficiente:
        print("\nSaldo insuficiente!")
    
    elif excedeu_valor_saque:
        print("\nO valor do saque excede o limite!")
        
    elif excedeu_numero_saques:
        print("\nNúmero de saques excedido!")
        
    elif valor<=0:
        print("\nValor inválido!")
    
    else:
        saldo -= valor
        extrato.append(f"Saque: \tR$ {valor: 8.2f}") 
        numero_saques += 1
        print("\nSaque realizado com sucesso!")

    return saldo, extrato, numero_saques
          
def gerar_extrato(saldo, /, *, extrato):
    print("EXTRATO".center(25, "="))
    print("Não foram realizadas movimentações" if len(extrato)==0 else "")
    for i in extrato:
        print(i)
    print(f'Saldo: \tR$ {saldo: 8.2f}') 

def main():
    clientes = []
    saldo = 0
    contas = []
    extrato = []
    nro_saques = 0
    AGENCIA = "0001"
    LIMITE_NUMERO_SAQUES = 3
    LIMITE_VALOR_SAQUES = 500
    
    while True:
        opcao = menu()
        
        if opcao == 1:
            valor = float(input("Digite o valor: "))
            saldo, extrato = depositar(saldo, valor, extrato)
            
        elif opcao == 2:
            valor = float(input("Digite o valor: "))
            saldo, extrato, nro_saques = sacar(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite = LIMITE_VALOR_SAQUES, 
                numero_saques=nro_saques, 
                limite_saques=LIMITE_NUMERO_SAQUES                
            )
            
        elif opcao == 3:
            gerar_extrato(saldo, extrato=extrato)
            
        elif opcao == 4:
            criar_cliente(clientes)
            
        elif opcao == 5:
            conta = len(contas) + 1
            conta = criar_conta_corrente(AGENCIA, conta, clientes)
            if conta:
                contas.append(conta)
                print(contas)
            
        elif opcao == 0:
            break 
        
        else:
            print("Opção inválida", end="\n\n")
            
main()
