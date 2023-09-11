import pyautogui
import webbrowser
from urllib.parse import quote
import time


def abrir_whatsapp(msg, user, num=None) -> None:
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
    
    if user.bateria:
        if user.bateria.percent <= 20:
            bateria_fraca = True


    # definir o tempo de espera conforme a bateria
    if bateria_fraca:
        time.sleep(2.1)
    else:
        time.sleep(1.4)

    r, g, b = pyautogui.pixel(centro_x, centro_y - 180)

    # clicando no botao de iniciar conversa
    if r == 18 and g == 140 and b == 126:
        pyautogui.click()
        pyautogui.moveTo(centro_x, centro_y - 120)

    if bateria_fraca:
        time.sleep(1.8)
    else:
        time.sleep(1.1)

    pyautogui.click()