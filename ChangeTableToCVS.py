import pandas as pd
import re
from original import data


# Lista para armazenar os dados extraídos
dados_extraidos = []

# Variável para armazenar o estado atual ("Inicio", "Liberou", "Abastecendo", etc.)
estado_atual = "Inicio"

# Expressão regular para capturar os valores numéricos
regex = r"Vrms:\s([\d.]+)\s*v;.*?Irms:\s([\d.]+)\s*A;.*?P:\s([\d.]+)\s*W;.*?S:\s([\d.]+)\s*VA;.*?FP:\s([\d.]+);.*?At\(sample\):\s*(\d+)Qnt:\s*(\d+);"

# Processando linha por linha
for linha in data.split("\n"):
    linha = linha.strip()
    
    # Se a linha contém uma mensagem de estado, extraímos o estado
    estado_match = re.search(r'Sent utf8 encoded message: "(.+?)"', linha)
    if estado_match:
        estado_atual = estado_match.group(1)  # Atualiza o estado
        continue  # Pula essa linha, pois não contém dados numéricos
    
    # Se a linha contém dados numéricos, extraímos as informações
    match = re.search(regex, linha)
    if match:
        valores = list(match.groups()) + [estado_atual]  # Adiciona o estado ao final
        dados_extraidos.append(valores)

# Criando um DataFrame Pandas
colunas = ["Vrms", "Irms", "P", "S", "FP", "At_sample", "Qnt", "Estado"]
df = pd.DataFrame(dados_extraidos, columns=colunas)

# Convertendo colunas numéricas para float ou int
df[["Vrms", "Irms", "P", "S", "FP"]] = df[["Vrms", "Irms", "P", "S", "FP"]].astype(float)
df[["At_sample", "Qnt"]] = df[["At_sample", "Qnt"]].astype(int)

# Exibindo a tabela resultante
print(df)

# Salvando em um arquivo CSV
df.to_csv("dados_processados.py", index=False)
print("\nArquivo 'dados_processados.py' salvo com sucesso!")









