from flask import Flask, render_template, request, jsonify, redirect, url_for
import database

app = Flask(__name__)

# [cite: 141] - GET /: Painel principal
@app.route('/')
def index():
    leituras = database.listar_leituras(10)
    return render_template('index.html', leituras=leituras)

# [cite: 141] - GET /leituras: Histórico completo
@app.route('/leituras', methods=['GET'])
def listar():
    leituras = database.listar_leituras(100)
    if request.args.get('formato') == 'json':
        return jsonify([dict(row) for row in leituras])
    return render_template('historico.html', leituras=leituras)

# [cite: 141] - POST /leituras: Recebe dados do Serial Reader
@app.route('/leituras', methods=['POST'])
def criar():
    dados = request.get_json() # [cite: 147]
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400
    id_novo = database.inserir_leitura(dados['temperatura'], dados['umidade'], dados.get('pressao'))
    return jsonify({'id': id_novo, 'status': 'criado'}), 201

# [cite: 141] - GET /leituras/<id>: Detalhe/Edição
@app.route('/leituras/<int:id>', methods=['GET'])
def detalhe(id):
    leitura = database.buscar_leitura(id)
    if not leitura: return "Não encontrado", 404
    return render_template('editar.html', leitura=leitura)

# [cite: 141] - PUT /leituras/<id>: Atualizar
@app.route('/leituras/<int:id>', methods=['PUT', 'POST'])
def atualizar(id):
    if request.method == 'POST': # Simplificação para formulário HTML
        dados = {
            'temperatura': request.form.get('temperatura'),
            'umidade': request.form.get('umidade'),
            'pressao': request.form.get('pressao')
        }
    else:
        dados = request.get_json()
    
    database.atualizar_leitura(id, dados)
    return redirect(url_for('listar'))

# [cite: 141] - DELETE /leituras/<id>
@app.route('/leituras/deletar/<int:id>')
def deletar(id):
    database.deletar_leitura(id)
    return redirect(url_for('listar'))

# [cite: 141] - GET /api/estatisticas
@app.route('/api/estatisticas')
def estatisticas():
    conn = database.get_db_connection()
    stats = conn.execute('SELECT AVG(temperatura), AVG(umidade), MAX(temperatura), MIN(temperatura) FROM leituras').fetchone()
    conn.close()
    return jsonify({
        'temp_media': round(stats[0], 2) if stats[0] else 0,
        'umid_media': round(stats[1], 2) if stats[1] else 0,
        'max_temp': stats[2],
        'min_temp': stats[3]
    })

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True, port=5000) # [cite: 208]