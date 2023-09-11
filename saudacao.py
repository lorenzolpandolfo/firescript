import datetime

def definir_saudacao_momentanea() -> str:
    agora = datetime.datetime.now()
    meio_dia = agora.replace(hour=12, minute=0)
    seis_horas = agora.replace(hour=18, minute=0)

    if agora < meio_dia:
        return "Bom dia"

    elif meio_dia <= agora < seis_horas:
        return "Boa tarde"

    else:
        return "Boa noite"
