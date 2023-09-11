import os

def limpar() -> None:
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')
