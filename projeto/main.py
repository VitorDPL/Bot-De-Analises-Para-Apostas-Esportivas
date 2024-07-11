from funcoes import *
from var import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import copy
# def roda_projeto():

def executar_ao_vivo(tempo_rodando):
    melhores_times = extrai_times()

    tempo_que_o_sistema_vai_rodar = tempo_rodando
    entradas_ja_enviadas_para_o_telegram = []

    print(f"TEMPO RODANDO -> {tempo_que_o_sistema_vai_rodar}")

    while tempo_que_o_sistema_vai_rodar > 0:
        try:
            driver = webdriver.Chrome()
            driver.get("https://www.sofascore.com/pt/")
            
            time.sleep(5)
            
            botao_ao_vivo = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div/label[2]/div')
            botao_ao_vivo.click()

            # while not botao_ao_vivo:
            #     botao_ao_vivo = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div/label[2]/div')
            #     botao_ao_vivo.click()

            time.sleep(5)

            clica_em_mostrar_probabilidades = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[3]/label')
            clica_em_mostrar_probabilidades.click()

            time.sleep(5)
            # while not clica_em_mostrar_probabilidades:
            #     clica_em_mostrar_probabilidades = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div/div[1]/div[3]/label')
            #     clica_em_mostrar_probabilidades.click()
            
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
            
            time.sleep(5)

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
                        odd_vitoria_fora = odd_vitoria[2].text.strip() if len(odd_vitoria) > 0 else "Odd's não disponíveis"
                        
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


        entradas_para_enviar = []

        try:
            for item in objetos_times:
                # Cria uma cópia profunda do dicionário atual
                item_copia = copy.deepcopy(item)

                # lógica VITÓRIA do time (MANDANTE ou VISITANTE).
                try:
                    # Verificando se a odd foi capturada
                    if (float(item_copia.get("Odd vitória casa")) and 
                        float(item_copia.get("Odd vitória fora"))):

                        # verifica se o time joga em casa.
                        if item_copia["Casa"] in melhores_times:
                            # verifica se o jogo está empatado.
                            if item_copia["Placar"][0] == item_copia["Placar"][4]:
                                # verifica se a odd é superior a 1.6 e se o time é um bom vencedor jogando em casa
                                try:
                                    if (float(item_copia["Odd vitória casa"]) > 1.6 and
                                        verifica_condicoes(item["Casa"], "Vitória em casa")):
                                        item_copia["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({item_copia['Casa']})"
                                        entradas_para_enviar.append(item_copia)
                                        print(f"Jogo empatado. O {item['Casa']} é bom para vencer em casa e a odd é superior a 1.6.")
            
                                    else:
                                        print(f"O {item['Casa']} não é bom para vencer em casa")
                                except:
                                    pass
                                    
                            # verifica se o time favorito está perdendo em casa.
                            elif item_copia["Placar"][0] < item_copia["Placar"][4]:
                                # verifica se entrar em dupla chance do time é algo coerente.
                                if verifica_condicoes(item["Casa"], "Dupla chance em casa"):
                                    item_copia["Entrada"] = f"DUPLA CHANCE TIME FAVORITO ({item_copia['Casa']})"
                                    entradas_para_enviar.append(item_copia)
                                    print(f"{item['Casa']} perdendo em casa. Opte por entrar na dupla chance do favorito.")
                                else:
                                    print(f"{item['Casa']} está perdendo em casa, mas não é o ideal entrar em um dupla chance no momento.")
                                    
                        # time jogando fora de casa 
                        if item_copia["Fora"] in melhores_times:
                            # verifica se o jogo está empatado.
                            if item_copia["Placar"][0] == item_copia["Placar"][4]:
                                try:
                                    if (float(item_copia["Odd vitória fora"]) > 1.6 and
                                        verifica_condicoes(item["Fora"], "Vitória fora de casa")):
                                        item_copia["Entrada"] = f"VITÓRIA DO TIME FAVORITO ({item_copia['Fora']})"
                                        entradas_para_enviar.append(item_copia)
                                        print(f"{item['Fora']} bom para vencer fora de casa e a odd é superior a 1.6.")
                                except:
                                    pass
                                    
                            elif (item_copia["Placar"][0] > item_copia["Placar"][4] and 
                                verifica_condicoes(item["Fora"], "Dupla chance fora de casa")):
                                    item_copia["Entrada"] = f"DUPLA CHANCE DO TIME FAVORITO ({item_copia['Fora']})"
                                    entradas_para_enviar.append(item_copia)
                                    print(f"{item['Fora']} bom para ao menos empatar fora de casa.")
                            
                
                
                except Exception as e:
                    # Trata qualquer exceção que possa ocorrer
                    print(f"Erro ao processar item: {e}")
        except Exception as e:
            # Trata qualquer exceção que possa ocorrer no loop principal
            print(f"Erro ao processar objetos_times: {e}")


        for item in objetos_times:
            try:
                placar_separado = item["Placar"].split(' - ')
                soma_placar = int(placar_separado[0]) + int(placar_separado[1])

                if (item["Casa"] and verifica_condicoes(item["Casa"], "Over 0.5 gols em casa") or
                item["Fora"] and verifica_condicoes(item["Fora"], "Over 0.5 gols fora") and
                # se o placar for 0 e o tempo for diferente de "INT" e passar dos 62 minutos...
                (soma_placar == 0 and item["Tempo de jogo"].strip("'") != "INT" and int(item["Tempo de jogo"].strip("'")) > 15)):
                    item["Entrada"] = f"Over 0.5 Gols no jogo."
                    entradas_para_enviar.append(item)
                    # deletando a chave de ODDS para não confundir o usuário.
                    del item["Odd vitória casa"]

            except ValueError as e:
                pass    
            
            
        entradas_para_enviar = [dict(t) for t in {tuple(sorted(d.items())) for d in entradas_para_enviar}]
                

        # token gerado pelo próprio bot do telegram
        token = meu_token

        # Nome do canal ou chat_id
        chat_id = meu_chat_id  

        # verifica se a mensagem já foi enviada anteriormente (chama a função send_message dentro)
        verifica_se_a_mensagem_ja_foi_enviada(entradas_para_enviar, entradas_ja_enviadas_para_o_telegram, token, chat_id)

        time.sleep(60)
        tempo_que_o_sistema_vai_rodar -= 60



    # melhor desempenhos: rodando de 1 em 1 minuto durante 5 minutos.