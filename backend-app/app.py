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
        print('Diga o nome do funcionário: ')
        audio = r.listen(source)
        try:
            func_nome = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(func_nome))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            func_nome = listenSpeech()

        print('Diga um cargo listado para o funcionário: ')
        cursor.execute(""" SELECT cargos_nome FROM cargos ORDER BY cargos_nome; """)
        for linha in cursor.fetchall():
            print(linha)
        audio = r.listen(source)
        try:
            func_cargo = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(func_cargo))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            func_cargo = listenSpeech()

        print('Diga o salário do funcionário: ')
        audio = r.listen(source)
        try:
            func_salario = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(func_salario))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            func_salario = listenSpeech()

        print('Você confirma esses dados sim ou não ?')
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

    ##print("Vamos cadastrar um novo cargo: ")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        print('Diga o nome do cargo: ')
        audio = r.listen(source)
        try:
            cargo_nome = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(cargo_nome))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            cargo_nome = listenSpeech()

        print('Você confirma esses dados sim ou não ?')
        audio = r.listen(source)
        try:
            confirmacao = r.recognize_google(audio, language='pt-BR')
            print('Você Disse: {0}\n'.format(confirmacao))
        except sr.UnknownValueError:
            print('Não entendi o que você disse, repita por favor.\n')
            confirmacao = listenSpeech()

    if confirmacao == "sim":

        cursor.execute(""" INSERT INTO cargos (cargos_nome) VALUES (?) """, (cargo_nome,))
        conn.commit()
        print('Dados inseridos com sucesso.')
        conn.close()

    else:
        print('Dados não inseridos !')
        return

def functionSwitcher(argument):

    if str(argument).lower() == "cadastrar funcionário":
        inserir_funcionarios()
    elif str(argument).lower() == "cadastrar cargo":
        inserir_cargo()
    elif str(argument).lower() == "desabilitar sara":
        sys.exit()

    ##return "Função Não Implementada\n"


def listenSpeech():

    print("MENU PRINCIPAL SARAH")
    print('_' * 42)
    print('Olá, sou a SARAH, sua assistente de RH!')
    print('_' * 42)
    print('Diga, o que você deseja fazer?')
    print('1 - Cadastrar funcionarios')
    print('2 - Pesquisar funcionario')
    print('3 - Cadastrar Cargo')
    print('4 - Desabilitar SARAH')

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        print('Diga o que você deseja fazer: ')
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
