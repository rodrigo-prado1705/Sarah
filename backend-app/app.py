import sys
import os
import inspect
import speech_recognition as sr
import sqlite3
from sugestao import sugestao
from time import sleep

r = sr.Recognizer()
r.pause_threshold = 0.5


##### ENVIAR PARA ARQUIVO functions_database
def inserir_funcionarios():

    ## Realizando a conexão com o banco
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    print('Diga o nome do funcionário que deseja cadastrar.')
    func_nome = listenSpeech()

    print('Diga um cargo listado a baixo em que deseja cadastrar o funcionário.')
    cursor.execute(""" SELECT * FROM cargos ORDER BY cargos_nome; """)

    for linha in cursor.fetchall():
        print("{0} - {1}".format(linha[0], linha[1]))
    voz_cargo = listenSpeech()

    sql = str(" SELECT cargos_id, cargos_nome FROM cargos WHERE cargos_nome = '"+ voz_cargo +"';")
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == "":
        print("Cargo não encontrado!\n Cadastre o cargo primeiro!")
        print("Deseja Cadastrar um novo cargo?")
        confim = listenSpeech()

        if confim == "sim":
            inserir_cargo()
        else:
            main()
    else:
        func_cargo = result[0]
        func_cargo_desc = func_cargo[1]
        func_cargo = int(func_cargo[0])

        print('Diga o salário do funcionário.')
        func_salario = listenSpeech()

        confirmacao = ""
        while confirmacao != "sim" and confirmacao != "não":

            print("Nome: {0};\nCargo: {1};\nSalário: {2}\n".format(func_nome, func_cargo_desc, func_salario))
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
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
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
    print('5 - Todos')

    print('Diga o filtro desejado.')
    filtro = listenSpeech()

    if filtro == "matrícula":

        print('Diga o numero da matricula: ')
        matricula = listenSpeech()

        sql = str("SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
                  "FROM funcionarios "
                  "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
                  "WHERE funcionarios_id = " + matricula + " ORDER BY funcionarios_id;")
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

                linha = FormatacaoString(linha)
                print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4] + "\n")
                
        conn.close()

        print('_' * 42)
        print("Caso queira editar algum dos registros, diga 'Selecionar <número da matricula>';")
        print("Caso queira demitir um funcionário, diga 'Demitir <número da matricula>';")
        print("Caso queira voltar ao menu principal, diga 'Voltar'.")

        continuar = ""
        while continuar != "voltar" and continuar.split(" ")[0] != "selecionar":
            continuar = listenSpeechNoClear()

            if continuar == "voltar":
                main()
            elif continuar.split(" ")[0] == "selecionar":
                edit_funcionario(continuar.split(" ")[1])
            elif continuar.split(" ")[0] == "demitir":
                demitir_funcionario(continuar.split(" ")[1])

    elif filtro == "nome":
        print('Diga o nome do funcionário.')
        nome = listenSpeech()

        sql = str(
            "SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
            "FROM funcionarios "
            "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
            "WHERE funcionarios_nome LIKE '%" + nome + "%' ORDER BY funcionarios_nome;")
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

                linha = FormatacaoString(linha)
                print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4] + "\n")

        conn.close()

        print('_' * 42)
        print("Caso queira editar algum dos registros, diga 'Selecionar <número da matricula>';")
        print("Caso queira demitir um funcionário, diga 'Demitir <número da matricula>';")
        print("Caso queira voltar ao menu principal, diga 'Voltar'.")

        continuar = ""
        while continuar != "voltar" and continuar.split(" ")[0] != "selecionar":
            continuar = listenSpeechNoClear()

            if continuar == "voltar":
                main()
            elif continuar.split(" ")[0] == "selecionar":
                edit_funcionario(continuar.split(" ")[1])
            elif continuar.split(" ")[0] == "demitir":
                demitir_funcionario(continuar.split(" ")[1])

    elif filtro == "cargo":
        print('Diga o cargo.')
        voz_cargo = listenSpeech()

        sql = str(" SELECT cargos_id, cargos_nome FROM cargos WHERE cargos_nome = '" + voz_cargo + "';")
        cursor.execute(sql)
        result = cursor.fetchall()
        func_cargo = result[0]
        func_cargo_desc = func_cargo[1]
        func_cargo = str(func_cargo[0])

        sql = str(
            "SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
            "FROM funcionarios "
            "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
            "WHERE funcionarios_cargo = '" + func_cargo + "' ORDER BY funcionarios_nome;")

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

                linha = FormatacaoString(linha)
                print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4])

        conn.close()

        print('_' * 42)
        print("Caso queira editar algum dos registros, diga 'Selecionar <número da matricula>';")
        print("Caso queira demitir um funcionário, diga 'Demitir <número da matricula>';")
        print("Caso queira voltar ao menu principal, diga 'Voltar'.")

        continuar = ""
        while continuar != "voltar" and continuar.split(" ")[0] != "selecionar":
            continuar = listenSpeechNoClear()

            if continuar == "voltar":
                main()
            elif continuar.split(" ")[0] == "selecionar":
                edit_funcionario(continuar.split(" ")[1])
            elif continuar.split(" ")[0] == "demitir":
                demitir_funcionario(continuar.split(" ")[1])

    elif filtro == "inativos":
        sql = str(
            "SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
            "FROM funcionarios "
            "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
            "WHERE funcionarios_status = 'inativo' ORDER BY funcionarios_id;")

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

                linha = FormatacaoString(linha)
                print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4] + "\n")

        conn.close()

        print('_' * 42)
        print("Caso queira ativar algum dos registros, diga 'Ativar <número da matricula>';")
        print("Caso queira voltar ao menu principal, diga 'Voltar'.")

        continuar = ""
        while continuar != "voltar" and continuar.split(" ")[0] != "selecionar":
            continuar = listenSpeechNoClear()

            if continuar == "voltar":
                main()
            elif continuar.split(" ")[0] == "ativar":
                ativar_funcionario(continuar.split(" ")[1])

    elif filtro == "todos":
        sql = str(
            "SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
            "FROM funcionarios "
            "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
            "WHERE funcionarios_status != 'inativo' ORDER BY funcionarios_nome;")
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

                linha = FormatacaoString(linha)
                print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4])

        conn.close()

        print('_' * 42)
        print("Caso queira editar algum dos registros, diga 'Selecionar <número da matricula>';")
        print("Caso queira demitir um funcionário, diga 'Demitir <número da matricula>';")
        print("Caso queira voltar ao menu principal, diga 'Voltar'.")

        continuar = ""
        while continuar != "voltar" and continuar.split(" ")[0] != "selecionar":
            continuar = listenSpeechNoClear()

            if continuar == "voltar":
                main()
            elif continuar.split(" ")[0] == "selecionar":
                edit_funcionario(continuar.split(" ")[1])
            elif continuar.split(" ")[0] == "demitir":
                demitir_funcionario(continuar.split(" ")[1])

    else:
        pesquisar_funcionario()

