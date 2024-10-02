saldo = 0
saques = []
depositos = []
LIMITE_NUMERO_SAQUES = 3
LIMITE_VALOR_SAQUES = 500

def deposito(valor):
    if valor > 0:
        depositos.append(valor)
        print("Depósito realizado!", end="\n\n")
        return valor
    else:
        print("O valor do depósito deve ser maior que 0", end="\n\n")
        return 0

def saque(valor, saldo):
    excedeu_valor_saque = valor > LIMITE_VALOR_SAQUES
    excedeu_numero_saques = len(saques) >= LIMITE_NUMERO_SAQUES
    if saldo >= valor and not(excedeu_valor_saque) and not(excedeu_numero_saques):
        saques.append(valor)
        print("Saque realizado!", end="\n\n")
        return valor 
    elif saldo <= valor:
        print("Saldo insuficiente", end="\n\n") 
    else:
        print("Valor do saque ultrapassa o número de saques ou limite máximo permitido", end="\n\n")
    return 0
          
def extrato():
    print("EXTRATO".center(19, "#"))
    for i in saques:
        print(f'Saque: R$ {i: 8.2f}')
    for i in depositos:
        print(f'Depósito: R$ {i: 8.2f}')
    print(f'Saldo: R$ {saldo: 8.2f}') 


while True:
    print(f'''
{"MENU".center(10," ")}
1 - depósito
2 - saque
3 - extrato
0 - sair
''')
    
    opcao = int(input("Escolha a operação que deseja realizar: "))
    
    if opcao == 1:
        valor = float(input("Digite o valor: "))
        saldo += deposito(valor)
    elif opcao == 2:
        valor = float(input("Digite o valor: "))
        saldo -= saque(valor, saldo)
    elif opcao == 3:
        extrato()
    elif opcao == 0:
        break 
    else:
        print("Opção inválida", end="\n\n")
   