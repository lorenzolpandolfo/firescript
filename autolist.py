import whatsapp
import saudacao as mytime
import formatting

format = formatting.Formatting()

saudacao = mytime.definir_saudacao_momentanea()


def ler_lista(user) -> None:
    print("")
    with open("numeros.txt", "r+", encoding="utf8") as arquivo:
        linhas = arquivo.readlines()
        edit = linhas.copy()
        arquivo.close()

    for linha in linhas:
        nome = linha.split(",")[0]
        telefone = linha.split(",")[1]

        mensagem = user.greetings_auto.replace("<nome>", user.username).replace("<saudacao>", saudacao)

        # Mandando mensagem
        e = input(f"[?] Mandar mensagem para {nome}? (S/n): ").upper()
        if e == 'S' or e == '':
            whatsapp.abrir_whatsapp(mensagem, user, telefone)

        elif e == 'X':
            print("\n[X] Abortando operação. As alterações no arquivo foram salvas.\n")
            format.escrever_correcoes(edit)
            break

        # Excluindo nome do arquivo
        e = input(f"[?] Excluir {nome} do arquivo? (S/n): ").upper()
        if e == 'S' or e == '':
            edit.remove(linha)

        elif e == 'X':
            print("\n[X] Abortando operação. As alterações no arquivo foram salvas.\n")
            format.escrever_correcoes(edit)
            break

        print("")

    format.escrever_correcoes(edit)
    print("[!] Os números acabaram e o arquivo foi atualizado.")
