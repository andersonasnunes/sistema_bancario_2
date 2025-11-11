# 🏦 Sistema Bancário em Python

Um sistema bancário desenvolvido em **Python** com **Programação Orientada a Objetos (POO)**, utilizando conceitos de **abstração, herança, polimorfismo, encapsulamento** e **iteradores personalizados**.  
O projeto permite **criar clientes, contas, realizar depósitos, saques e emitir extratos bancários** de forma interativa via terminal.

---

## 🚀 Funcionalidades

✅ Criar clientes (CPF, nome, data de nascimento e endereço)  
✅ Criar contas correntes associadas a clientes  
✅ Realizar **depósitos** e **saques** com controle de limites  
✅ Emitir **extratos** com histórico de transações  
✅ Listar todas as contas cadastradas  
✅ Decorator de **log de transações** (com data e hora)  
✅ Iterador personalizado para exibir contas formatadas  

---

## 🧱 Estrutura do Código

| Classe / Função | Descrição |
|------------------|------------|
| **Cliente** | Classe base com dados de endereço e contas. |
| **PessoaFisica** | Herda de `Cliente`. Adiciona nome, CPF e data de nascimento. |
| **Conta** | Classe base para contas bancárias, com saldo e operações básicas. |
| **ContaCorrente** | Herda de `Conta`. Adiciona limite e número máximo de saques. |
| **Historico** | Armazena e gera relatórios de transações (saques e depósitos). |
| **Transacao** | Classe abstrata que define a estrutura das transações. |
| **Saque / Deposito** | Implementam a classe abstrata `Transacao`. |
| **ContasIterador** | Iterador customizado que percorre e exibe as contas formatadas. |
| **log_transacao** | Decorator que registra logs de execução com data/hora. |
| **menu()** | Exibe o menu de operações. |
| **filtrar_cliente()** | Localiza cliente pelo CPF. |
| **recuperar_conta_cliente()** | Recupera a conta associada ao cliente. |

---

## 🧮 Regras de Negócio

- Cada **conta corrente** possui:
  - 💰 Limite de saque: **R$ 500,00**
  - 🔁 Máximo de **3 saques por dia**
- Não é permitido sacar valor maior que o saldo.
- Apenas valores **positivos** podem ser sacados ou depositados.
- Um cliente pode ter **mais de uma conta**.

---

## 🖥️ Menu Interativo

Ao executar o programa, será exibido o seguinte menu no terminal:  


=============== MENU ================  
[d] Depositar  
[s] Sacar  
[e] Extrato  
[nc] Nova conta  
[lc] Listar contas  
[nu] Novo usuário  
[q] Sair  
=>  

---

## 📂 Exemplo de Uso

### 1️⃣ Criar Cliente  
Informe o CPF (somente número): 12345678900  
Informe o nome completo: João Silva  
Informe a data de nascimento (dd-mm-aaaa): 01-01-1990  
Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): Rua A, 10 - Centro - SP/SP  
=== Cliente criado com sucesso! ===  


### 2️⃣ Criar Conta
Informe o CPF do cliente: 12345678900  
=== Conta criada com sucesso! ===  


### 3️⃣ Realizar Depósito  
Informe o CPF do cliente: 12345678900  
Informe o valor do depósito: 1000  
=== Depósito realizado com sucesso! ===  


### 4️⃣ Efetuar Saque  
Informe o CPF do cliente: 12345678900  
Informe o valor do saque: 200  
=== Saque realizado com sucesso! ===  


### 5️⃣ Consultar Extrato  
================ EXTRATO ================  
Saque:  
R$ 200.00  
Saldo:  
R$ 800.00  


---  

## 🧩 Padrões e Conceitos Utilizados  

- 🔹 **Abstração:** Classes genéricas (`Transacao`, `Conta`) que servem de modelo.    
- 🔹 **Herança:** `PessoaFisica` e `ContaCorrente` derivam de classes bases.   
- 🔹 **Polimorfismo:** Métodos sobrescritos, como `sacar()` em `ContaCorrente`.  
- 🔹 **Encapsulamento:** Atributos privados (`_saldo`, `_cliente`, etc).  
- 🔹 **Iterador Customizado:** `ContasIterador` para percorrer contas.  
- 🔹 **Decorator:** `log_transacao` registra operações no terminal.  

---  

## 🧰 Tecnologias Utilizadas  

- 🐍 **Python 3.10+**  
- 📦 Módulos padrão:  
  - `textwrap`  
  - `datetime`  
  - `abc`  

---  
 
## 🏁 Como Executar  

1. **Clone o repositório**  
   ```bash  
   git clone https://github.com/seu-usuario/sistema-bancario-python.git
   cd sistema-bancario-python
