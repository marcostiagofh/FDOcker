from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import time
from sqlalchemy import exc
from app import Visit
import os  # Adicione esta importação

app = Flask(__name__, template_folder='./docker-entrypoint-initdb.d/templates')  # Altere o caminho aqui
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/visit_counter'
db = SQLAlchemy(app)

# Função para aguardar a disponibilidade do banco de dados
def wait_for_db():
    max_retries = 30
    retries = 0

    while retries < max_retries:
        try:
            # Tenta se conectar ao banco de dados
            db.session.query("1").all()
            print("Conectado ao banco de dados!")
            return
        except exc.SQLAlchemyError:
            print(f"Tentativa {retries + 1}/{max_retries} - Não foi possível conectar ao banco de dados. Tentando novamente em 1 segundo...")
            time.sleep(1)
            retries += 1

    # Se não for possível conectar após o número máximo de tentativas
    raise RuntimeError("Não foi possível conectar ao banco de dados após várias tentativas.")

# Chame a função de espera antes de prosseguir
wait_for_db()

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

# Executar a criação da tabela de maneira mais robusta
with app.app_context():
    try:
        db.session.execute('SELECT 1')  # Testa a conexão
        db.create_all()
    except exc.SQLAlchemyError as e:
        print(f"Erro ao criar tabela: {e}")

@app.route('/')
def home():
    # Incrementa a contagem de visitas no banco de dados
    increment_count()

    # Obtém a contagem atual
    count = get_count()

    return render_template('index.html', count=count)  # Remova 'templates/' aqui

def increment_count():
    # Incrementa a contagem no banco de dados usando uma instrução SQL bruta
    db.engine.execute(text('UPDATE visit SET count = count + 1'))

def get_count():
    visit = Visit.query.first()
    if visit:
        return visit.count
    else:
        return 69  # ou outro valor padrão desejado

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
