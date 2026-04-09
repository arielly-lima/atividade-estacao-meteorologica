import sqlite3

DATABASE = 'dados.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE, timeout=10) # [cite: 130]
    conn.execute('PRAGMA journal_mode=WAL')      # [cite: 131]
    conn.execute('PRAGMA busy_timeout=5000')     # [cite: 132]
    conn.row_factory = sqlite3.Row               # [cite: 133]
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def inserir_leitura(temperatura, umidade, pressao=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)',
                (temperatura, umidade, pressao))
    conn.commit()
    novo_id = cur.lastrow_id
    conn.close()
    return novo_id

def listar_leituras(limite=50):
    conn = get_db_connection()
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?', (limite,)).fetchall()
    conn.close()
    return leituras

def buscar_leitura(id):
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id,)).fetchone()
    conn.close()
    return leitura

def atualizar_leitura(id, dados):
    conn = get_db_connection()
    conn.execute('UPDATE leituras SET temperatura = ?, umidade = ?, pressao = ? WHERE id = ?',
                 (dados['temperatura'], dados['umidade'], dados.get('pressao'), id))
    conn.commit()
    conn.close()

def deletar_leitura(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
    conn.commit()
    conn.close()