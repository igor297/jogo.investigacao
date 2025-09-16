from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from ai_system import PersonagemIA
from database import init_database
import os

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend React

# Inicializar sistema de IA
ai_system = PersonagemIA()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({"status": "ok", "message": "API funcionando"})

@app.route('/test', methods=['GET'])
def test_connection():
    """Endpoint simples para testar conexão do app mobile"""
    return jsonify({"status": "success", "message": "Backend Python conectado!", "version": "1.0"})

@app.route('/api/personagens', methods=['GET'])
def get_personagens():
    """Retorna lista de todos os personagens disponíveis"""
    import sqlite3

    conn = sqlite3.connect('backend/game_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, name, alias, role, is_culprit
        FROM personagens
    ''')

    rows = cursor.fetchall()
    conn.close()

    personagens = []
    for row in rows:
        personagens.append({
            'id': row[0],
            'name': row[1],
            'alias': row[2],
            'role': row[3],
            'is_culprit': bool(row[4])
        })

    return jsonify(personagens)

@app.route('/api/personagem/<personagem_id>', methods=['GET'])
def get_personagem(personagem_id):
    """Retorna informações básicas de um personagem específico"""
    char_data = ai_system.get_personagem_data(personagem_id)

    if not char_data:
        return jsonify({"error": "Personagem não encontrado"}), 404

    # Retornar apenas informações básicas (não os segredos)
    basic_info = {
        'id': char_data['id'],
        'name': char_data['name'],
        'alias': char_data['alias'],
        'age': char_data['age'],
        'role': char_data['role'],
        'personality': char_data['personality'],
        'backstory': char_data['backstory']
    }

    return jsonify(basic_info)

@app.route('/api/interrogar', methods=['POST'])
def interrogar_personagem():
    """Endpoint principal para interrogar personagens"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400

        personagem_id = data.get('personagem_id')
        question = data.get('question')

        if not personagem_id or not question:
            return jsonify({"error": "personagem_id e question são obrigatórios"}), 400

        # Validar se personagem existe
        char_data = ai_system.get_personagem_data(personagem_id)
        if not char_data:
            return jsonify({"error": "Personagem não encontrado"}), 404

        # Gerar resposta usando IA
        response = ai_system.generate_response(personagem_id, question)

        return jsonify({
            "personagem_id": personagem_id,
            "personagem_name": char_data['name'],
            "question": question,
            "answer": response,
            "timestamp": "now"
        })

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/conversa/<personagem_id>', methods=['GET'])
def get_conversa_historico(personagem_id):
    """Retorna histórico de conversas com um personagem"""
    try:
        limit = request.args.get('limit', 10, type=int)

        history = ai_system.get_conversation_history(personagem_id, limit)

        conversations = []
        for question, answer in history:
            conversations.append({
                'question': question,
                'answer': answer
            })

        return jsonify({
            "personagem_id": personagem_id,
            "conversations": conversations
        })

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/reset_conversa/<personagem_id>', methods=['POST'])
def reset_conversa(personagem_id):
    """Reset do histórico de conversa de um personagem"""
    try:
        import sqlite3

        conn = sqlite3.connect('backend/game_database.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM conversations WHERE personagem_id = ?
        ''', (personagem_id,))

        conn.commit()
        conn.close()

        return jsonify({"message": f"Histórico de conversa resetado para {personagem_id}"})

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/dica/<personagem_id>', methods=['GET'])
def get_dica_interrogatorio(personagem_id):
    """Fornece dicas sobre como interrogar o personagem"""
    char_data = ai_system.get_personagem_data(personagem_id)

    if not char_data:
        return jsonify({"error": "Personagem não encontrado"}), 404

    # Dicas baseadas na personalidade do personagem
    personality = char_data['personality'].lower()

    dicas = []

    if 'nervoso' in personality:
        dicas.append("Este personagem parece nervoso. Perguntas diretas podem fazê-lo revelar mais.")
        dicas.append("Tente pressionar sobre inconsistências no álibi.")

    if 'defensivo' in personality:
        dicas.append("Este personagem é defensivo. Aborde com perguntas indiretas primeiro.")
        dicas.append("Pergunte sobre outras pessoas para deixá-lo mais confortável.")

    if 'pomposo' in personality or 'autoridade' in personality:
        dicas.append("Este personagem gosta de demonstrar conhecimento. Deixe-o falar.")
        dicas.append("Pergunte sobre detalhes que só ele saberia.")

    if char_data['is_culprit']:
        dicas.append("Há algo estranho neste personagem. Observe contradições.")
        dicas.append("Confronte com evidências conhecidas.")

    if not dicas:
        dicas = [
            "Pergunte sobre o álibi e relacionamentos com Helena.",
            "Investigue possíveis motivações para o crime.",
            "Questione sobre o que viram na noite do sequestro."
        ]

    return jsonify({
        "personagem_id": personagem_id,
        "personagem_name": char_data['name'],
        "dicas": dicas
    })

