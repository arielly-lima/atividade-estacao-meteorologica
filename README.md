# Estação Meteorológica IoT

Sistema de monitoramento meteorológico desenvolvido para a disciplina de Engenharia de Computação — Módulo 5 (Automação de Processos e Sistemas).

---

## O que o projeto faz

Um script Python simula uma estação meteorológica gerando dados de temperatura, umidade e pressão a cada 5 segundos. Esses dados são enviados via HTTP para uma API Flask, que os salva em um banco SQLite. Uma interface web exibe as leituras em tempo real com gráfico e tabela.

**Fluxo:**
```
serial_reader.py (simulador) → POST → API Flask (app.py) → SQLite (dados.db) → Interface Web
```

---

## Decisão de Arquitetura

Como o hardware físico (Arduino + DHT11) não estava disponível, o `serial_reader.py` substitui o Arduino. Ele gera valores aleatórios realistas (temperatura entre 22–31°C, umidade 40–75%, pressão 1010–1015 hPa) e os envia para a API, replicando o comportamento que o `serial_reader.py` original teria ao ler a porta USB serial.

O código do Arduino (`arduino/estacao.ino`) também está presente e já inclui um fallback com valores aleatórios caso os sensores físicos não respondam.

---

## Estrutura de Arquivos

```
estacao-meteorologica/
├── arduino/
│   └── estacao.ino          # Sketch do Arduino (com fallback de simulação)
├── src/
│   ├── app.py               # Servidor Flask — rotas e API REST
│   ├── database.py          # Funções de acesso ao banco SQLite
│   ├── serial_reader.py     # Simulador que envia dados para a API
│   ├── schema.sql           # Criação da tabela no banco
│   ├── dados.db             # Banco de dados gerado automaticamente
│   ├── static/
│   │   ├── css/style.css    # Estilos da interface
│   │   └── js/main.js       # Gráfico com Chart.js
│   └── templates/
│       ├── base.html        # Layout base com navbar
│       ├── index.html       # Dashboard com gráfico e últimas leituras
│       ├── historico.html   # Tabela completa com editar/excluir
│       └── editar.html      # Formulário de edição de uma leitura
└── README.md
```

---

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Passo 1 — Clone ou extraia o projeto

```bash
cd estacao-meteorologica
```

### Passo 2 — Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### Passo 3 — Instale as dependências

```bash
pip install flask pyserial requests
```

> O `sqlite3` já vem instalado com o Python, não precisa instalar separadamente.

---

## Como Executar

### Terminal 1 — Inicie o servidor Flask

```bash
cd src
python app.py
```

O servidor sobe em `http://localhost:5000`. O banco `dados.db` é criado automaticamente na primeira execução.

### Terminal 2 — Inicie o simulador

Com o venv ativado, abra outro terminal e rode:

```bash
cd src
python serial_reader.py
```

O simulador vai enviar uma nova leitura a cada 5 segundos. Você verá mensagens como:

```
Enviado com sucesso: {'temperatura': 27.43, 'umidade': 61.2, 'pressao': 1012.5}
Enviado com sucesso: {'temperatura': 25.81, 'umidade': 58.9, 'pressao': 1013.1}
```

### Passo 3 — Acesse a interface

Abra o navegador em: **http://localhost:5000**

---

## Rotas da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Dashboard com as últimas 10 leituras e gráfico |
| GET | `/leituras` | Histórico completo (HTML) |
| GET | `/leituras?formato=json` | Histórico em JSON |
| POST | `/leituras` | Cria nova leitura (usado pelo simulador) |
| GET | `/leituras/<id>` | Abre formulário de edição |
| POST | `/leituras/<id>` | Salva edição de uma leitura |
| GET | `/leituras/deletar/<id>` | Remove uma leitura |
| GET | `/api/estatisticas` | Retorna médias, máximo e mínimo de temperatura e umidade |

### Exemplo de POST manual (via curl ou Postman)

```bash
curl -X POST http://localhost:5000/leituras \
  -H "Content-Type: application/json" \
  -d '{"temperatura": 25.5, "umidade": 60.0, "pressao": 1013.0}'
```

Resposta esperada:
```json
{"id": 1, "status": "criado"}
```

---

## Banco de Dados

O schema da tabela principal:

```sql
CREATE TABLE IF NOT EXISTS leituras (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL NOT NULL,
    umidade     REAL NOT NULL,
    pressao     REAL,
    localizacao TEXT DEFAULT 'Lab',
    timestamp   DATETIME DEFAULT (datetime('now', 'localtime'))
);
```

O arquivo `dados.db` já vem com leituras de exemplo. Para zerar e começar do zero, basta deletar o arquivo — ele será recriado ao iniciar o Flask.

**Nota sobre escrita simultânea:** O banco usa `PRAGMA journal_mode=WAL`, o que permite que o Flask e o simulador escrevam ao mesmo tempo sem travar um ao outro.

---

## Tecnologias

- **Python 3** + **Flask** — servidor web e API REST
- **SQLite3** — banco de dados (nativo do Python)
- **PySerial** — preparado para conexão com Arduino físico
- **Requests** — o simulador usa para fazer POST à API
- **Chart.js** — gráfico de variação temporal no dashboard
- **HTML + CSS + JavaScript** — interface web