import psutil

class User:
    def __init__(self):
        self.session_logo = ''
        self.username = ''
        self.prefix = 55
        self.greetings_manual = ''
        self.greetings_auto = ''
        
        try:
            self.bateria = psutil.sensors_battery()
        except Exception:
            print("[!] Aviso: não foi possível encontrar uma bateria no computador. Portanto, a automação funcionará de forma rápida. Se estiver rodando o script em um computador, não preocupe-se.")
            self.bateria = False