def edit_funcionario(matricula):

    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    cursor = conn.cursor()

    clear()

    sql = str(
        "SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
        "FROM funcionarios "
        "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
        "WHERE funcionarios_id = " + matricula + ";")
    cursor.execute(sql)

    cabecalho = "Formulário de alteração de dados do funcionário\n" + '_' * 42 \
    + "\nMATRÍCULA NOME                                    CARGO               SALÁRIO   SITUAÇÃO"

    for linha in cursor.fetchall():
        if linha == None:
            break
        else:
            linha = str(linha)
            linha = linha.replace(")", "")
            linha = linha.replace("(", "")
            linha = linha.replace("'", "")
            linha = linha.split(', ')

            linha = FormatacaoString(linha)

            confirmacaoRegistro = ""
            confirmacao = ""
            func_nome = ""
            func_cargo = ""
            func_salario = ""

            while confirmacao != "sim" and confirmacao != "não":
                print(cabecalho)
                print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4] + "\n")
                confirmacaoRegistro = ""
                confirmacao = ""

                print('Deseja alterar o nome do funcionário? (Sim ou Não)')
                confirmacao = listenSpeechNoClear()
                if confirmacao == "sim":
                    while confirmacaoRegistro != "sim":
                        print("Diga o novo nome do funcionário: ")
                        func_nome = str(listenSpeechNoClear())
                        print('Confirma a atualização?')
                        confirmacaoRegistro = listenSpeech()
                elif confirmacao == "não":
                    func_nome = str(linha[1]).strip()
            
            confirmacaoRegistro = ""
            confirmacao = ""
            linha[1] = func_nome
            linha = FormatacaoString(linha)

            while confirmacao != "sim" and confirmacao != "não":
                print(cabecalho)
                print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4])
                confirmacaoRegistro = ""
                confirmacao = ""

                print('Deseja trocar o cargo do funcionário? (Sim ou Não)')
                confirmacao = listenSpeechNoClear()
                if confirmacao == "sim":
                    cursor.execute(""" SELECT * FROM cargos ORDER BY cargos_nome; """)
                    for linhaCargo in cursor.fetchall():
                        print("{0} - {1}".format(linhaCargo[0], linhaCargo[1]))
                    while confirmacaoRegistro != "sim":
                        print("Diga o novo cargo do funcionário: ")
                        voz_cargo = str(listenSpeech())

                        sql = str(" SELECT cargos_id, cargos_nome FROM cargos WHERE cargos_nome = '" + voz_cargo.title() + "';")
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        func_cargo = result[0]
                        func_cargo_desc = func_cargo[1]
                        func_cargo = str(func_cargo[0])

                        print('Confirma a atualização?')
                        confirmacaoRegistro = listenSpeech()
                elif confirmacao == "não":
                    func_cargo = str(linha[5]).strip()

            confirmacaoRegistro = ""
            confirmacao = ""
            linha[2] = func_cargo
            linha = FormatacaoString(linha)

            while confirmacao != "sim" and confirmacao != "não":
                print(cabecalho)
                print(str(linha[0]) + linha[1] + func_cargo_desc + str(linha[3]) + linha[4])
                confirmacaoRegistro = ""
                confirmacao = ""

                print('Deseja alterar o salário do funcionário? (Sim ou Não)')
                confirmacao = listenSpeechNoClear()
                if confirmacao == "sim":
                    while confirmacaoRegistro != "sim":
                        print("Diga o novo salário do funcionário: ")
                        func_salario = str(listenSpeech())
                        print('Confirma a atualização?')
                        confirmacaoRegistro = listenSpeech()
                elif confirmacao == "não":
                    func_salario = str(linha[3]).strip()

            sql = """
            UPDATE funcionarios SET
            funcionarios_nome = '""" + func_nome + """',
            funcionarios_cargo = '""" + func_cargo + """',
            funcionarios_salario = '""" + func_salario + """'   
            WHERE funcionarios_id = """ + str(linha[0]).strip() + ""
            cursor.execute(sql)
            conn.commit()

            print('Dados atualizados com sucesso.')

        conn.close()