@app.route('/api/pedido-socorro', methods=['GET'])
def get_pedido_socorro():
    """Gera pedidos de socorro da vítima usando IA"""
    import random

    # Contextualizar com informações do caso
    contexto = {
        "vitima": "Helena",
        "local": "Solar dos Campos",
        "situacao": "sequestrada",
        "tempo": "há alguns dias",
        "ambiente": "porão escuro e úmido"
    }

    # Templates de pedidos de socorro baseados no contexto
    templates = [
        "Socorro... meu nome é Helena... estou presa no {local}... alguém me ajude...",
        "Por favor... me tirem daqui... está muito escuro... ouço ruídos estranhos...",
        "Ajuda... estou no porão do {local}... {tempo} que estou aqui... tenho medo...",
        "Detetive... se está me ouvindo... procure no {local}... há segredos nas paredes...",
        "Me encontrem... não sei exatamente onde estou... mas ouço o barulho da chuva no telhado...",
        "Tenho frio e fome... por favor... minha família deve estar preocupada...",
        "O homem que me trouxe... ele disse que conhece minha família... isso me assusta...",
        "Há algo estranho nesta casa... sussurros nas paredes... vozes que não consigo entender...",
        "Ouço passos lá fora... acho que alguém vem vindo... me escondam...",
        "Não me deixem aqui... prometo que não vou contar nada... só quero voltar para casa..."
    ]

    # Variações de intensidade emocional
    intensidades = {
        "desesperado": {
            "prefixo": "POR FAVOR! ",
            "sufixo": "... EU IMPLORO!",
            "velocidade": 0.6
        },
        "sussurrado": {
            "prefixo": "",
            "sufixo": "... (sussurrando para não me ouvirem)",
            "velocidade": 0.8
        },
        "chorando": {
            "prefixo": "*soluçando* ",
            "sufixo": "... *choro*",
            "velocidade": 0.7
        },
        "esperançoso": {
            "prefixo": "Ainda há esperança... ",
            "sufixo": "... acredito que vão me encontrar...",
            "velocidade": 0.9
        }
    }

    # Selecionar template e intensidade aleatórios
    template = random.choice(templates)
    intensidade_key = random.choice(list(intensidades.keys()))
    intensidade = intensidades[intensidade_key]

    # Formatar mensagem com contexto
    mensagem = template.format(**contexto)
    mensagem_final = f"{intensidade['prefixo']}{mensagem}{intensidade['sufixo']}"

    # Adicionar informações sobre localização específica (às vezes)
    if random.random() < 0.3:  # 30% de chance
        localizacoes = [
            "Estou ouvindo água gotejando...",
            "Há uma janela pequena muito alta...",
            "Sinto cheiro de mofo e madeira velha...",
            "Ouço música clássica vindo de cima...",
            "Há baús antigos aqui embaixo..."
        ]
        localizacao = random.choice(localizacoes)
        mensagem_final += f" {localizacao}"

    return jsonify({
        "mensagem": mensagem_final,
        "intensidade": intensidade_key,
        "configuracao_voz": {
            "velocidade": intensidade['velocidade'],
            "pitch": 0.8 if intensidade_key == "desesperado" else 0.9,
            "volume": 0.7 if intensidade_key == "sussurrado" else 0.9
        },
        "contexto": contexto
    })

if __name__ == '__main__':
    # Inicializar banco de dados se não existir
    if not os.path.exists('backend/game_database.db'):
        print("Inicializando banco de dados...")
        init_database()

    print("Iniciando servidor Flask na porta 5000...")
    print("Frontend React deve estar em http://localhost:3003")
    print("API disponível em http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000)