import requests

def extrai_times(melhores_opcoes):
    times_extraidos = []
    for campeonato in melhores_opcoes.values():
        for time in campeonato.keys():
            times_extraidos.append(time)
    return times_extraidos

def formata_mensagem(tipo_de_entrada):
    mensagens = ""
    for indice, item in enumerate(tipo_de_entrada):
        if "Odd vitória casa" in item.keys():
            mensagem = (
                f"❗ ENTRE ->APENAS<- se a odd for IGUAL ou SUPERIOR a 1.6 ❗ \n"
                f"👉🏻 ENTRADA: {item['Entrada']}👈🏻\n"
                f"🏠 Time de Casa: {item['Casa']}\n"
                f"⛺️ Time de Fora: {item['Fora']}\n"
                f"🔢 Placar: {item['Placar']}\n"
                f"🕙 Tempo de jogo: {item['Tempo de jogo']}\n"
                f"🔎 Link do jogo: {item['Link do jogo']}\n"
                f"🔥 Odd vitória casa: {item['Odd vitória casa']}\n"
                f"🔥 Odd vitória fora: {item['Odd vitória fora']}\n"
                "-------------------------------------------------------------------------------------------------\n"
            )
        else:
            mensagem = (
                f"❗ ENTRE ->APENAS<- se a odd for IGUAL ou SUPERIOR a 1.6 ❗ \n"
                f"👉🏻 ENTRADA: {item['Entrada']}👈🏻\n"
                f"🏠 Time de Casa: {item['Casa']}\n"
                f"⛺️ Time de Fora: {item['Fora']}\n"
                f"🔢 Placar: {item['Placar']}\n"
                f"🕙 Tempo de jogo: {item['Tempo de jogo']}\n"
                f"🔎 Link do jogo: {item['Link do jogo']}\n"
                "-------------------------------------------------------------------------------------------------\n"
            )
        mensagens += mensagem
    return mensagens


def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message}
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.post(url, data)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso!")
        else:
            print(f'Erro ao enviar mensagem, código de status: {response.status_code}')
    except Exception as e:
        print("Erro no sendMessage:", e)