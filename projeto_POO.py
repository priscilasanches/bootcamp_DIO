from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
            
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)   

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, dt_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.dt_nascimento = dt_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod #método fábrica
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
            
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self) -> float:
        return self._agencia    
    
    @property
    def cliente(self) -> float:
        return self._cliente    
    
    @property
    def historico(self) -> float:
        return self._historico
  
    def sacar(self, valor):
        saldo_insuficiente = self.saldo < valor

        if saldo_insuficiente:
            print("\nSaldo insuficiente!")
                   
        elif valor <= 0:
            print("\nValor inválido!")
        
        else:
            self._saldo -= valor
            print("\nSaque realizado com sucesso")
            return True

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True
        else:
            print("\nValor informado inválido")
            return False 
    
class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques 
        
    #sobrepor o método sacar para inserir validações
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"]) 
        
        excedeu_valor_saque = valor > self._limite
        excedeu_numero_saques = numero_saques >= self._limite_saques
              
        if excedeu_valor_saque:
            print("\nO valor do saque excede o limite!")
            
        elif excedeu_numero_saques:
            print("\nNúmero de saques excedido!")
        
        else:
            return super().sacar(valor) 
        
        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
       self._valor = valor 
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
       self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(),
            }
        )

def encontrar_cliente(cpf, clientes):
    cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente[0] if cliente else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return
    #para este caso não tem como escolher conta
    return cliente.contas[0]
    
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Informe o valor: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Informe o valor: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("EXTRATO".center(25, "="))
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
     extrato = "Não foram realizadas movimentações" 
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")  
    print("="*33)   

def criar_cliente(clientes):
    cpf = input("Informe os dígitos do cpf (apenas números): ")
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
    endereco = f"{logradouro}, {nro} - {bairro} - {cidade}/{estado}" 
    
    cliente = PessoaFisica(nome=nome, dt_nascimento=nascimento, cpf=cpf, endereco=endereco) 
    
    clientes.append(cliente)
 
    print("Cliente cadastrado com sucesso!\n", cliente.nome)  
      
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = Conta_Corrente.nova_conta(numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\n=== Conta Criada com Sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))  
          
def menu():
    menu = f'''
    {"MENU".center(22,"=")}
    [1]\tDepósito
    [2]\tSaque
    [3]\tExtrato
    [4]\tCriar cliente
    [5]\tCriar conta
    [6]\tListar contas
    [0]\tSair 
    '''   
    return int(input(textwrap.dedent(menu)))

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == 1:
            depositar(clientes)
            
        elif opcao == 2:
            sacar(clientes)
            
        elif opcao == 3:
            exibir_extrato(clientes)
            
        elif opcao == 4:
            criar_cliente(clientes)
            
        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 6:
            listar_contas(contas)
            
        elif opcao == 0:
            break 
        
        else:
            print("Opção inválida", end="\n\n")
            
main()
 