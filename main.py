import user as myuser
import formatting
import saudacao as mytime
import terminal
import logo
import whatsapp
import autolist
import config

user = myuser.User()
format = formatting.Formatting()

saudacao: str = mytime.definir_saudacao_momentanea()


def menu() -> bool:
    try:
        escolha = int(
            input(f"\n[!] {saudacao}, {user.username}!\n\n(1) Digitar números\n(2) Utilizar lista de números\n(3) Configurações\n(4) Sair" +
                  "\n\n> Escolha a opção: "))

        if escolha == 1:
            mensagem = user.greetings_manual.replace("<saudacao>", saudacao).replace("<nome>", user.username)
            whatsapp.abrir_whatsapp(mensagem, user)
            return True

        elif escolha == 2:
            format.corrigir_erros()
            autolist.ler_lista(user)
            return voltar_ao_menu()

        if escolha == 3:
            return config.registrar(user)

        else:
            return False

    except ValueError:
        return True


def voltar_ao_menu() -> bool:
    e = input('[?] Gostaria de retornar ao menu principal? (s/N): ')
    return e.upper() == 'S'


if __name__ == '__main__':
    user.session_logo = logo.definir_logo()
    if not config.carregar(user):
        print("[!] Não foi encontrada nenhuma configuração prévia. Portanto, realize-a preenchendo os dados:")
        config.registrar(user)

    while True:
        terminal.limpar()
        print(user.session_logo)
        if not menu():
            break
