import sys
import os
import inspect
import speech_recognition as sr
import sqlite3
from time import sleep

r = sr.Recognizer()
r.pause_threshold = 1
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)

def inserir_funcionarios():

    ## Realizando a conexão com o banco
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    print('Diga o nome do funcionário que deseja cadastrar.')
    func_nome = listenSpeech()

    print('Diga um cargo listado a baixo em que deseja cadastrar o funcionário.')
    cursor.execute(""" SELECT * FROM cargos ORDER BY 1; """)

    for row in cursor.fetchall():
        print("{0} - {1}".format(row[0], row[1]))
    func_cargo = listenSpeech()

    print('Diga o salário do funcionário.')
    func_salario = listenSpeech()

    confirmacao = ""
    while confirmacao != "sim" and confirmacao != "não":

        print("Nome: {0};\nCargo: {1};\nSalário: {2}\n".format(func_nome, func_cargo, func_salario))
        print('Você confirma esses dados? Sim, ou não?')
        confirmacao = listenSpeech()

        if confirmacao == "sim":

            cursor.execute("""
            INSERT INTO funcionarios (funcionarios_nome, funcionarios_cargo, funcionarios_salario, funcionarios_status)
            VALUES (?,?,?,?)
            """, (func_nome, func_cargo, func_salario, "ativo"))

            conn.commit()
            print('Dados inseridos com sucesso.')
        elif confirmacao == "não":
            print('Dados não inseridos!')
        else:
            print('Por favor, diga apenas sim, ou não.\n')


    conn.close()
    return