def demitir_funcionario(matricula):
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    cursor = conn.cursor()

    clear()

    sql = str(
        "SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
        "FROM funcionarios "
        "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
        "WHERE funcionarios_id = " + matricula + ";")
    cursor.execute(sql)

    cabecalho = "Formulário de alteração de dados do funcionário\n" + '_' * 42 \
                + "\nMATRÍCULA NOME                                    CARGO               SALÁRIO   SITUAÇÃO"
    confirmacao = ""

    for linha in cursor.fetchall():
        if linha == None:
            break
        else:
            linha = str(linha)
            linha = linha.replace(")", "")
            linha = linha.replace("(", "")
            linha = linha.replace("'", "")
            linha = linha.split(', ')

            linha = FormatacaoString(linha)
            print(cabecalho)
            print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4] + "\n")

            print("Confirma a demissão do funcionário selecionado? (Sim ou Não)")
            confirmacao = listenSpeechNoClear()
            if confirmacao == "sim":
                sql = """
                UPDATE funcionarios SET
                funcionarios_status = 'inativo'
                WHERE funcionarios_id = """ + matricula + ""
                cursor.execute(sql)
                conn.commit()

    print('Funcionário demitido com sucesso !')
    pesquisar_funcionario()

    conn.close()

def ativar_funcionario(matricula):
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    cursor = conn.cursor()

    clear()
    sql = str(
        "SELECT funcionarios_id, funcionarios_Nome, funcionarios_cargo, funcionarios_salario, funcionarios_status, cargos_nome "
        "FROM funcionarios "
        "INNER JOIN cargos ON funcionarios.funcionarios_cargo = cargos.cargos_id "
        "WHERE funcionarios_id = " + matricula + ";")
    cursor.execute(sql)

    cabecalho = "Formulário de alteração de dados do funcionário\n" + '_' * 42 \
                + "\nMATRÍCULA NOME                                    CARGO               SALÁRIO   SITUAÇÃO"
    confirmacao = ""

    for linha in cursor.fetchall():
        if linha == None:
            break
        else:
            linha = str(linha)
            linha = linha.replace(")", "")
            linha = linha.replace("(", "")
            linha = linha.replace("'", "")
            linha = linha.split(', ')

            linha = FormatacaoString(linha)
            print(cabecalho)
            print(str(linha[0]) + linha[1] + linha[5] + str(linha[3]) + linha[4] + "\n")

            print("Deseja reativar o funcionário selecionado? (Sim ou Não)")
            confirmacao = listenSpeechNoClear()
            if confirmacao == "sim":
                sql = """
                UPDATE funcionarios SET
                funcionarios_status = 'ativo'
                WHERE funcionarios_id = """ + matricula + ""
                cursor.execute(sql)
                conn.commit()

    print('Funcionário ativado com sucesso !')
    pesquisar_funcionario()

    conn.close()

