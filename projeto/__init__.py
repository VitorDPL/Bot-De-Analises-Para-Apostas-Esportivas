# def verifica_se_a_mensagem_ja_foi_enviada(mensagem_atual):
#     mensagens_enviadas = [
#     ]

#     # Mostra mensagens já enviadas antes da comparação
#     print("Mensagens enviadas antes:")
#     for item in mensagens_enviadas:
#         print(item)
#     print("-" * 50)

#     for mensagem in mensagem_atual[:]:
#         foi_enviada = False
#         for enviada in mensagens_enviadas:
#             if mensagem["Casa"] == enviada["Casa"] and mensagem["Entrada"] == enviada["Entrada"]:
#                 print(f"Iguais: {mensagem}")
#                 foi_enviada = True

#         if not foi_enviada:
#             print(f"Diferentes: {mensagem}")
#             mensagens_enviadas.append(mensagem)

#     # Mostra mensagens após a comparação
#     print("Mensagens enviadas após:")
#     for item in mensagens_enviadas:
#         print(item)
#     print("-" * 50)

# # Exemplo de uso
# mensagem_atual = [
#     {
#         "Entrada": "Vitória Bayern",
#         "Casa": "Bayern",
#         "Fora": "Wolfsburg",
#         "Placar": "0 - 0",
#         "Link do jogo": "null",
#         "Odd vitória casa": 2.10,
#         "Odd vitória fora": 2.0,
#         "Tempo de jogo": 75
#     },
#     {
#         "Entrada": "Dupla chance Vasco",
#         "Casa": "Vasco",
#         "Fora": "São Paulo",
#         "Placar": "0 - 1",
#         "Link do jogo": "null",
#         "Odd vitória casa": 2.10,
#         "Odd vitória fora": 2.0,
#         "Tempo de jogo": 75
#     },
#     {
#         "Entrada": "Vitória Manchester City",
#         "Casa": "Manchester City",
#         "Fora": "Wolves",
#         "Placar": "0 - 0",
#         "Link do jogo": "null",
#         "Odd vitória casa": 2.10,
#         "Odd vitória fora": 2.0,
#         "Tempo de jogo": 75
#     }
# ]

# verifica_se_a_mensagem_ja_foi_enviada(mensagem_atual)

# Arquivo: main.py