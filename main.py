from projeto.funcoes import *
from projeto.times import *
from projeto.var import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import copy

melhores_times = extrai_times(melhores_opcoes)

# print(melhores_times)

try:
    driver = webdriver.Chrome()
    driver.get("https://www.sofascore.com/pt/")
    
    # time.sleep(1.5)
    
    botao_ao_vivo = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div/label[2]/div')
    botao_ao_vivo.click()

    while not botao_ao_vivo:
        botao_ao_vivo = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div/label[2]/div')
        botao_ao_vivo.click()

    clica_em_mostrar_probabilidades = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[3]/label')
    clica_em_mostrar_probabilidades.click()

    while not clica_em_mostrar_probabilidades:
        clica_em_mostrar_probabilidades = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[3]/label')
        clica_em_mostrar_probabilidades.click()
    
except Exception as e:
    print("Não foi possível executar o Chrome Driver")

try:
    # Captura o conteúdo HTML da página carregada pelo Selenium
    html = driver.page_source
    
    # Parseia o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Encontra todos os jogos usando BeautifulSoup
    jogos = soup.find_all('div', class_='Box klGMtt')
except Exception as e:
    print("Erro ao efetuar a captura do conteúdo:", e)


try:
    objetos_times = []
    
    # Itera sobre os jogos encontrados e imprime os textos dos times de casa e fora
    for jogo in jogos:
        # Encontra todos os elementos <bdi> com a classe específica
        times = jogo.find_all('bdi', class_='Text ldkigH')
        
        placar_elementos = jogo.find_all('span', class_='Text cvwZXc currentScore')
        
        # Encontra o elemento <a> com o atributo data-id específico dentro do jogo atual
        tag_a = jogo.find('a', {'data-id': True})

        # odd's para a vitória dos times
        odd_vitoria = jogo.find_all('span', class_='Text gclYTO')

        # tempo de jogo
        tempo_de_jogo = jogo.find_all('bdi', class_='Text ipsxwz')

        if len(times) == 2 and len(placar_elementos) >= 2:
            time_casa = times[0].text.strip()
            time_fora = times[1].text.strip()

            # Verifica se o time de casa ou fora está nas "melhores opções"
            if any(time_casa in opcoes for opcoes in melhores_times) or any(time_fora in opcoes for opcoes in melhores_times):
                # Obtém os placares
                placar_casa = placar_elementos[0].text.strip()
                placar_fora = placar_elementos[1].text.strip()

                print(f'Time de Casa: {time_casa}')
                print(f'Time de Fora: {time_fora}')
                print(f'Placar: {placar_casa} - {placar_fora}')
                print(f'Tempo de jogo: {tempo_de_jogo[0].text}')
                
                if tag_a:
                    link_jogo = f"https://www.sofascore.com{tag_a['href']}"
                    print(f"Link do jogo: {link_jogo}")
                
                odd_vitoria_casa = odd_vitoria[0].text.strip() if len(odd_vitoria) > 0 else "Odd's não disponíveis"
                odd_vitoria_fora = odd_vitoria[2].text.strip() if len(odd_vitoria) > 2 else "Odd's não disponíveis"
                
                print(f"Odd vitória casa: {odd_vitoria_casa}")
                print(f"Odd vitória fora: {odd_vitoria_fora}")

                # Adiciona ao dicionário
                objetos_times.append({
                    "Entrada" : "null",
                    "Casa": time_casa,
                    "Fora": time_fora,
                    "Placar": f"{placar_casa} - {placar_fora}",
                    "Link do jogo": link_jogo,
                    "Odd vitória casa": odd_vitoria_casa,
                    "Odd vitória fora": odd_vitoria_fora,
                    "Tempo de jogo": tempo_de_jogo[0].text if tempo_de_jogo else 'N/A'
                })

                print('-'*130)

except Exception as e:
    print("Ocorreu um erro ao acessar os jogos:", e)

finally:
    driver.quit()


entradas_enviadas = []

