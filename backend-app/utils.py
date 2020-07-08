import os
from time import sleep

def clear():

    sleep(2)
    if os.name == 'nt': 
        _ = os.system('cls') 
   
    else: 
        _ = os.system('clear')

def FormatacaoString(linha):

    matricula = len(str(linha[0]))
    nome = len(linha[1])
    cargo = len(linha[5])
    salario = len(str(linha[3]))
    situacao = len(linha[4])

    if matricula < 10:
        linha[0] = str(linha[0]) + (10 - matricula) * " "
    else:
        linha[0] = linha[0][0:10]
    if nome < 40:
        linha[1] = linha[1] + (40 - nome) * " "
    else:
        linha[1] = linha[1][0:40]
    if cargo < 20:
        linha[5] = linha[5] + (20 - cargo) * " "
    else:
        linha[5] = linha[5][0:20]
    if salario < 10:
        linha[3] = str(linha[3]) + (10 - matricula) * " "
    else:
        linha[3] = linha[3][0:10]
    if situacao < 10:
        linha[4] = linha[4] + (10 - situacao) * " "
    else:
        linha[4] = linha[4][0:10]

    return linha