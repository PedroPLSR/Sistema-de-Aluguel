    # This is a sample Python script.
import re


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Usuario:
    def __init__(self, nome, cpf, senha):
        self.nome = nome
        self.senha = senha
        self.cpf = cpf
        self.imoveis = [];
        self.carteira = 0;
        self.isADM = False;
    def AdicionarImovelComParametros(self, tamanho: int, local: str, preço: float, dono):
        if (tamanho <= 0 or preço <= 0):  # RF[11]
            return;

        self.imoveis.append(Imovel(tamanho, local, preço, dono))

    def AdicionarImovel(self):
        tamanho = input("Digite qual o tamanho do imóvel a ser cadastrado: ")
        while (not re.match("^[0-9]+$", tamanho) or re.match("^0+$", tamanho)):
            tamanho = input("Digite um tamanho válido");
        local = input("Digite o local do imóvel: ")
        while not re.match("^(?=.*[A-Z])(?=.*[\W_])(?=.*[a-z]).*$", local):
            local = input("Coloque um local valido: ")

        preço = input("Digite o preço do aluguel: ")
        while not re.match("^[0-9]+$", preço) or re.match("^0+$", preço):
            preço = input("Digite um preço válido: ")

        self.imoveis.append(Imovel(int(tamanho), local, float(preço), self))
        print("Imovel cadastrado com sucesso.")


    def AdicionarFundos(self, valor: float):
        if (valor <= 0):  # RF[11]
            return "Valor não aceito";
        self.carteira += valor;
        return "Valor adicionado à carteira, carteira atual = R$" + str(self.carteira);


class ADM(Usuario):

    def __init__(self, nome, cpf, senha, bancoDeDados):
        super().__init__(nome, cpf, senha)
        self.isADM = True;
        self.BancoDeDados = bancoDeDados


class Imovel:
    def __init__(self, Tamanho, Local, Preço, Dono: Usuario):
        self.Tamanho = Tamanho;
        self.Local = Local;
        self.Preço = Preço;
        self.DiasAlugados = [];
        self.Dono = Dono;

    def AlugarDia(self, user: Usuario):
        dia = input("Que dia gostaria de alugar?")
        while (not re.match("^[0-9]+$", dia)):
            dia = input("Digite apenas numeros: ")
        dia = int(dia)
        while (dia <= 0 or dia >= 32):
            dia = int(input("Diga um dia válido: "))
        if (dia in self.DiasAlugados):
            print("Infelizmente esse dia já está alugado")
            return
        if (user.carteira < self.Preço):
            print("infelizmente, sua carteira não possui o suficiente para alugar esse local.")
            return
        self.DiasAlugados.append(dia)
        user.carteira -= self.Preço;
        self.Dono.carteira += self.Preço;
        print(f"Dia {dia} Alugado!")

    def MudaInfo(self):
        mudaNome = input("Gostaria de mudar o Local do imovel? 1- Sim | 2-Nao")
        while (not re.match("^[0-9]{1}$", mudaNome)):
            mudaNome = input("Digite uma operacao valida")
        if (mudaNome == "1"):
            novoNome = input("Digite o novo Local: ")
            while (not re.match("^[A-z]+", novoNome)):
                novoNome = input("Digite um nome de verdade: ")
            self.Local = novoNome;

        mudaTamanho = input("Gostaria de mudar o Tamanho do imovel? 1- Sim | 2-Nao")
        while (not re.match("^[0-9]{1}$", mudaTamanho)):
            mudaTamanho = input("Digite uma operacao valida")
        if (mudaTamanho == "1"):
            novoTamanho = input("Digite o novo Tamanho: ")
            while (not re.match("^[0-9]+$", novoTamanho)):
                novoTamanho = input("Digite um tamanho de verdade: ")
            self.Tamanho = novoTamanho;

        mudaPreco = input("Gostaria de mudar o Preco do imovel? 1- Sim | 2-Nao")
        while (not re.match("^[0-9]{1}$", mudaPreco)):
            mudaPreco = input("Digite uma operacao valida")
        if (mudaPreco == "1"):
            novoPreco = input("Digite o novo Preco: ")
            while (not re.match("^[0-9]+$", novoPreco)):
                novoPreco = input("Digite um preco valido: ")
            self.Preço = novoPreco;