def inserir_cargo():

    ## Realizando a conexão com o banco
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    print('Diga o nome do cargo.')
    cargo_nome = listenSpeech()

    cursor.execute(""" SELECT cargos_nome FROM cargos WHERE cargos_nome LIKE '%""" + cargo_nome + """%'; """)
    if len(cursor.fetchall()) != 0:
        print("Cargo ja cadastrado no Sistema !\n")
        inserir_cargo()
    else:
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

def pesquisar_cargo():
    ## Realizando a conexão com o banco
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    print("MENU DE PESQUISA DE CARGOS")
    print('_' * 42)

    sql = str("SELECT cargos_id, cargos_nome FROM cargos ORDER BY cargos_nome;")
    cursor.execute(sql)
    cabecalho = str("CÓDIGO  CARGO          ")
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

            codigo = len(str(linha[0]))
            cargo = len(linha[1])

            if codigo < 8:
                linha[0] = str(linha[0]) + (8 - codigo) * " "
            else:
                linha[0] = linha[0][0:8]
            if cargo < 15:
                linha[1] = linha[1] + (15 - cargo) * " "
            else:
                linha[1] = linha[1][0:15]

            linha = str(str(linha[0]) + linha[1])
            print(linha)

    conn.close()

    print('_' * 42)
    print("Caso queira editar algum dos registros, diga 'Alterar <número da código>';")
    print("Caso queira deletar algum dos registros, diga 'Deletar <número da código>';")
    print("Caso queira voltar ao menu principal, diga 'Voltar'.")

    continuar = ""
    while continuar != "voltar" and continuar.split(" ")[0] != "alterar":
        continuar = listenSpeechNoClear()

        if continuar == "voltar":
            main()
        elif continuar.split(" ")[0] == "alterar":
            edit_cargo(continuar.split(" ")[1])
        elif continuar.split(" ")[0] == "deletar":
            deletar_cargo(continuar.split(" ")[1])

