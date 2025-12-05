import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


# -----------------------------
# ITERADOR PERSONALIZADO PARA LISTAR CONTAS
# -----------------------------
class ContasIterador:
    """Permite iterar sobre a lista de contas exibindo seus dados formatados."""
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            # Final da lista -> encerra iteração
            raise StopIteration
        finally:
            self._index += 1


# -----------------------------
# ENTIDADES DE CLIENTE
# -----------------------------
class Cliente:
    """Representa um cliente genérico com endereço e lista de contas."""
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """Executa a operação desejada (depósito/saque)."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Cliente específico com CPF, nome e data de nascimento."""
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# -----------------------------
# MODELO DE CONTA BANCÁRIA
# -----------------------------
class Conta:
    """Classe base de uma conta bancária com saldo, número e histórico."""
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Criação de contas."""
        return cls(numero, cliente)

    # Propriedades da conta
    @property
    def saldo(self): return self._saldo

    @property
    def numero(self): return self._numero

    @property
    def agencia(self): return self._agencia

    @property
    def cliente(self): return self._cliente

    @property
    def historico(self): return self._historico

    # ---------- OPERAÇÕES ----------
    def sacar(self, valor):
        """Realiza saque verificando saldo."""
        excedeu_saldo = valor > self.saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        """Realiza depósito se valor for positivo."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True

        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


# -----------------------------
# CONTA CORRENTE COM LIMITES
# -----------------------------
class ContaCorrente(Conta):
    """Conta com limite diário de valor e quantidade de saques."""
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Valida limites antes de realizar o saque."""
        numero_saques = len([
            t for t in self.historico.transacoes
            if t["tipo"] == Saque.__name__
        ])

        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor excede o limite. @@@")

        elif numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Limite de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# -----------------------------
# HISTÓRICO DE TRANSAÇÕES
# -----------------------------
class Historico:
    """Armazena e gera relatório das movimentações da conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self): return self._transacoes

    def adicionar_transacao(self, transacao):
        """Salva o tipo, valor e data da transação."""
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

    def gerar_relatorio(self, tipo_transacao=None):
        """Gera extrato filtrado ou completo."""
        for t in self._transacoes:
            if tipo_transacao is None or t["tipo"].lower() == tipo_transacao.lower():
                yield t


# -----------------------------
# CLASSES ABSTRATAS DE TRANSAÇÃO
# -----------------------------
class Transacao(ABC):
    """Define a estrutura padrão de uma operação bancária."""

    @property
    @abstractproperty
    def valor(self): pass

    @abstractclassmethod
    def registrar(self, conta): pass


class Saque(Transacao):
    """Transação de saque."""
    def __init__(self, valor): self._valor = valor

    @property
    def valor(self): return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """Transação de depósito."""
    def __init__(self, valor): self._valor = valor

    @property
    def valor(self): return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# -----------------------------
# DECORADOR PARA LOG DE OPERAÇÕES
# -----------------------------
def log_transacao(func):
    """Decora funções operacionais registrando hora e nome da operação."""
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return envelope


# -----------------------------
# FUNÇÕES DE INTERFACE E FLUXO
# -----------------------------
def menu():
    """Exibe o menu principal e retorna a opção escolhida."""
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    """Retorna o cliente com o CPF informado, se existir."""
    filtrados = [c for c in clientes if c.cpf == cpf]
    return filtrados[0] if filtrados else None


def recuperar_conta_cliente(cliente):
    """Retorna a primeira conta do cliente (ainda não permite escolher)."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    """Fluxo de depósito via entrada do usuário."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))


@log_transacao
def sacar(clientes):
    """Fluxo de saque via entrada do usuário."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Saque(valor))


@log_transacao
def exibir_extrato(clientes):
    """Mostra extrato filtrando transações do tipo saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")

    extrato = ""
    tem_transacao = False

    for transacao in conta.historico.gerar_relatorio(tipo_transacao="saque"):
        tem_transacao = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


@log_transacao
def criar_cliente(clientes):
    """Cadastra um novo cliente Pessoa Física."""
    cpf = input("Informe o CPF (somente número): ")

    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço completo: ")

    novo = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(novo)

    print("\n=== Cliente criado com sucesso! ===")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    """Cria uma conta corrente para um cliente existente."""
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    """Mostra todas as contas utilizando o iterador personalizado."""
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


# -----------------------------
# LOOP PRINCIPAL DA APLICAÇÃO
# -----------------------------
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Opção inválida! @@@")


main()
