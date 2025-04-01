#gerar o executável: C:\Users\Adriano\AppData\Roaming\Python\Python313\Scripts\pyinstaller.exe --onefile .\mqtt_2_sqlserver.py 

import paho.mqtt.client as mqtt
import pyodbc
import json
from datetime import datetime

# Configuração do SQL Server
server = '192.168.0.201'  # Endereço do SQL Server
database = 'AnaliseEquip'  # Nome do banco de dados
username = 'bi'  # Usuário do banco de dados
password = 'bizfx'  # Senha do banco de dados
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    topico = msg.topic
    mensagem = msg.payload.decode()  # Decodifica a mensagem recebida
    print(f"Recebido do tópico {topico}: {mensagem}")

    # Processar o JSON recebido
    data = json.loads(mensagem)
    nome = data['equipamento']
    horario = datetime.now()  # Obtém a data e hora atual
    # horario = datetime.strptime(data['hora'], '%Y-%m-%d %H:%M:%S')  # Se a hora vier no JSON

    # Inserindo os dados no banco de dados
    query = "INSERT INTO mosquitto (equipamento, data_hora) VALUES (?, ?)"
    valores = (nome, horario)
    cursor.execute(query, valores)
    conn.commit()  # Confirma as mudanças no banco de dados
    print("Dados inseridos no banco de dados com sucesso.")

# Configuração do cliente MQTT
broker = "192.168.0.203"  # Endereço do broker MQTT da presto: 192.168.0.203
topico = "AdrPresto"  # Tópico de assinatura

client = mqtt.Client()
#V2 #client = mqtt.Client(protocol=mqtt.MQTTv311, userdata=None, transport="tcp", protocol_api=2)

client.on_message = on_message  # Define a função de callback
client.connect(broker, 1883, 60)  # Conecta ao broker
client.subscribe(topico)  # Assina o tópico

# Loop para manter o cliente MQTT conectado
print("Aguardando mensagens...")
client.loop_forever()