try:
    for item in objetos_times:
        # Cria uma cópia profunda do dicionário atual
        item_copia = copy.deepcopy(item)
        
        try:
            # Verifica se as odd's estão disponíveis
            if float(item_copia.get("Odd vitória casa")) and float(item_copia.get("Odd vitória fora")):
                # Verifica se o time de casa é o favorito
                if item_copia["Casa"] in melhores_times:
                    if item_copia["Placar"][0] == item_copia["Placar"][4] and float(item_copia["Odd vitória casa"]) > 1.6:
                        item_copia["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({item_copia['Casa']})"
                        entradas_enviadas.append(item_copia)
                    elif item_copia["Placar"][0] < item_copia["Placar"][4]:
                        item_copia["Entrada"] = f"DUPLA CHANCE TIME FAVORITO ({item_copia['Casa']})"
                        entradas_enviadas.append(item_copia)
                        
                elif item_copia["Fora"] in melhores_times:
                    if item_copia["Placar"][4] == item_copia["Placar"][0] and float(item_copia["Odd vitória fora"]) > 1.6:
                        item_copia["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({item_copia['Fora']})"
                        entradas_enviadas.append(item_copia)
                    elif item_copia["Placar"][4] < item_copia["Placar"][0]:
                        item_copia["Entrada"] = f"DUPLA CHANCE TIME FAVORITO ({item_copia['Fora']})"
                        entradas_enviadas.append(item_copia)
        except ValueError as e:
            pass
            
        else:
            try:
                if item_copia["Casa"] in melhores_times and item_copia["Tempo de jogo"].strip("'") != "INT" and int(item_copia["Tempo de jogo"].strip("'")) > 50:
                    if item_copia["Placar"][0] == item_copia["Placar"][4]:
                        item_copia["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({item_copia['Casa']})"
                        entradas_enviadas.append(item_copia)
                    elif item_copia["Placar"][0] < item_copia["Placar"][4]:
                        item_copia["Entrada"] = f"DUPLA CHANCE TIME FAVORITO ({item_copia['Casa']})"
                        entradas_enviadas.append(item_copia)
                        
                elif item_copia["Fora"] in melhores_times and item_copia["Tempo de jogo"].strip("'") != "INT" and int(item_copia["Tempo de jogo"].strip("'")) > 50:
                    if item_copia["Placar"][4] == item_copia["Placar"][0]:
                        item_copia["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({item_copia['Fora']})"
                        entradas_enviadas.append(item_copia)
                    elif item_copia["Placar"][4] < item_copia["Placar"][0]:
                        item_copia["Entrada"] = f"DUPLA CHANCE TIME FAVORITO ({item_copia['Fora']})"
                        entradas_enviadas.append(item_copia)
            except ValueError as e:
                pass
except ValueError as e:
    print("Erro", e)
    pass

entradas_enviadas = [dict(t) for t in {tuple(sorted(d.items())) for d in entradas_enviadas}]

for item in objetos_times:
    placar_separado = item["Placar"].split(' - ')
    soma_placar = int(placar_separado[0]) + int(placar_separado[1])
    # print(f"{placar_separado[0]} - {placar_separado[1]}")

    item_copia_over = copy.deepcopy(item)
    
    try:
        # se o placar for 0 e o tempo for diferente de "INT" e passar dos 62 minutos...
        if(soma_placar == 0 and item["Tempo de jogo"].strip("'") != "INT" and int(item["Tempo de jogo"].strip("'")) > 50):
            item_copia_over["Entrada"] = f"Over 0.5 Gols no jogo (OBS -> Odd's para OVER 0.5 INDISPONÍVEIS. Entre apenas se for superior ou igual a 1.6"
            entradas_enviadas.append(item_copia_over)
            # deletando a chave de ODDS para não confundir o usuário.
            del item_copia_over["Odd vitória casa"]
            # print(entradas_enviadas)
    except ValueError as e:
        print("Erro ao converter o placar para um número inteiro.")
        pass
    
        

# token gerado pelo próprio bot do telegram
token = meu_token

# Nome do canal ou chat_id
chat_id = meu_chat_id  

# Envia a mensagem para o grupo
send_message(token, chat_id, formata_mensagem(entradas_enviadas))
