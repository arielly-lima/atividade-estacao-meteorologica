import json
import requests
import time
import random

# Configurações
URL = 'http://localhost:5000/leituras'

def simular_estacao():
    print("=== Modo de Simulação Ativado ===")
    print(f"Enviando dados para: {URL}")
    print("Pressione Ctrl+C para parar.\n")
    
    while True:
        try:
            # Gerando dados aleatórios realistas 
            dados_simulados = {
                "temperatura": round(random.uniform(22.0, 31.0), 2),
                "umidade": round(random.uniform(40.0, 75.0), 2),
                "pressao": round(random.uniform(1010.0, 1015.0), 2)
            }
            
            # Fazendo o POST para a API Flask [cite: 159, 174]
            response = requests.post(URL, json=dados_simulados)
            
            if response.status_code == 201:
                print(f"Enviado com sucesso: {dados_simulados}")
            else:
                print(f"Erro no servidor: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("Erro: O servidor Flask não está rodando. Inicie o app.py primeiro!")
            
        # Espera 5 segundos entre as leituras (conforme requisito) [cite: 78, 96]
        time.sleep(5)

if __name__ == '__main__':
    simular_estacao()