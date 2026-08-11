from cryptography.fernet import Fernet
import os

ARQUIVO_CHAVE = "chave.key"
ARQUIVO_SENHAS = "senhas.txt"


# Gera e salva uma nova chave de criptografia
def gerar_chave():
    chave = Fernet.generate_key()

    with open(ARQUIVO_CHAVE, "wb") as arquivo:
        arquivo.write(chave)


# Carrega a chave existente ou gera uma nova
def carregar_chave():
    if not os.path.exists(ARQUIVO_CHAVE):
        gerar_chave()

    with open(ARQUIVO_CHAVE, "rb") as arquivo:
        return arquivo.read()


# Inicializa a chave e o Fernet
chave = carregar_chave()
fernet = Fernet(chave)


# Adiciona uma nova senha criptografada
def adicionar_senha():
    servico = input("Nome do serviço: ")
    usuario = input("Usuário/E-mail: ")
    senha = input("Senha: ")

    senha_criptografada = fernet.encrypt(
        senha.encode()
    ).decode()

    with open(ARQUIVO_SENHAS, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"{servico}|{usuario}|{senha_criptografada}\n"
        )

    print("\nSenha salva com sucesso!")


# Lista todos os serviços cadastrados
def listar_servicos():
    if not os.path.exists(ARQUIVO_SENHAS):
        print("Nenhuma senha cadastrada.")
        return

    print("\nServiços cadastrados:")

    with open(ARQUIVO_SENHAS, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            servico = linha.strip().split("|")[0]
            print("-", servico)


# Busca e exibe os dados de um serviço
def buscar_senha():
    servico_busca = input("Digite o nome do serviço: ")

    if not os.path.exists(ARQUIVO_SENHAS):
        print("Nenhuma senha cadastrada.")
        return

    with open(ARQUIVO_SENHAS, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            servico, usuario, senha = linha.strip().split("|")

            if servico.lower() == servico_busca.lower():
                senha = fernet.decrypt(
                    senha.encode()
                ).decode()

                print("\n=== DADOS ===")
                print("Serviço:", servico)
                print("Usuário:", usuario)
                print("Senha:", senha)

                return

    print("Serviço não encontrado.")


# Menu principal do gerenciador de senhas
while True:
    print("\n===== GERENCIADOR DE SENHAS =====")
    print("1 - Adicionar senha")
    print("2 - Listar serviços")
    print("3 - Buscar senha")
    print("4 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_senha()

    elif opcao == "2":
        listar_servicos()

    elif opcao == "3":
        buscar_senha()

    elif opcao == "4":
        print("Até logo!")
        break

    else:
        print("Opção inválida. Tente novamente.")