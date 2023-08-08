import webbrowser

from urllib.parse import quote
import datetime
import logo
import os
import re
import pyautogui
import time
import psutil
import random


class Usuario:
    def __init__(self):
        self.logo = logo.nova

        try:
            self.bateria = psutil.sensors_battery()
        except:
            pass


user = Usuario()


def horario() -> str:
    agora = datetime.datetime.now()
    meiodia = agora.replace(hour=12, minute=0, second=0, microsecond=0)
    seis = agora.replace(hour=18, minute=0, second=0, microsecond=0)

    if agora < meiodia:
        return "Bom dia"

    elif seis > agora > meiodia:
        return "Boa tarde"

    else:
        return "Boa noite"


saudacao: str = horario()


def limpar_terminal() -> None:
    # rodando em windows
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def abrir_whatsapp(msg, num=None) -> None:
    msg = quote(msg).strip()

    if num is None:
        num = input("> Digite um número de telefone (sem o 55): ")
    else:
        num = num.strip()

    url = f"https://wa.me/55{num}?text={msg}"
    webbrowser.open(url)

    largura, altura = pyautogui.size()
    centro_x = largura // 2
    centro_y = altura // 2

    pyautogui.moveTo(centro_x, centro_y - 180)

    # Conferir se a bateria está fraca
    bateria_fraca = False

    try:
        if user.bateria.percent <= 20:
            bateria_fraca = True
    except:
        pass

    # definir o tempo de espera conforme a bateria
    if bateria_fraca:
        time.sleep(2)

    else:
        time.sleep(1.4)

    r, g, b = pyautogui.pixel(centro_x, centro_y - 180)

    # clicando no botao de iniciar conversa
    if r == 18 and g == 140 and b == 126:
        pyautogui.click()
        pyautogui.moveTo(centro_x, centro_y - 120)

    if bateria_fraca:
        time.sleep(1.7)
    else:
        time.sleep(1.1)

    pyautogui.click()


def menu() -> int:
    try:
        escolha = int(
            input(f"\n[!] {saudacao}!\n\n(1) Digitar números\n(2) Utilizar lista de números\n(3) Sair\n" +
                  "\n> Escolha a opção: "))

        if escolha == 1:
            mensagem = f"Olá, {saudacao.lower()}! Tudo bem? Aqui é o(a) (seu nome)!"
            abrir_whatsapp(mensagem)
            voltar_ao_menu()

        elif escolha == 2:
            corrigir_erros()
            ler_lista()

        else:
            return 0

    except ValueError as error:
        print(error)


def corrigir_erros() -> None:
    with open("numeros2.txt", "r+", encoding='utf8') as arquivo:
        linhas = arquivo.readlines()
        conserto = []
        numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        for mainindex, linha in enumerate(linhas):
            linha = remover_espacos_desnecessarios(linha.replace("-", "").replace("(", "").replace(")", "")).replace("+", "")

            if checar_se_ha_numero(linha):
                if ',' in linha:
                    numero = linha.split(",")[1]
                    # formatando o numero corretamente
                    numero = re.sub(r'\D', '', numero)
                    # formatando o nome corretamente
                    nome = linha.split(",")[0].strip()
                    # adicionando a virgula na linha, com nome e numero formatados corretamente
                    linha = nome + f", {numero}"
                    # removendo emojis da linha
                    linha_formatada = remover_emojis(linha.replace("\n", ""))
                    # adiciona na lista para ser escrito no arquivo
                    conserto.append(linha_formatada)
                else:
                    # Encontrar o local correto onde a virgula deveria estar e adiciona-la
                    linha_list = list(linha)

                    try:
                        # para cada caractere da linha
                        for localindex, c in enumerate(linha):
                            proximo_caractere = linha_list[localindex + 1]

                            # encontra o local para inserir a virgula (numero seguido de outro numero)
                            if c in numeros and proximo_caractere in numeros:

                                # caso o caractere anterior à nova virgula seja espaço, remove-o
                                if linha_list[localindex - 1] == ' ':
                                    linha_list[localindex - 1] = ''

                                # formata a linha com a virgula
                                linha_list[localindex] = f', {linha_list[localindex]}'
                                linha = ''.join(linha_list)

                                nome = linha.split(",")[0]
                                numero = linha.split(",")[1]
                                numero = re.sub(r'\D', '', numero)

                                linha = nome + f', {numero}'

                                # remove emojis da linha
                                linha_formatada = remover_emojis(linha)

                                # deixa o primeiro caractere do nome maiusculo
                                linha_formatada_list = list(linha_formatada)
                                linha_formatada_list[0] = str(linha_formatada_list[0]).upper()
                                linha_formatada = ''.join(linha_formatada_list)

                                # adiciona à lista que sera escrita
                                conserto.append(linha_formatada)
                                break

                    # caso não haja numero seguido de numero na linha
                    except IndexError:
                        print(f"[X] A linha foi removida: {linha}")
            else:
                print(f"[X] A linha foi removida: {linha} (não há número de telefone)")
            # salva no arquivo a lista de linhas consertadas
            escrever_correcoes(conserto)


