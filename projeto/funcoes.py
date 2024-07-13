import requests
from times import melhores_opcoes

def extrai_times():
    times_extraidos = []
    for campeonato in melhores_opcoes.values():
        for time in campeonato.keys():
            times_extraidos.append(time)
    return times_extraidos

def verifica_condicoes(nome_do_time, entrada):
    for campeonato, times_opcoes in melhores_opcoes.items():
        for time, opcoes in times_opcoes.items():
            if entrada in opcoes and time == nome_do_time:
                print(f"Encontrado: {time} no {campeonato} com a entrada '{entrada}'")
                return True
    return False

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


def verifica_se_a_mensagem_ja_foi_enviada(mensagem_atual, mensagens_enviadas, token, chat_id):
    print("Mensagens enviadas antes:")
    for item in mensagens_enviadas:
        print(item)
    print("-" * 50)

    for mensagem in mensagem_atual:
        foi_enviada = False
        for enviada in mensagens_enviadas:
            if mensagem["Casa"] == enviada["Casa"] and mensagem["Entrada"] == enviada["Entrada"]:
                print(f"Iguais: {mensagem}")
                foi_enviada = True
                break 

        if not foi_enviada:
            print(f"Diferentes: {mensagem}")
            mensagens_enviadas.append(mensagem)
            formatted_message = formata_mensagem([mensagem]) 
            send_message(token, chat_id, formatted_message)
            
    print("Mensagens enviadas após:")
    for item in mensagens_enviadas:
        print(item)
    print("-" * 50)


def verifica_se_dois_times_sao_favoritos(time_casa, time_fora, melhores_times):
    """
    evita que uma entrada de vitória ou dupla chance seja enviada contra um outro time que também é favorito.

    -melhoria: pode ser que um time seja favorito para over gols, mas não para vencer ou ter o dupla chance. O interessante é uma verificação para ver se na linha do time existe a entrada de dupla chance e vitória, caso contrário, essa verificação retorna false.

    chama a verifica condições e pergunta a ela se no time a opção de vitória ou dupla chance estão presentes. Se retornar True, a linha pula para o Over ao invés de vitoria ou dupla chance. (OBS: a função ja retorna True or False por padrão.)
    """
    if time_casa in melhores_times and time_fora in melhores_times:
        return True
    return False

def entrada_vitoria_time_da_casa(objeto_com_todas_as_entradas, item_da_lista_de_objetos, time_casa, lista_de_entradas_para_enviar):

    if (float(objeto_com_todas_as_entradas["Odd vitória casa"]) > 1.6 and
            verifica_condicoes(item_da_lista_de_objetos["Casa"], "Vitória em casa")):
            objeto_com_todas_as_entradas["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({time_casa})"
            lista_de_entradas_para_enviar.append(objeto_com_todas_as_entradas)
            print(f"Jogo empatado. {time_casa} é bom para vencer em casa e a odd é superior a 1.6.")

    else:
        print(f"O {item_da_lista_de_objetos['Casa']} não é bom para vencer em casa")

def entrada_dupla_chance_time_da_casa(objeto_com_todas_as_entradas,item_da_lista_de_objetos, time_casa, lista_de_entradas_para_enviar):
    if verifica_condicoes(item_da_lista_de_objetos["Casa"], "Dupla chance em casa"):
        objeto_com_todas_as_entradas["Entrada"] = f"DUPLA CHANCE TIME FAVORITO ({time_casa})"
        lista_de_entradas_para_enviar.append(objeto_com_todas_as_entradas)
        print(f"{item_da_lista_de_objetos['Casa']} perdendo em casa. Opte por entrar na dupla chance do favorito.")
    else:
        print(f"{item_da_lista_de_objetos['Casa']} está perdendo em casa, mas não é o ideal entrar em um dupla chance no momento.")

def entrada_vitoria_time_fora(objeto_com_todas_as_entradas, item_da_lista_de_objetos, time_fora, lista_de_entradas_para_enviar):
    if (float(objeto_com_todas_as_entradas["Odd vitória fora"]) > 1.6 and
    verifica_condicoes(item_da_lista_de_objetos["Fora"], "Vitória fora de casa")):
        objeto_com_todas_as_entradas["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({time_fora})"
        lista_de_entradas_para_enviar.append(objeto_com_todas_as_entradas)
        print(f"{item_da_lista_de_objetos['Fora']} bom para vencer fora de casa e a odd é superior a 1.6.")
    else:
        print(f"Jogo empatado: {time_fora} é bom para vencer fora de casa e a odd é superior a 1.6.")

def entrada_dupla_chance_time_fora(objeto_com_todas_as_entradas,item_da_lista_de_objetos, time_fora, lista_de_entradas_para_enviar):
    verifica_condicoes(item_da_lista_de_objetos["Fora"], "Dupla chance fora de casa")
    objeto_com_todas_as_entradas["Entrada"] = f"DUPLA CHANCE DO TIME FAVORITO ({time_fora})"
    lista_de_entradas_para_enviar.append(objeto_com_todas_as_entradas)
    print(f"{item_da_lista_de_objetos['Fora']} bom para ao menos empatar fora de casa.")

def entrada_ao_menos_um_gol_no_jogo(item_da_lista_de_objetos, lista_de_entradas_para_enviar):
    placar_separado = item_da_lista_de_objetos["Placar"].split(' - ')
    soma_placar = int(placar_separado[0]) + int(placar_separado[1])

    if (item_da_lista_de_objetos["Casa"] and verifica_condicoes(item_da_lista_de_objetos["Casa"], "Over 0.5 gols em casa") or
        item_da_lista_de_objetos["Fora"] and verifica_condicoes(item_da_lista_de_objetos["Fora"], "Over 0.5 gols fora") and
        # se o placar for 0 e o tempo for diferente de "INT" e passar dos 62 minutos...
        (soma_placar == 0 and item_da_lista_de_objetos["Tempo de jogo"].strip("'") != "INT" and int(item_da_lista_de_objetos["Tempo de jogo"].strip("'")) > 60)):
            item_da_lista_de_objetos["Entrada"] = f"Over 0.5 Gols no jogo."
            lista_de_entradas_para_enviar.append(item_da_lista_de_objetos)