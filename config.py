import json

def carregar(user) -> None:
    with open("config.json", "r") as arquivo:
        try:
            dados = json.load(arquivo)
        except Exception:
            return False

        if all(valor == "" for valor in dados.values()):
            return False

        user.username = dados['name']
        user.prefix = dados['country_code']
        user.greetings_manual = dados['greetings_manual']
        user.greetings_auto = dados['greetings_auto']
        arquivo.close()
        return True


def registrar(user) -> bool:
    print("\n-- Configurando o Script --\n[!] Dica: utilize <saudacao> e <nome> para inserir as variáveis no seu texto introdutório.")
    nome = input("\n> Digite o seu nome: ")
    country_code = input("> Digite o código do seu país (exemplo: Brasil +55, EUA +1) (sem o símbolo de +): ")
    greetings_manual = input("> Digite o seu texto introdutório para mensagens manuais: ")
    greetings_auto = input("> Digite o seu texto introdutório para mensagens automatizadas (digite c para usar o texto anterior): ")

    if greetings_auto == "c":
        greetings_auto = greetings_manual

    escrever_informacoes(nome, country_code, greetings_manual, greetings_auto)
    carregar(user)
    start = input("[!] Registro realizado com sucesso. Pressione ENTER para iniciar o programa.")
    return True


def escrever_informacoes(nome, cc, gm, ga):
    dicionario = {
        "name": nome,
        "country_code": cc,
        "greetings_manual": gm,
        "greetings_auto": ga
    }

    with open("config.json", "w", encoding="utf-8") as arquivo:
        json.dump(dicionario, arquivo, indent=4)
        arquivo.close()
    
