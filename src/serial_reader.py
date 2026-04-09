import serial, json, requests, time

PORTA = 'COM3' # Windows [cite: 161, 164]
BAUD = 9600
URL = 'http://localhost:5000/leituras'

def ler_serial():
    print(f"Iniciando leitura na porta {PORTA}...")
    try:
        with serial.Serial(PORTA, BAUD, timeout=2) as ser: # [cite: 167]
            while True:
                linha = ser.readline().decode('utf-8').strip() # [cite: 168]
                if linha:
                    try:
                        dados = json.loads(linha) # [cite: 173]
                        response = requests.post(URL, json=dados) # [cite: 174]
                        print(f"Status: {response.status_code} | Enviado: {dados}")
                    except Exception as e:
                        print(f"Erro ao processar linha: {e}")
                time.sleep(0.1)
    except serial.SerialException:
        print("Erro: Arduino desconectado ou porta ocupada.") # [cite: 207]

if __name__ == '__main__':
    ler_serial()