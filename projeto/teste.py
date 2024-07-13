from funcoes import *
from var import *

mensagem_enviada = [
    {
        "Entrada": "Vitória Bayern",
        "Casa": "Bayern",
        "Fora": "Wolfsburg",
        "Placar": "0 - 0",
        "Link do jogo": "null",
        "Odd vitória casa": 2.10,
        "Odd vitória fora": 2.0,
        "Tempo de jogo": 75
    }
]

# Exemplo de uso
entradas_para_enviar = [
    {
        "Entrada": "Vitória Bayern",
        "Casa": "Bayern",
        "Fora": "Wolfsburg",
        "Placar": "0 - 0",
        "Link do jogo": "null",
        "Odd vitória casa": 2.10,
        "Odd vitória fora": 2.0,
        "Tempo de jogo": 75
    },
    {
        "Entrada": "Dupla chance Vasco",
        "Casa": "Vasco",
        "Fora": "São Paulo",
        "Placar": "0 - 1",
        "Link do jogo": "null",
        "Odd vitória casa": 2.10,
        "Odd vitória fora": 2.0,
        "Tempo de jogo": 75
    },
    {
        "Entrada": "Vitória Manchester City",
        "Casa": "Manchester City",
        "Fora": "Wolves",
        "Placar": "0 - 0",
        "Link do jogo": "null",
        "Odd vitória casa": 2.10,
        "Odd vitória fora": 2.0,
        "Tempo de jogo": 75
    }
]

# token gerado pelo próprio bot do telegram
token = meu_token

# Nome do canal ou chat_id
chat_id = meu_chat_id  

# verifica se a mensagem já foi enviada anteriormente (chama a função send_message dentro)
verifica_se_a_mensagem_ja_foi_enviada(entradas_para_enviar, mensagem_enviada, token, chat_id)