from flask import Flask, request, jsonify, render_template, redirect, url_for
import database

app = Flask(__name__)

# Rota do Painel Principal [cite: 141]
@app.route('/')
def index():
    conn = database.get_db_connection()
    # Busca as últimas 10 leituras para o dashboard [cite: 141]
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('index.html', leituras=leituras)

# Rota de Listagem Completa [cite: 141]
@app.route('/leituras', methods=['GET'])
def listar():
    formato = request.args.get('formato')
    conn = database.get_db_connection()
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC').fetchall()
    conn.close()

    if formato == 'json':
        return jsonify([dict(row) for row in leituras])
    return render_template('historico.html', leituras=leituras)

# Rota POST para receber dados [cite: 141, 144]
@app.route('/leituras', methods=['POST'])
def criar():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400
    
    id_novo = database.inserir_leitura(
        dados.get('temperatura'), 
        dados.get('umidade'), 
        dados.get('pressao')
    )
    return jsonify({'id': id_novo, 'status': 'criado'}), 201

# Rota DELETE para remover leitura [cite: 141]
@app.route('/leituras/<int:id>', methods=['DELETE', 'POST'])
def deletar(id):
    # Aceita POST para facilitar a deleção via formulário HTML simples
    conn = database.get_db_connection()
    conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    if request.method == 'DELETE':
        return jsonify({'status': 'removido'}), 200
    return redirect(url_for('listar'))

# Rota de Estatísticas (Média, Mín, Máx) [cite: 141]
@app.route('/api/estatisticas')
def estatisticas():
    conn = database.get_db_connection()
    stats = conn.execute('''
        SELECT 
            AVG(temperatura) as media_temp, 
            MIN(temperatura) as min_temp, 
            MAX(temperatura) as max_temp,
            AVG(umidade) as media_umid
        FROM leituras
    ''').fetchone()
    conn.close()
    return jsonify(dict(stats))

# Rota para exibir o formulário de edição
@app.route('/leituras/<int:id>/editar')
def editar_form(id):
    conn = database.get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('editar.html', leitura=leitura)

# Rota PUT para atualizar os dados [cite: 141]
@app.route('/leituras/<int:id>', methods=['PUT'])
def atualizar(id):
    dados = request.get_json()
    conn = database.get_db_connection()
    conn.execute('''
        UPDATE leituras 
        SET temperatura = ?, umidade = ?, pressao = ? 
        WHERE id = ?
    ''', (dados['temperatura'], dados['umidade'], dados['pressao'], id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'atualizado'}), 200

if __name__ == '__main__':
    database.init_db() # Inicializa o schema.sql [cite: 121]
    app.run(debug=True)
    
    