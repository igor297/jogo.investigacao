import sqlite3
import json
import os

def init_database():
    """Inicializa o banco de dados SQLite com os dados dos personagens"""

    # Dados dos personagens baseados no jogo
    personagens_data = {
        "carlos": {
            "id": "carlos",
            "name": "Carlos Menezes",
            "alias": "O Empresário Falido",
            "age": 44,
            "role": "Empresário falido",
            "personality": "Ressentido, amargo, mas ainda mantém certa dignidade. Fala com tom de superioridade mascarando sua insegurança.",
            "backstory": "Ex-sócio próspero do pai de Helena nos negócios imobiliários. Perdeu uma fortuna significativa em disputa judicial com a família. Manteve relações cordiais superficiais para preservar aparências.",
            "motivation": "Vingança contra a família Campos pela ruína financeira, mas também uma possível tentativa de recuperar o que considera seu por direito.",
            "alibi": "Diz que saiu da festa às 23h para atender ligações de um 'investidor importante'. No entanto, o porteiro confirma que ele ainda estava nos jardins quase meia-noite.",
            "secrets": [
                "Está desesperadamente endividado",
                "Foi visto conversando com um homem estranho na festa",
                "Tem anotações de dívidas no carro",
                "Ainda nutre esperanças de recuperar sua fortuna através da família Campos"
            ],
            "key_relationships": {
                "Helena": "Relação complexa - ressentimento misturado com nostalgia dos bons tempos",
                "Pai de Helena": "Antigo sócio que o traiu na visão dele",
                "Marina": "Testemunha que o viu com homem estranho"
            },
            "speech_patterns": [
                "Usa linguagem formal e rebuscada",
                "Frequentemente menciona 'os bons tempos'",
                "Demonstra amargura disfarçada de nostalgia",
                "Evita falar diretamente sobre dinheiro"
            ],
            "is_culprit": False
        },
        "valeria": {
            "id": "valeria",
            "name": "Valéria Campos",
            "alias": "A Cunhada Ciumenta",
            "age": 38,
            "role": "Cunhada de Helena",
            "personality": "Elegante mas tensa, ciumenta, defensiva. Tenta manter aparências mas revela insegurança profunda.",
            "backstory": "Casou-se com o irmão de Helena há 12 anos. Sempre se sentiu em segundo plano nas decisões familiares. Demonstra ciúme crescente da influência de Helena.",
            "motivation": "Ciúme profundo da posição privilegiada de Helena na família e possível desejo de eliminar a 'competição' por influência e herança.",
            "alibi": "Afirma que estava no quarto arrumando os filhos, mas Joana, a governanta, a viu discutindo com Helena às 23h30 perto do jardim.",
            "secrets": [
                "Brigou com Helena na noite do sequestro",
                "Sua pulseira foi encontrada no jardim",
                "Tem ciúmes extremos da cunhada",
                "Teme perder a herança para Helena"
            ],
            "key_relationships": {
                "Helena": "Relacionamento tenso - ciúme e competição constante",
                "Irmão (marido)": "Casamento estável mas ela sente que ele prefere Helena",
                "Joana": "A governanta que a viu brigando com Helena",
                "Filhos": "Usa-os como justificativa para suas ações"
            },
            "speech_patterns": [
                "Defensiva quando questionada sobre Helena",
                "Menciona frequentemente seus filhos",
                "Usa tom de vítima incompreendida",
                "Evita admitir conflitos diretos"
            ],
            "is_culprit": False
        },
        "rogerio": {
            "id": "rogerio",
            "name": "Rogério Paiva",
            "alias": "O Motorista Desesperado",
            "age": 29,
            "role": "Motorista da família",
            "personality": "Nervoso, leal na superfície mas desesperado. Tenta manter compostura mas revela ansiedade extrema.",
            "backstory": "Trabalha como motorista da família há 5 anos. Sempre demonstrou lealdade e competência. Contraiu dívidas significativas com agiotas.",
            "motivation": "Dívidas urgentes com agiotas que ameaçam sua vida. O sequestro representava sua única chance de conseguir dinheiro rápido usando seu acesso privilegiado à família.",
            "alibi": "Declara que permaneceu na garagem organizando o carro de Dona Laura, mas as câmeras de segurança mostram ele entrando na ala leste, próximo à biblioteca, às 23h40.",
            "secrets": [
                "É o verdadeiro culpado do sequestro",
                "Deve dinheiro para agiotas perigosos",
                "Conhece todos os segredos da casa",
                "Tinha chave reserva do sótão",
                "Foi flagrado pelas câmeras no horário do crime"
            ],
            "key_relationships": {
                "Helena": "Relação profissional respeitosa, mas ele a via como solução para seus problemas",
                "Família Campos": "Empregador confiável que ele traiu por desespero",
                "Agiotas": "Credores que ameaçam sua vida",
                "Pedro (garçom)": "Testemunha que o viu no local errado"
            },
            "speech_patterns": [
                "Fala de forma respeitosa mas nervosa",
                "Muda versões quando confrontado",
                "Demonstra conhecimento detalhado da casa",
                "Evita falar sobre dinheiro ou dívidas"
            ],
            "is_culprit": True,
            "crime_details": {
                "method": "Usou seu acesso ao Solar dos Campos para levar Helena ao sótão. Aproveitou o conhecimento da casa e das câmeras de segurança para executar o plano.",
                "motive": "Dívidas urgentes com agiotas. Precisava de dinheiro rápido e conhecia a rotina da família.",
                "evidence": "Tinha acesso físico ao sótão, foi flagrado pelas câmeras no horário do crime, tinha motivo imediato (dívidas) e foi visto perto da biblioteca onde o bilhete foi deixado."
            }
        },
        "clara": {
            "id": "clara",
            "name": "Clara Souza",
            "alias": "A Amiga Invejosa",
            "age": 24,
            "role": "Amiga de Helena",
            "personality": "Jovem, bonita mas amarga. Relacionamento complexo com Helena - amizade genuína misturada com inveja profunda.",
            "backstory": "Amiga de longa data de Helena desde a adolescência. Teve um relacionamento passado com o marido de Helena. Sempre demonstrou inveja sutil da vida luxuosa da amiga.",
            "motivation": "Inveja da vida privilegiada de Helena e ressentimento por relacionamentos passados, especialmente envolvendo o marido de Helena.",
            "alibi": "Disse que saiu da festa por volta das 23h15, mas o porteiro confirma que ela passou pelo portão apenas às 00h10.",
            "secrets": [
                "Teve relacionamento com o marido de Helena",
                "Escreveu carta criticando Helena que nunca enviou",
                "Mentiu sobre horário que saiu da festa",
                "Inveja profunda da vida luxuosa de Helena"
            ],
            "key_relationships": {
                "Helena": "Amizade complicada - amor e ódio misturados",
                "Marido de Helena": "Ex-namorado que ainda gera sentimentos",
                "Porteiro": "Testemunha que contradiz seu álibi",
                "Outros convidados": "Viram-na dançando até tarde"
            },
            "speech_patterns": [
                "Fala com carinho forçado sobre Helena",
                "Demonstra conhecimento íntimo da vida pessoal de Helena",
                "Usa tom defensivo quando questionada sobre horários",
                "Revela amargura ocasional"
            ],
            "is_culprit": False
        },
        "augusto": {
            "id": "augusto",
            "name": "Augusto Ramos",
            "alias": "O Administrador Corrupto",
            "age": 52,
            "role": "Administrador do Solar",
            "personality": "Experiente, pomposo, confiança excessiva mascarando preocupação constante sobre finanças.",
            "backstory": "Administra o Solar dos Campos há 15 anos. Desenvolveu esquemas de desvio de verba ao longo dos anos. Helena recentemente descobriu irregularidades em suas contas.",
            "motivation": "Medo de perder o emprego e exposição de suas práticas financeiras questionáveis. Helena descobriu irregularidades e planejava demiti-lo.",
            "alibi": "Afirma que passou a noite inteira coordenando garçons, mas nenhum funcionário confirma. Apenas diziam que ele 'aparecia e sumia' da cozinha.",
            "secrets": [
                "Desviou dinheiro da família por anos",
                "Helena descobriu suas irregularidades",
                "Estava prestes a ser demitido",
                "Conhece todos os segredos financeiros da família"
            ],
            "key_relationships": {
                "Helena": "Relação profissional tensa - ela descobriu seus crimes",
                "Família Campos": "Empregador de longa data que ele traiu",
                "Funcionários": "Subordinados que não confirmam seu álibi",
                "Contadores": "Cúmplices em potencial de seus esquemas"
            },
            "speech_patterns": [
                "Fala com autoridade sobre a casa",
                "Demonstra conhecimento detalhado das finanças",
                "Fica defensivo sobre questões financeiras",
                "Confunde detalhes quando pressionado"
            ],
            "is_culprit": False
        }
    }

    # Criar banco de dados
    conn = sqlite3.connect('backend/game_database.db')
    cursor = conn.cursor()

    # Criar tabelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personagens (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            alias TEXT,
            age INTEGER,
            role TEXT,
            personality TEXT,
            backstory TEXT,
            motivation TEXT,
            alibi TEXT,
            secrets TEXT,
            key_relationships TEXT,
            speech_patterns TEXT,
            is_culprit BOOLEAN,
            crime_details TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personagem_id TEXT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (personagem_id) REFERENCES personagens (id)
        )
    ''')

    # Inserir dados dos personagens
    for char_id, char_data in personagens_data.items():
        cursor.execute('''
            INSERT OR REPLACE INTO personagens
            (id, name, alias, age, role, personality, backstory, motivation, alibi,
             secrets, key_relationships, speech_patterns, is_culprit, crime_details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            char_data['id'],
            char_data['name'],
            char_data['alias'],
            char_data['age'],
            char_data['role'],
            char_data['personality'],
            char_data['backstory'],
            char_data['motivation'],
            char_data['alibi'],
            json.dumps(char_data['secrets']),
            json.dumps(char_data['key_relationships']),
            json.dumps(char_data['speech_patterns']),
            char_data['is_culprit'],
            json.dumps(char_data.get('crime_details', {}))
        ))

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_database()