# BANCO DE DADOS E ROTAS --------------------------------------------------------------------------------------------------------
banco_de_dados = {}


def AdicionarUsuário(usuario: Usuario):
    banco_de_dados.update({usuario.cpf: usuario})
    if (usuario.isADM):
        print("ADM")
    return banco_de_dados[usuario.cpf]
    pass


def RemoveUsuário(key):
    del banco_de_dados[key]
    pass




def _PROTOCOL_SINGUP():
    nome = input("Digite seu nome:")
    while not re.match("[A-z]+", nome):
        nome = input("Por favor, digite seu nome Completo:")

    CPF = input("Digite seu CPF:")
    while not re.match("[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}", CPF):
        CPF = input("Digite um CPF válido")

    senha = input("Digite uma senha que contenha ao menos uma letra maiúscula e um símbolo:")
    while not re.match("^(?=.*[A-Z])(?=.*[\W_])(?=.*[a-z]).*$", senha):
        senha = input("Sua senha está muito fraca, tente novamente:")

    while not input("Confirme sua senha:") == senha:
        print("Senhas não batem, tente novamente")

    print("Criado Usuario com nome de:", nome, "e cpf de: ", CPF);
    return AdicionarUsuário(Usuario(nome, CPF, senha));
    pass

def _PROTOCOL_LOGIN():
    CPF = input("Por favor, digite seu CPF:")
    if (CPF in banco_de_dados.keys()):
        usuario = banco_de_dados[CPF]

        print("Bem-vindo", usuario.nome)
        senha = input("Por favor, digite sua senha:")
        if (senha == usuario.senha):
            print("Login realizado. Abrindo Aplicação");
            return banco_de_dados[usuario.cpf];
        else:
            contador = 0
            while (senha != usuario.senha):
                senha = input("Senha incorreta. tente novamente: ")
                contador += 1

                if (contador == 3):
                    print("Infelizmente você errou a senha 3 vezes, vamos encerrar o login.")
                    break;
            if (senha == usuario.senha):
                print("Login realizado. Abrindo Aplicação");
                return banco_de_dados[usuario.cpf];
            if (contador == 3): return None;
    else:
        print("Usuário não encontrado.")
        op = int(input("Se quiser tentar digitar novamente, digite 1. Se quiser se cadastrar, digite 2."))
        if (op == 1):
            return _PROTOCOL_LOGIN()
        elif (op == 2):
            return _PROTOCOL_SINGUP()
        else:
            print("Comando desconhecido. Encerrando processo de Login.")
            return None;
    pass


def _PROTOCOL_SHOW_IMOVEIS(BancoDeDados: dict):
    imoveisDisponiveis = []

    for user in BancoDeDados.keys():
        if len(BancoDeDados[user].imoveis) > 0:
            for imovel in BancoDeDados[user].imoveis:
                imoveisDisponiveis.append(imovel);
    return imoveisDisponiveis;


