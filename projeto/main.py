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

                time_casa = item_copia["Casa"]
                time_fora = item_copia["Fora"]

                placar_time_casa = item_copia["Placar"][0]
                placar_time_fora = item_copia["Placar"][4]

                tempo_de_jogo = item_copia["Tempo de jogo"]
    
                # lógica VITÓRIA do time (MANDANTE ou VISITANTE).
                try:
                    if not verifica_se_dois_times_sao_favoritos(time_casa= time_casa, time_fora= time_fora, melhores_times= melhores_times):
                        # Verificando se a odd foi capturada
                        if (float(item_copia.get("Odd vitória casa")) and 
                            float(item_copia.get("Odd vitória fora"))):

                            # verifica se o time joga em casa.
                            if time_casa in melhores_times:
                                # verifica se o jogo está empatado.
                                if placar_time_casa == placar_time_fora:
                                    # verifica se a odd é superior a 1.6 e se o time é um bom vencedor jogando em casa
                                    try:
                                        # envia uma entrada de vitória
                                        entrada_vitoria_time_da_casa(objeto_com_todas_as_entradas= item_copia, item_da_lista_de_objetos= item, time_casa= time_casa, lista_de_entradas_para_enviar= entradas_para_enviar)
                                    except:
                                        pass
                                        
                                # verifica se o time favorito está perdendo em casa.
                                elif placar_time_casa < placar_time_fora:
                                    # verifica se entrar em dupla chance do time é algo coerente.
                                    entrada_dupla_chance_time_da_casa(objeto_com_todas_as_entradas= item_copia, item_da_lista_de_objetos= item, time_casa= time_casa, lista_de_entradas_para_enviar= entradas_para_enviar)
                                        
                            # time jogando fora de casa 
                            if time_fora in melhores_times:
                                # verifica se o jogo está empatado.
                                if placar_time_casa == placar_time_fora:
                                    try:
                                        entrada_vitoria_time_fora(objeto_com_todas_as_entradas= item_copia, item_da_lista_de_objetos= item, time_fora = time_fora, lista_de_entradas_para_enviar= entradas_para_enviar)
                                    except:
                                        pass
                                        
                                    # se o time favorito estiver perdendo fora de casa
                                elif placar_time_casa > placar_time_fora: 
                                    entrada_dupla_chance_time_fora(objeto_com_todas_as_entradas= item_copia, item_da_lista_de_objetos= item, time_fora = time_fora, lista_de_entradas_para_enviar= entradas_para_enviar)
                            
                            if (time_casa in melhores_times or time_fora in melhores_times) and tempo_de_jogo > 60:
                                entrada_ao_menos_um_gol_no_jogo(item_da_lista_de_objetos= item, lista_de_entradas_para_enviar= entradas_para_enviar)
                                

                    else:
                        print(f"Ambas as equipes são favoritas no jogo entre {time_casa} x {time_fora}")

                except Exception as e:
                    # Trata qualquer exceção que possa ocorrer
                    print(f"Erro ao processar item: {e}")
        except Exception as e:
            # Trata qualquer exceção que possa ocorrer no loop principal
            print(f"Erro ao processar objetos_times: {e}")


        for item in objetos_times:
            try:
                entrada_ao_menos_um_gol_no_jogo(item_da_lista_de_objetos= item, lista_de_entradas_para_enviar= entradas_para_enviar)

                    # # deletando a chave de ODDS para não confundir o usuário.
                    # del item["Odd vitória casa"]

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