def checar_se_ha_numero(linha):
    numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for n in numeros:
        if n in linha:
            return True
        else:
            if n == '9':
                return False


def remover_espacos_desnecessarios(linha) -> str:
    linha_list = list(linha)

    try:
        for i, c in enumerate(linha):
            proximo_caractere = linha_list[i + 1]

            # remover espaços duplos na linha
            if c == ' ' and proximo_caractere == ' ':
                linha_list[i] = ''
                linha = ''.join(linha_list)

        return linha.strip()

    except IndexError:
        return linha.strip()


def remover_emojis(texto) -> str:
    emojis = re.compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # símbolos & pictografias
                        u"\U0001F680-\U0001F6FF"  # transportes & símbolos de mapas
                        u"\U0001F1E0-\U0001F1FF"  # bandeiras (iOS)
                        u"\U00002500-\U00002BEF"  # caracteres chineses comuns
                        u"\U00002702-\U000027B0"  # símbolos diversos
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001f926-\U0001f937"
                        u"\U00010000-\U0010ffff"
                        u"\u200d"
                        u"\u2640-\u2642"
                        u"\u2600-\u2B55"
                        u"\u23cf"
                        u"\u23e9"
                        u"\u231a"
                        u"\ufe0f"  # dingbats
                        u"\u3030"
                        "]+", flags=re.UNICODE)

    return emojis.sub(r'', texto).strip()


def escrever_correcoes(novo: list) -> None:
    with open("numeros2.txt", "w+", encoding="utf8") as arquivo:
        for linha in novo:
            if '\n' in linha:
                arquivo.writelines(linha)
            else:
                arquivo.writelines(linha + '\n')


def ler_lista() -> None:
    print("")
    with open("numeros2.txt", "r+", encoding="utf8") as arquivo:
        linhas = arquivo.readlines()
        edit = linhas.copy()
        arquivo.close()

    for linha in linhas:
        nome = linha.split(",")[0]
        telefone = linha.split(",")[1]

        mensagem = f"{saudacao}, {nome}! Aqui é o(a) (seu nome)!"

        # Mandando mensagem
        e = input(f"[?] Mandar mensagem para {nome}? (S/n): ").upper()
        if e == 'S' or e == '':
            abrir_whatsapp(mensagem, telefone)

        elif e == 'X':
            print("\n[X] Abortando operação. As alterações no arquivo foram salvas.\n")
            escrever_correcoes(edit)
            break

        # Excluindo nome do arquivo
        e = input(f"[?] Excluir {nome} do arquivo? (S/n): ").upper()
        if e == 'S' or e == '':
            edit.remove(linha)

        elif e == 'X':
            print("\n[X] Abortando operação. As alterações no arquivo foram salvas.\n")
            escrever_correcoes(edit)
            break

        print("")

    escrever_correcoes(edit)
    print("[!] Os números acabaram e o arquivo foi atualizado.")
    voltar_ao_menu()


def voltar_ao_menu() -> None:
    e = input('[?] Gostaria de retornar ao menu principal? (s/N): ')
    if e.upper() == 'S':
        limpar_terminal()
        print(user.logo)
        menu()
    else:
        return None


def definir_logo():
    num = random.randint(0, 5)
    if num == 0:
        user.logo = logo.vaca
    elif num == 1:
        user.logo = logo.nova
    elif num == 2:
        user.logo = logo.logo
    elif num == 3:
        user.logo = logo.mymelody
    elif num == 4:
        user.logo = logo.cinnamonroll
    else:
        user.logo = logo.flat


if __name__ == '__main__':
    definir_logo()
    print(user.logo)
    menu()