# MAIN ---------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pedro = ADM("Pedro Quinhas", "2111138", "BANANAS", banco_de_dados)
    pedro.AdicionarImovelComParametros(90, "Rua das graças", 900.00, pedro)
    pedro.AdicionarImovelComParametros(50, "Rua eusebio", 9000.00, pedro)
    AdicionarUsuário(pedro)
    print(banco_de_dados)
    while 1:
        user = _PROTOCOL_LOGIN();
        if user is not None:
            op = 1
            while (op <= 9 and op >= 1 and user != None):
                op = input(user.nome + ", o que gostaria de fazer?"
                                       "\n1-Depósito"
                                       "\n2-Alugar um local"
                                       "\n3-Mudar nome do perfil"
                                       "\n4-Cadastrar um local"
                                       "\n5-Verificar locais cadastrados"
                                       "\n6-Verificar extrato" +
                                        ("\n7- Mostrar Banco De Dados" if user.isADM else "") +
                                                                                         "\n0-Sair da conta.")
                if (re.match("^[0-9]{1}$", op)):
                    op = int(op)

                    if (op == 1):
                        valor = input("Quanto gostaria de depositar?")
                        while (not re.match("^[0-9]+$", valor)):
                            valor = input("Digite um valor valido")
                        print(user.AdicionarFundos(int(valor)));
                    if (op == 2):
                        lista = _PROTOCOL_SHOW_IMOVEIS(banco_de_dados)
                        contador = 0
                        if (len(lista) > 0):
                            for imovel in lista:
                                contador += 1
                                print("=========================================")
                                print("Local:", contador)
                                print("Espaço:", imovel.Tamanho)
                                print("Local:", imovel.Local)
                                print("Dono:", imovel.Dono.nome)
                                print("Preco:", imovel.Preço)
                                print("=========================================")

                            localEscolhido = input("Qual local você deseja alugar?")
                            while not re.match("^[1-9]+$", localEscolhido):
                                localEscolhido = input("Digite uma opção válida: ")
                            if int(localEscolhido) > len(lista) or int(localEscolhido) < 0:
                                print("Esse numero não é válido!")
                            else:
                                lista[int(localEscolhido) - 1].AlugarDia(user)
                    if (op == 3):
                        novoNome = input("Digite seu novo nome: ")
                        while not re.match("[A-z]+", novoNome):
                            novoNome = input("Digite um nome valido: ")
                        user.nome = novoNome;
                    if (op == 4):
                        user.AdicionarImovel();
                    if (op == 5):
                        contador = 0
                        for imovel in user.imoveis:
                            contador += 1
                            print("=========================================")
                            print("Local:", contador)
                            print("Espaço:", imovel.Tamanho)
                            print("Local:", imovel.Local)
                            print("Dono:", imovel.Dono.nome)
                            print("Preco:", imovel.Preço)
                            print("=========================================")

                        mudanca = input("Deseja alterar alguma informacao? 1- Sim | 2- Nao")
                        while (not re.match("^[1-2]{1}$", mudanca)):
                            mudanca = input("Digite uma operacao valida")
                        if (mudanca == "1"):
                            ImovelMudado = input("Qual imovel deseja mudar?")
                            while (not re.match("^[0-9]{1}$", ImovelMudado)):
                                ImovelMudado = input("Digite um local valido")
                            if (not int(ImovelMudado) > len(user.imoveis)):
                                mudaOuApaga = input("Deseja apagar ou mudar? 1- Apagar | 2- Mudar")
                                while (not re.match("^[1-2]{1}$", mudaOuApaga)):
                                    mudaOuApaga = input("Digite um local valido")

                                if (mudaOuApaga == "1"):
                                    user.imoveis.remove(user.imoveis[int(ImovelMudado) - 1])
                                else:
                                    user.imoveis[int(ImovelMudado) - 1].MudaInfo();
                            else:
                                print("O local Selecionado nao existe")
                    if (op == 6):
                        print(f"Seu saldo é de R${user.carteira}")
                    if (op == 7 and user.isADM):
                        print(banco_de_dados)

                        mudanca = input("Deseja apagar alguma informacao? 1- Sim | 2- Nao")
                        while (not re.match("^[1-2]{1}$", mudanca)):
                            mudanca = input("Digite uma operacao valida")
                        if (mudanca == "1"):
                            userIndex = input("Qual usuario deseja mudar?")
                            while (not re.match("^[0-9]{1}$", userIndex)):
                                userIndex = input("Digite um usuario valido")
                            if (not int(userIndex) > len(banco_de_dados)):
                                
                                mudaOuApaga = input("Deseja apagar ? 1- Apagar | 2- Nao Apagar")
                                while (not re.match("^[1-2]{1}$", mudaOuApaga)):
                                    mudaOuApaga = input("Digite a confirmação corretamente")

                                if (mudaOuApaga == "1"):
                                    contador = 0;
                                    chave = "";
                                    for key in banco_de_dados.keys():
                                        contador+=1
                                        if contador == int(userIndex):
                                            chave = key;
                                            break
                                    if user.nome == (banco_de_dados[chave]).nome: 
                                        user = None;
                                    RemoveUsuário(chave)
                                    
                                else:
                                    pass
                            else:
                                print("O local Selecionado nao existe")

                else:
                    print("Por favor, digite uma operação válida.")
                    op = 1;

        else:
            comando = input("Para logar novamente, digite 1.")
            if (comando != "1"):
                break

    pass
