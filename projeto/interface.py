import tkinter as tk
import customtkinter
from main import *

# Configurações iniciais
customtkinter.set_appearance_mode("dark")  # Modo de aparência "dark"
customtkinter.set_default_color_theme("green")  # Tema de cores "green"

app = customtkinter.CTk()
app.title('Bot Para Análises Esportivas')
app.geometry("1000x600")  # Tamanho inicial da janela

# Configuração para expandir as células da grade
for i in range(10):  # Ajuste de acordo com o número máximo de linhas ou colunas ocupadas
    app.grid_rowconfigure(i, weight=1)
    app.grid_columnconfigure(i, weight=1)

# Dicionário com os tempos disponíveis
tempos_disponiveis_para_o_sistema_rodar = {
    "2 min e 30 seg" : "150",
    "5 minutos (Teste do bot)": 300,
    "10 minutos" : 600,
    "15 minutos" : 900,
    "48 minutos (1º tempo + acréscimos)": 2880,
    "1 hora e 40 minutos": 5400,
    "3 horas": 10800
}

# Função para pegar valor
def pegar_valor():
    opcao_selecionada = tempo_rodando.get()
    valor = tempos_disponiveis_para_o_sistema_rodar.get(opcao_selecionada)
    if valor is not None:
        print(f"Programa rodando por {valor} segundos.")
        return valor
    else:
        print("Opção selecionada não encontrada.")

# Labels e widgets
titulo = customtkinter.CTkLabel(app, text='Bot Para Análises Esportivas', font=("Arial", 28, "bold"), justify="center")
titulo.grid(row=0, column=0, padx=20, pady=30, sticky='nswe', columnspan=10)

c_ref = customtkinter.CTkLabel(app, text='Ao Vivo', font=("Arial", 28, "bold"), justify="center")
c_ref.grid(row=2, column=0, padx=20, pady=30, sticky='nswe', columnspan=5)

# Label para mostrar as métricas
metricas_texto = """
Algumas métricas utilizadas pelo nosso robô:
- Vitória de times favoritos em casa ou fora.
- Dupla chance de times favoritos em desvantagem.
- Over de gols em jogos de times no sistema.
- Over de escanteios em jogos de times no sistema.
"""
metricas = customtkinter.CTkLabel(app, text=metricas_texto.strip(), font=("Arial", 16), fg_color="#FF8C00", text_color="black", corner_radius=15, justify="left")
metricas.grid(row=1, column=0, padx=20, pady=10, sticky='nswe', columnspan=10)


# Label para selecionar o tempo
tempo_rodando_txt = customtkinter.CTkLabel(app, text="Defina o tempo que o bot ficará rodando", font=("Arial", 20), justify="center")
tempo_rodando_txt.grid(row=3, column=0, padx=10, pady=20, sticky='nswe', columnspan=5)

# Combobox para selecionar o tempo
tempo_rodando = customtkinter.CTkComboBox(app, values=list(tempos_disponiveis_para_o_sistema_rodar.keys()), font=("Arial", 18), justify="center")
tempo_rodando.grid(row=4, column=0, padx=10, pady=10, sticky='nswe', columnspan=5)

# Botão para buscar peças
buscar_botao = customtkinter.CTkButton(app, text='Executar Análise Ao Vivo', font=("Arial", 20), command=lambda: executar_ao_vivo(pegar_valor()))
buscar_botao.grid(row=5, column=0, padx=20, pady=30, sticky='nswe', columnspan=5)

c_ref_2 = customtkinter.CTkLabel(app, text='Analisar jogo único', font=("Arial", 28, "bold"), justify="center")
c_ref_2.grid(row=2, column=6, padx=20, pady=30, sticky='nswe', columnspan=5)

link_jogo_txt = customtkinter.CTkLabel(app, text="Insira o link do jogo (SofaScore)", font=("Arial", 20), justify="center")
link_jogo_txt.grid(row=3, column=6, padx=10, pady=20, sticky='nswe', columnspan=6)

link_jogo = customtkinter.CTkEntry(app)
link_jogo.grid(row= 4, column = 6 ,padx=10, pady=10, sticky='nswe', columnspan=6)

# Botão para buscar peças
buscar_botao = customtkinter.CTkButton(app, text='Analisar jogo único', font=("Arial", 20))
buscar_botao.grid(row= 5, column=6, padx=20, pady=30, sticky='nswe', columnspan=6)


text= """
© Start Bet
"""
footer = customtkinter.CTkLabel(app, text=text, font=("Arial", 16), fg_color="white", text_color="black")
footer.grid(row=6, column=0, sticky='nswe', columnspan=10)

app.mainloop()
