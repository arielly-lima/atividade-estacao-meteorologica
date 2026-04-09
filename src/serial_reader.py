import json
import requests
import time
import random # Para simulação

URL = 'http://localhost:5000/leituras'

def gerar_dados_simulados():
    """Gera valores aleatórios realistas para teste """
    temp = round(random.uniform(20.0, 30.0), 2)
    umid = round(random.uniform(40.0, 70.0), 2)
    pressao = round(random.uniform(1010.0, 1015.0), 2)
    return {"temperatura": temp, "umidade": umid, "pressao": pressao}

def ler_e_enviar():
    print("Iniciando simulação de dados... Pressione Ctrl+C para parar.")
    while True:
        try:
            dados = gerar_dados_simulados()
            response = requests.post(URL, json=dados)
            
            if response.status_code == 201:
                print(f"Enviado com sucesso: {dados}")
            else:
                print(f"Erro no servidor: {response.status_code}")
                
        except Exception as e:
            print(f"Erro de conexão com a API: {e}")
            
        time.sleep(5) # Intervalo de 5 segundos conforme requisito [cite: 78, 96]

if __name__ == '__main__':
    ler_e_enviar()