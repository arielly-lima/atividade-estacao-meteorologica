import sqlite3

DATABASE = 'dados.db'

def get_db_connection():
    """Retorna uma conexão configurada com row_factory e modo WAL[cite: 121, 128]."""
    conn = sqlite3.connect(DATABASE, timeout=10) # [cite: 130]
    conn.execute('PRAGMA journal_mode=WAL')      # [cite: 131]
    conn.execute('PRAGMA busy_timeout=5000')     # [cite: 132]
    conn.row_factory = sqlite3.Row               # [cite: 133]
    return conn

def init_db():
    """Cria as tabelas se não existirem executando o schema.sql."""
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def inserir_leitura(temperatura, umidade, pressao=None):
    """Executa o INSERT e retorna o ID da nova leitura."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)',
        (temperatura, umidade, pressao)
    )
    conn.commit()
    # Correção: O atributo correto é lastrowid (sem o underline)
    novo_id = cur.lastrowid 
    conn.close()
    return novo_id

def listar_leituras(limite=50):
    """Retorna uma lista de leituras com limite para paginação básica."""
    conn = get_db_connection()
    leituras = conn.execute(
        'SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?', 
        (limite,)
    ).fetchall()
    conn.close()
    return leituras

def buscar_leitura(id):
    """Realiza um SELECT por ID para retornar uma leitura específica[cite: 122]."""
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id,)).fetchone()
    conn.close()
    return leitura

def atualizar_leitura(id, dados):
    """Executa o UPDATE nos campos de uma leitura específica[cite: 122]."""
    conn = get_db_connection()
    conn.execute(
        'UPDATE leituras SET temperatura = ?, umidade = ?, pressao = ? WHERE id = ?',
        (dados['temperatura'], dados['umidade'], dados.get('pressao'), id)
    )
    conn.commit()
    conn.close()

def deletar_leitura(id):
    """Remove uma leitura do banco de dados pelo ID[cite: 123]."""
    conn = get_db_connection()
    conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
    conn.commit()
    conn.close()