import requests
from time import sleep

def sugestao():
    sugestao = requests.get('http://topicos-avancados.herokuapp.com/getFilme/9')

    sugestao = sugestao.json()

    sugestao = sugestao.get('filme')

    print("A sugestão do filme de hoje é: " + sugestao + "\n")
    sleep(2)