def edit_cargo(codigo):
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    cursor = conn.cursor()

    sql = str("SELECT * FROM cargos WHERE cargos_id = " + codigo + ";")
    cursor.execute(sql)

    cabecalho = "Formulário de alteração de Cargo\n" + '_' * 42 \
                + "\nCÓDIGO  CARGO          "

    for linha in cursor.fetchall():
        if linha == None:
            break
        else:
            linha = str(linha)
            linha = linha.replace(")", "")
            linha = linha.replace("(", "")
            linha = linha.replace("'", "")
            linha = linha.split(', ')

            codigo = len(str(linha[0]))
            cargo = len(linha[1])

            if codigo < 8:
                linha[0] = str(linha[0]) + (8 - codigo) * " "
            else:
                linha[0] = linha[0][0:8]
            if cargo < 15:
                linha[1] = linha[1] + (15 - cargo) * " "
            else:
                linha[1] = linha[1][0:15]

            confirmacaoRegistro = ""
            confirmacao = ""
            cargo_nome = ""

            while confirmacao != "sim" and confirmacao != "não":
                print(cabecalho)
                print(str(linha[0]) + linha[1]+"\n")
                confirmacaoRegistro = ""
                confirmacao = ""

                print('Deseja alterar cargo? (Sim ou Não)')
                confirmacao = listenSpeechNoClear()
                if confirmacao == "sim":
                    while confirmacaoRegistro != "sim":
                        print("Diga o novo nome do cargo: ")
                        cargo_nome = str(listenSpeechNoClear())
                        print('Confirma a atualização? (Sim ou Não)')
                        confirmacaoRegistro = listenSpeech()
                elif confirmacao == "não":
                    cargo_nome = str(linha[1]).strip()

            sql = """
            UPDATE cargos SET
            cargos_nome = '""" + cargo_nome + """' 
            WHERE cargos_id = """ + str(linha[0]).strip() + ""
            cursor.execute(sql)
            conn.commit()

            print('Dados atualizados com sucesso.')
            sleep(2)

        conn.close()

def deletar_cargo(codigo):
    ## Realizando a conexão com o banco
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), 'database.db'))
    ## Criando um cursor, utilizado para executar as funções do banco
    cursor = conn.cursor()

    print("Atenção ao concordar com a exclusão os dados não poderam ser recuperados.")
    print("Deseja mesmo deletar este cargo? (Sim ou Não)")
    confirmacao = listenSpeechNoClear()
    if confirmacao == "sim":

        cursor.execute("""
        DELETE FROM cargos
        WHERE cargos_id = ?
        """, (codigo,))

        conn.commit()

        print("Cargo deletado com sucesso !")
        pesquisar_cargo()
    else:
        pesquisar_cargo()
##############################################

def functionSwitcher(argument):

    if str(argument).lower() == "cadastrar funcionário":
        inserir_funcionarios()
    elif str(argument).lower() == "pesquisar funcionário":
        pesquisar_funcionario()
    elif str(argument).lower() == "cadastrar cargo":
        inserir_cargo()
    elif str(argument).lower() == "pesquisar cargo":
        pesquisar_cargo()
    elif str(argument).lower() == "sugerir filme":
        sugestao()
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
    print('4 - Pesquisar Cargo')
    print('5 - Sugerir Filme')
    print('6 - Desabilitar SARAH\n')

    print('Diga o que deseja fazer:')
    command = listenSpeech()

    functionSwitcher(command)

def listenSpeech():

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)

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
        command = listenSpeech()

    if command == "voltar":
        sleep(2)
        clear()
        main()
    
    clear()
    return command

def listenSpeechNoClear():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)

    with sr.Microphone() as source:
        print('Escutando...  \r')
        audio = r.listen(source)
        print('Processando...\r')
    try:
        command = r.recognize_google(audio, language='pt-BR')
    # loop back to continue to listen for commands if unrecognizable speech
    # is received
    except sr.UnknownValueError:
        command = listenSpeechNoClear()
    
    if command == "voltar":
        print('Você disse: {0}\n'.format(command))
        sleep(2)
        clear()
        main()

    return command

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

while True:

    main()
pass
