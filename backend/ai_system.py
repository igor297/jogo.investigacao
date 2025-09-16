import sqlite3
import json
import random
import re
from typing import Dict, List, Tuple

class PersonagemIA:
    def __init__(self, db_path='backend/game_database.db'):
        self.db_path = db_path

    def get_personagem_data(self, personagem_id: str) -> Dict:
        """Busca dados do personagem no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM personagens WHERE id = ?
        ''', (personagem_id,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        columns = [desc[0] for desc in cursor.description]
        char_data = dict(zip(columns, row))

        # Parse JSON fields
        char_data['secrets'] = json.loads(char_data['secrets']) if char_data['secrets'] else []
        char_data['key_relationships'] = json.loads(char_data['key_relationships']) if char_data['key_relationships'] else {}
        char_data['speech_patterns'] = json.loads(char_data['speech_patterns']) if char_data['speech_patterns'] else []
        char_data['crime_details'] = json.loads(char_data['crime_details']) if char_data['crime_details'] else {}

        return char_data

    def save_conversation(self, personagem_id: str, question: str, answer: str):
        """Salva conversa no banco para histórico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO conversations (personagem_id, question, answer)
            VALUES (?, ?, ?)
        ''', (personagem_id, question, answer))

        conn.commit()
        conn.close()

    def get_conversation_history(self, personagem_id: str, limit: int = 5) -> List[Tuple]:
        """Busca histórico de conversas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT question, answer FROM conversations
            WHERE personagem_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (personagem_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return rows

    def analyze_question_intent(self, question: str) -> Dict[str, float]:
        """Analisa a intenção da pergunta para gerar resposta apropriada"""
        question_lower = question.lower()

        intents = {
            'alibi': 0.0,
            'relationship': 0.0,
            'motive': 0.0,
            'accusation': 0.0,
            'emotion': 0.0,
            'evidence': 0.0,
            'timeline': 0.0,
            'general': 0.0
        }

        # Palavras-chave para cada intenção
        alibi_keywords = ['onde', 'quando', 'hora', 'momento', 'estava', 'fazendo', 'horário']
        relationship_keywords = ['helena', 'família', 'conhece', 'relacionamento', 'amigo', 'opinião']
        motive_keywords = ['por que', 'motivo', 'razão', 'dinheiro', 'problema', 'conflito']
        accusation_keywords = ['culpado', 'culpa', 'fez', 'responsável', 'sequestro', 'crime']
        emotion_keywords = ['sente', 'sentimento', 'triste', 'raiva', 'medo', 'preocupado']
        evidence_keywords = ['evidência', 'prova', 'viu', 'ouviu', 'sabe', 'testemunha']
        timeline_keywords = ['antes', 'depois', 'durante', 'festa', 'noite', 'aconteceu']

        # Calcular scores
        for word in question_lower.split():
            if word in alibi_keywords:
                intents['alibi'] += 1
            if word in relationship_keywords:
                intents['relationship'] += 1
            if word in motive_keywords:
                intents['motive'] += 1
            if word in accusation_keywords:
                intents['accusation'] += 1
            if word in emotion_keywords:
                intents['emotion'] += 1
            if word in evidence_keywords:
                intents['evidence'] += 1
            if word in timeline_keywords:
                intents['timeline'] += 1

        # Se nenhuma intenção específica foi detectada
        if sum(intents.values()) == 0:
            intents['general'] = 1.0

        # Normalizar scores
        total = sum(intents.values())
        if total > 0:
            for key in intents:
                intents[key] = intents[key] / total

        return intents

    def generate_response(self, personagem_id: str, question: str) -> str:
        """Gera resposta baseada no personagem e contexto da pergunta"""
        char_data = self.get_personagem_data(personagem_id)
        if not char_data:
            return "Desculpe, não posso responder agora."

        intents = self.analyze_question_intent(question)
        primary_intent = max(intents, key=intents.get)

        # Buscar histórico para manter consistência
        history = self.get_conversation_history(personagem_id)

        response = self._generate_contextual_response(char_data, question, primary_intent, history)

        # Aplicar padrões de fala do personagem
        response = self._apply_speech_patterns(response, char_data)

        # Salvar conversa
        self.save_conversation(personagem_id, question, response)

        return response

    def _generate_contextual_response(self, char_data: Dict, question: str, intent: str, history: List) -> str:
        """Gera resposta baseada na intenção identificada"""

        # Respostas baseadas na personalidade e intenção
        if intent == 'alibi':
            return self._generate_alibi_response(char_data, question)
        elif intent == 'relationship':
            return self._generate_relationship_response(char_data, question)
        elif intent == 'motive':
            return self._generate_motive_response(char_data, question)
        elif intent == 'accusation':
            return self._generate_accusation_response(char_data, question)
        elif intent == 'emotion':
            return self._generate_emotion_response(char_data, question)
        elif intent == 'evidence':
            return self._generate_evidence_response(char_data, question)
        elif intent == 'timeline':
            return self._generate_timeline_response(char_data, question)
        else:
            return self._generate_general_response(char_data, question)

    def _generate_alibi_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta sobre álibi"""
        base_alibi = char_data['alibi']

        if char_data['is_culprit']:
            variations = [
                f"Como já disse, {base_alibi.lower()} Não tenho mais nada a acrescentar.",
                f"Minha versão não mudou: {base_alibi.lower()}",
                f"Já expliquei onde estava... {base_alibi.lower()} Por que continua duvidando?"
            ]
        else:
            variations = [
                f"Posso explicar novamente: {base_alibi.lower()}",
                f"Com certeza, {base_alibi.lower()} Várias pessoas podem confirmar.",
                f"Não tenho nada a esconder. {base_alibi}"
            ]

        return random.choice(variations)

    def _generate_relationship_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta sobre relacionamentos"""
        relationships = char_data['key_relationships']

        if 'helena' in question.lower():
            if 'Helena' in relationships:
                helena_rel = relationships['Helena']
                responses = [
                    f"Helena e eu... {helena_rel.lower()}. É complicado de explicar.",
                    f"Meu relacionamento com Helena sempre foi {helena_rel.lower()}",
                    f"Bem, sobre Helena... {helena_rel.lower()}. Isso resume bem nossa situação."
                ]
                return random.choice(responses)

        general_responses = [
            "Conheço a família há tempo suficiente para entender as dinâmicas aqui.",
            "Cada pessoa nesta casa tem seus segredos, detetive.",
            "Relacionamentos familiares são sempre complicados, especialmente quando há dinheiro envolvido."
        ]

        return random.choice(general_responses)

    def _generate_motive_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta sobre motivação"""
        if char_data['is_culprit']:
            deflect_responses = [
                "Motivo? Que motivo eu teria? Sempre fui leal a esta família.",
                "Não sei por que está me perguntando isso. Eu não tenho motivos para fazer mal a Helena.",
                "Está insinuando algo? Porque posso garantir que não tenho nada contra Helena."
            ]
            return random.choice(deflect_responses)
        else:
            # Pode revelar motivação parcialmente sem admitir culpa
            motivation = char_data['motivation']
            responses = [
                f"Olha, não vou negar que {motivation.lower()}, mas isso não significa que eu faria algo terrível.",
                f"Talvez seja verdade que {motivation.lower()}, mas há uma grande diferença entre sentir algo e agir sobre isso.",
                "Todo mundo tem suas frustrações, detetive. Isso não torna ninguém criminoso."
            ]
            return random.choice(responses)

    def _generate_accusation_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta a acusações"""
        if char_data['is_culprit']:
            nervous_responses = [
                "Está me acusando de algo muito sério. Espero que tenha provas.",
                "Isso é um absurdo! Por que eu faria algo assim?",
                "Não vou mais responder perguntas sem um advogado presente.",
                "Está completamente enganado sobre mim."
            ]
            return random.choice(nervous_responses)
        else:
            innocent_responses = [
                "Se está me acusando, está perdendo tempo. Eu não fiz nada.",
                "Pode investigar quanto quiser, não vai encontrar nada porque sou inocente.",
                "Essa acusação é ridícula. Você deveria estar procurando o verdadeiro culpado.",
                "Estou disposto a cooperar, mas não vou aceitar ser tratado como criminoso."
            ]
            return random.choice(innocent_responses)

    def _generate_emotion_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta emocional"""
        personality = char_data['personality']

        if 'nervoso' in personality.lower() or char_data['is_culprit']:
            responses = [
                "Estou preocupado, obviamente. Quem não estaria em uma situação dessas?",
                "É difícil manter a calma quando se está sendo investigado.",
                "Claro que estou abalado. Helena... isso é terrível."
            ]
        elif 'ciumenta' in personality.lower():
            responses = [
                "É frustrante ser constantemente comparada a Helena.",
                "Admito que às vezes sinto... ressentimento. Mas isso é natural.",
                "Nem todos temos a sorte de nascer com uma vida perfeita."
            ]
        else:
            responses = [
                "Estou preocupado com Helena, como qualquer pessoa decente estaria.",
                "É uma situação terrível para toda a família.",
                "Só quero que Helena seja encontrada em segurança."
            ]

        return random.choice(responses)

    def _generate_evidence_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta sobre evidências"""
        secrets = char_data['secrets']

        if char_data['is_culprit']:
            evasive_responses = [
                "Não sei nada sobre evidências. Talvez devesse procurar melhor.",
                "Se encontraram algo, tenho certeza de que há uma explicação lógica.",
                "Não posso comentar sobre evidências que não vi."
            ]
            return random.choice(evasive_responses)
        else:
            helpful_responses = [
                "Se posso ajudar com informações, estou à disposição.",
                "Vi algumas coisas estranhas naquela noite, mas não sei se são relevantes.",
                "Gostaria de poder ajudar mais, mas só posso contar o que sei."
            ]
            return random.choice(helpful_responses)

    def _generate_timeline_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta sobre cronologia dos eventos"""
        alibi = char_data['alibi']

        responses = [
            f"Sobre a cronologia... {alibi.lower()}",
            "A noite foi longa e confusa. Muita gente indo e vindo.",
            "Posso tentar lembrar dos detalhes, mas estava focado em outras coisas."
        ]

        return random.choice(responses)

    def _generate_general_response(self, char_data: Dict, question: str) -> str:
        """Gera resposta geral baseada na personalidade"""
        personality = char_data['personality']

        if 'nervoso' in personality.lower():
            responses = [
                "Desculpe, está sendo difícil pensar claramente com tudo isso acontecendo.",
                "Pode repetir a pergunta? Estou um pouco abalado.",
                "Vou tentar responder da melhor forma que posso."
            ]
        elif 'pomposo' in personality.lower():
            responses = [
                "Bem, isso é uma pergunta interessante, detetive.",
                "Com minha experiência, posso dizer que...",
                "Permita-me esclarecer essa questão para você."
            ]
        elif 'elegante' in personality.lower():
            responses = [
                "Claro, posso responder isso.",
                "É uma pergunta compreensível, dadas as circunstâncias.",
                "Vou fazer o melhor para ajudar na investigação."
            ]
        else:
            responses = [
                "O que mais gostaria de saber?",
                "Estou aqui para ajudar no que for necessário.",
                "Pode perguntar o que quiser."
            ]

        return random.choice(responses)

    def _apply_speech_patterns(self, response: str, char_data: Dict) -> str:
        """Aplica padrões de fala específicos do personagem"""
        speech_patterns = char_data['speech_patterns']
        name = char_data['name']

        # Aplicar modificações baseadas nos padrões de fala
        if 'formal' in ' '.join(speech_patterns).lower():
            response = response.replace('você', 'o senhor').replace('tá', 'está')

        if 'defensiva' in ' '.join(speech_patterns).lower():
            if random.random() < 0.3:  # 30% chance de adicionar tom defensivo
                defensive_additions = [
                    " Não sei por que está me perguntando isso.",
                    " Espero que não esteja duvidando de mim.",
                    " Já disse tudo que sei."
                ]
                response += random.choice(defensive_additions)

        return response