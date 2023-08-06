import re

# Fonte para realizar validações

def menuOK(opcao):
    if opcao in (1, 2, 3, 4, 5):
        return True
    else:
        return False


def formatacao(resultado):
    if type(resultado) == int:
        return f'{resultado}'
    else:
        return f'{resultado:.2f}'


def conversor(numero):
    if re.search('.', numero):
        return float(numero)
    else:
        return int(numero)