def pesquisar_funcionario():
    ## Realizando a conexão com o banco
    conn = sqlite3.connect('database.db')
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    print("MENU DE PESQUISA DE FUNCIONÁRIOS")
    print('_' * 42)
    print('Diga de que forma deseja filtrar sua pesquisa: ')
    print('_' * 42)
    print('1 - Matrícula ')
    print('2 - Nome')
    print('3 - Cargo')
    print('4 - Inativos')

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        print('Diga o filtro desejado: ')
        audio = r.listen(source)
        try:
            filtro = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(filtro))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            filtro = listenSpeech()

    if filtro == "matrícula":

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            print('Diga o numero da matricula: ')
            audio = r.listen(source)
            try:
                matricula = r.recognize_google(audio, language='pt-BR')
                print('Você Disse: {0}\n'.format(matricula))
            except sr.UnknownValueError:
                print('Não entendi o que você disse, repita por favor.\n')
                matricula = listenSpeech()

        sql = str("SELECT * FROM funcionarios WHERE funcionarios_id = " + matricula + ";")
        ##print(sql)
        cursor.execute(sql)
        cabecalho = str("MATRÍCULA NOME                                    CARGO               SALÁRIO   SITUAÇÃO  ")
        print(cabecalho)

        for linha in cursor.fetchall():
            if linha == None:
                break
            else:
                linha = str(linha)
                linha = linha.replace(")", "")
                linha = linha.replace("(", "")
                linha = linha.replace("'", "")
                linha = linha.split(', ')

                #print(linha)

                matricula = len(linha[0])
                nome = len(linha[1])
                cargo = len(linha[2])
                salario = len(linha[3])
                situacao = len(linha[4])

                if matricula < 10:
                    linha[0] = linha[0] + (10-matricula) * " "
                else:
                    linha[0] = linha[0][0:9]
                if nome < 40:
                    linha[1] = linha[1] + (40-nome) * " "
                else:
                    linha[1] = linha[1][0:39]
                if cargo < 20:
                    linha[2] = linha[2] + (20-cargo) * " "
                else:
                    linha[2] = linha[2][0:19]
                if salario < 10:
                    linha[3] = linha[3] + (10-matricula) * " "
                else:
                    linha[3] = linha[3][0:9]
                if situacao < 10:
                    linha[4] = linha[4] + (10-situacao) * " "
                else:
                    linha[4] = linha[4][0:9]

                linha = str(linha[0] + linha[1] + linha[2] + linha[3] + linha[4])
                print(linha)

        conn.close()

    if filtro == "nome":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            print('Diga o nome do funcionário: ')
            audio = r.listen(source)
            try:
                nome = r.recognize_google(audio, language='pt-BR')
                print('Você Disse: {0}\n'.format(nome))
            except sr.UnknownValueError:
                print('Não entendi o que você disse, repita por favor.\n')
                nome = listenSpeech()

        sql = str("SELECT * FROM funcionarios WHERE funcionarios_nome LIKE '%" + nome + "%' ;")
        cursor.execute(sql)
        cabecalho = str("MATRÍCULA NOME                                    CARGO               SALÁRIO   SITUAÇÃO  ")
        print(cabecalho)

        for linha in cursor.fetchall():
            if linha == None:
                break
            else:
                linha = str(linha)
                linha = linha.replace(")", "")
                linha = linha.replace("(", "")
                linha = linha.replace("'", "")
                linha = linha.split(', ')

                # print(linha)

                matricula = len(linha[0])
                nome = len(linha[1])
                cargo = len(linha[2])
                salario = len(linha[3])
                situacao = len(linha[4])

                if matricula < 10:
                    linha[0] = linha[0] + (10 - matricula) * " "
                else:
                    linha[0] = linha[0][0:9]
                if nome < 40:
                    linha[1] = linha[1] + (40 - nome) * " "
                else:
                    linha[1] = linha[1][0:39]
                if cargo < 20:
                    linha[2] = linha[2] + (20 - cargo) * " "
                else:
                    linha[2] = linha[2][0:19]
                if salario < 10:
                    linha[3] = linha[3] + (10 - matricula) * " "
                else:
                    linha[3] = linha[3][0:9]
                if situacao < 10:
                    linha[4] = linha[4] + (10 - situacao) * " "
                else:
                    linha[4] = linha[4][0:9]

                linha = str(linha[0] + linha[1] + linha[2] + linha[3] + linha[4])
                print(linha)

        conn.close()

    if filtro == "cargo":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            print('Diga o cargo: ')
            audio = r.listen(source)
            try:
                cargo = r.recognize_google(audio, language='pt-BR')
                print('Você Disse: {0}\n'.format(cargo))
            except sr.UnknownValueError:
                print('Não entendi o que você disse, repita por favor.\n')
                cargo = listenSpeech()

        sql = str("SELECT * FROM funcionarios WHERE funcionarios_cargo = '" + cargo + "';")
        cursor.execute(sql)
        cabecalho = str("MATRÍCULA NOME                                    CARGO               SALÁRIO   SITUAÇÃO  ")
        print(cabecalho)

        for linha in cursor.fetchall():
            if linha == None:
                break
            else:
                linha = str(linha)
                linha = linha.replace(")", "")
                linha = linha.replace("(", "")
                linha = linha.replace("'", "")
                linha = linha.split(', ')

                # print(linha)

                matricula = len(linha[0])
                nome = len(linha[1])
                cargo = len(linha[2])
                salario = len(linha[3])
                situacao = len(linha[4])

                if matricula < 10:
                    linha[0] = linha[0] + (10 - matricula) * " "
                else:
                    linha[0] = linha[0][0:9]
                if nome < 40:
                    linha[1] = linha[1] + (40 - nome) * " "
                else:
                    linha[1] = linha[1][0:39]
                if cargo < 20:
                    linha[2] = linha[2] + (20 - cargo) * " "
                else:
                    linha[2] = linha[2][0:19]
                if salario < 10:
                    linha[3] = linha[3] + (10 - matricula) * " "
                else:
                    linha[3] = linha[3][0:9]
                if situacao < 10:
                    linha[4] = linha[4] + (10 - situacao) * " "
                else:
                    linha[4] = linha[4][0:9]

                linha = str(linha[0] + linha[1] + linha[2] + linha[3] + linha[4])
                print(linha)

        conn.close()

    if filtro == "inativos":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            print('Diga o numero da matricula do funcionario inativo: ')
            audio = r.listen(source)
            try:
                inativo = r.recognize_google(audio, language='pt-BR')
                print('Você Disse: {0}\n'.format(inativo))
            except sr.UnknownValueError:
                print('Não entendi o que você disse, repita por favor.\n')
                inativo = listenSpeech()

        sql = str("SELECT * FROM funcionarios WHERE funcionarios_id = " + inativo + " AND funcionarios_status = 'inativo' ;")
        cursor.execute(sql)
        cabecalho = str("MATRÍCULA NOME                                    CARGO               SALÁRIO   SITUAÇÃO  ")
        print(cabecalho)

        for linha in cursor.fetchall():
            if linha == None:
                break
            else:
                linha = str(linha)
                linha = linha.replace(")", "")
                linha = linha.replace("(", "")
                linha = linha.replace("'", "")
                linha = linha.split(', ')

                matricula = len(linha[0])
                nome = len(linha[1])
                cargo = len(linha[2])
                salario = len(linha[3])
                situacao = len(linha[4])

                if matricula < 10:
                    linha[0] = linha[0] + (10 - matricula) * " "
                else:
                    linha[0] = linha[0][0:9]
                if nome < 40:
                    linha[1] = linha[1] + (40 - nome) * " "
                else:
                    linha[1] = linha[1][0:39]
                if cargo < 20:
                    linha[2] = linha[2] + (20 - cargo) * " "
                else:
                    linha[2] = linha[2][0:19]
                if salario < 10:
                    linha[3] = linha[3] + (10 - matricula) * " "
                else:
                    linha[3] = linha[3][0:9]
                if situacao < 10:
                    linha[4] = linha[4] + (10 - situacao) * " "
                else:
                    linha[4] = linha[4][0:9]

                linha = str(linha[0] + linha[1] + linha[2] + linha[3] + linha[4])
                print(linha)

        conn.close()

