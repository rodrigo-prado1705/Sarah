import sys
import speech_recognition as sr
import sqlite3

def inserir_funcionarios():
    ## Realizando a conexão com o banco
    conn = sqlite3.connect('database.db')
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        print('Digite o nome do funcionário: ')
        audio = r.listen(source)
        try:
            func_nome = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(func_nome))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            func_nome = listenSpeech()

        print('Digite o cargo do funcionário: ')
        audio = r.listen(source)
        try:
            func_cargo = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(func_cargo))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            func_cargo = listenSpeech()

        print('Digite o salário do funcionário: ')
        audio = r.listen(source)
        try:
            func_salario = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(func_salario))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            func_salario = listenSpeech()

        print('Você confirma esses dados? ')
        audio = r.listen(source)
        try:
            confirmacao = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(confirmacao))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            confirmacao = listenSpeech()

    if confirmacao == "sim":

        status = str("ativo")
        cursor.execute("""
        INSERT INTO funcionarios (funcionarios_nome, funcionarios_cargo, funcionarios_salario, funcionarios_status)
        VALUES (?,?,?,?)
        """, (func_nome, func_cargo, func_salario, status))

        conn.commit()
        print('Dados inseridos com sucesso.')
        conn.close()
    else:
        print('Dados não inseridos !')
        return

def inserir_cargo():
    ## Realizando a conexão com o banco
    conn = sqlite3.connect('database.db')
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    print("Vamos cadastrar um novo cargo: ")
    cargo_nome = input("Digite o cargo: ")
    confirmacao = input("Você confirma esses dados? ")

    if confirmacao == "sim":

        cursor.execute("""INSERT INTO cargos (cargos_nome) VALUES (?) """, (cargo_nome,))

        conn.commit()
        print('Dados inseridos com sucesso.')
        conn.close()
    else:
        print('Dados não inseridos !')
        return

def functionSwitcher(argument):
    switcher = {
        1: "Bom dia",
        2: "Boa tarde",
        3: "Boa noite"
    }

    for key, value in switcher.items():
        if str(argument).lower() == value.lower():
            return key, value
        elif str(argument).lower() == "cadastrar funcionário":
            inserir_funcionarios()
        elif str(argument).lower() == "cadastrar cargo":
            inserir_cargo()
        elif str(argument).lower() == "desabilitar sara":
            sys.exit()

    return "Função Não Implementada\n"


def listenSpeech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        print('Diga Algo: ')
        audio = r.listen(source)
        print('Processando...\n')
    try:
        command = r.recognize_google(audio, language='pt-BR')
        print('Você Disse: {0}\n'.format(command))
    # loop back to continue to listen for commands if unrecognizable speech
    # is received
    except sr.UnknownValueError:
        print('Não entendi o que você disse, repita por favor.\n')
        command = listenSpeech()
    return command


while True:
    answer = listenSpeech()

    print(functionSwitcher(answer))
pass
