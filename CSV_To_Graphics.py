import pandas as pd
import matplotlib.pyplot as plt
from dados_processados import data

# Simulando os dados da tabela (substitua por seu arquivo real)
"""    FORMATO ENTRADA
Vrms,Irms,P,S,FP,At_sample,Qnt,Estado
205.22,4.58,293.65,940.04,0.31,2,0,Inicio
191.13,5.11,270.29,977.37,0.28,2,0,Inicio
211.87,5.73,394.99,1214.36,0.33,2,0,Inicio
203.78,4.78,320.24,974.75,0.33,3,0,Inicio
224.64,5.27,373.19,1184.22,0.32,2,0,Inicio
202.10,4.33,282.24,876.00,0.32,2,0,Inicio
209.65,4.87,354.39,1021.49,0.35,2,0,Inicio
207.86,4.95,341.66,1029.74,0.33,2,0,Inicio
202.71,4.42,278.10,896.33,0.31,2,0,Inicio
207.75,5.35,374.99,1110.93,0.34,2,0,Inicio
"""

from io import StringIO
df = pd.read_csv(StringIO(data))

# Criando uma coluna de tempo acumulado
df['Tempo (s)'] = df['At_sample'].cumsum()

# Mapeando os valores da coluna "Estado"
estado_mapping = {
    "Inicio": 600,
    "inicio": 600,
    "iniciou": 600,
    "liberou": 100,
    "Liberou": 100,
    "abastecendo": 20
}
df["Estado"] = df["Estado"].map(estado_mapping).fillna(4)

# Calculando a média de potência e os limites de 10%
media_potencia = df["P"].mean()
limite_superior = media_potencia * 1.10
limite_inferior = media_potencia * 0.90

# Calculando o tempo total em cada estado
tempo_estado_600 = df[df["Estado"] == 600]["At_sample"].sum()
tempo_estado_100 = df[df["Estado"] == 100]["At_sample"].sum()
tempo_estado_20 = df[df["Estado"] == 20]["At_sample"].sum()

# Criando o gráfico
plt.figure(figsize=(10, 5))
plt.plot(df["Tempo (s)"], df["P"], label="Potência Ativa (P)", color="g", marker="o")
#plt.plot(df["Tempo (s)"], df["S"], label="Potência Aparente (S)", color="orange", marker="s")
#plt.plot(df["Tempo (s)"], df["FP"], label="Fator de Potência (FP)", color="red", marker="^")
plt.plot(df["Tempo (s)"], df["Estado"], label="Estado", color="blue", marker="s")

# Adicionando as linhas de média e limites
plt.axhline(y=media_potencia, color='red', linestyle='-', label="Média de Potência")
plt.axhline(y=limite_superior, color='yellow', linestyle='--', label="10% acima da média")
plt.axhline(y=limite_inferior, color='yellow', linestyle='--', label="10% abaixo da média")

# Adicionando informações sobre o tempo em cada estado
info_text = (f"600 Estado Fatiando: {tempo_estado_600}s\n"
             f"100 Estado Parado(Preparando): {tempo_estado_100}s\n"
             f"20  Estado Abastecendo: {tempo_estado_20}s")
plt.gcf().text(0.15, 0.85, info_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel("Tempo (s)")
plt.ylabel("Valores")
plt.title("Potência Ativa, Aparente, Fator de Potência e Estado ao longo do tempo")
plt.legend()
plt.grid()
plt.show()