def inserir_cargo():

    ## Realizando a conexão com o banco
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    ##print("Vamos cadastrar um novo cargo: ")

    print('Diga o nome do cargo.')
    cargo_nome = listenSpeech()

    confirmacao = ""
    while confirmacao != "sim" and confirmacao != "não":
        
        print("Cargo: {0}\n".format(cargo_nome))
        print('Você confirma esses dados? Sim, ou não?')
        confirmacao = listenSpeech()

        if confirmacao == "sim":
            cursor.execute(""" INSERT INTO cargos (cargos_nome) VALUES (?) """, (cargo_nome,))
            conn.commit()
            print('Dados inseridos com sucesso.')
        elif confirmacao == "não":
            print('Dados não inseridos!')
        else:
            print('Por favor, diga apenas sim, ou não.\n')
    
    conn.close()
    return

def functionSwitcher(argument):

    if str(argument).lower() == "cadastrar funcionário":
        inserir_funcionarios()
    elif str(argument).lower() == "cadastrar cargo":
        inserir_cargo()
    elif str(argument).lower() == "desabilitar sara":
        sys.exit()
    else:
        print("Função Não Implementada\n")

def main():

    print('MENU PRINCIPAL SARAH')
    print('_' * 42)
    print('Olá, sou a SARAH, sua assistente de RH!')
    print('_' * 42)
    print('Diga, o que você deseja fazer?')
    print('1 - Cadastrar funcionário')
    print('2 - Pesquisar funcionário')
    print('3 - Cadastrar Cargo')
    print('4 - Desabilitar SARAH\n')
    print('Diga o que deseja fazer.')
    command = listenSpeech()

    functionSwitcher(command)

def listenSpeech():

    with sr.Microphone() as source:
        print('Escutando...\n')
        audio = r.listen(source)
        print('Processando...\n')
    try:
        command = r.recognize_google(audio, language='pt-BR')
        print('Você disse: {0}\n'.format(command))
    # loop back to continue to listen for commands if unrecognizable speech
    # is received
    except sr.UnknownValueError:
        print('Não entendi o que você disse, repita por favor.')
        print('Escutando...\n')
        command = listenSpeech()
    
    clear()
    return command

def clear():

    sleep(2)
    if os.name == 'nt': 
        _ = os.system('cls') 
   
    else: 
        _ = os.system('clear')

while True:

    main()
pass
