import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'wordquest.db')
# Для MySQL строка была бы: mysql+pymysql://user:password@localhost/wordquest
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # отключает предупреждения

db.init_app(app)
from models import User, Test, Question, Word, UserWord, UserTestProgress

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/tests')
def list_tests():
    tests = Test.query.all()
    result = []
    for t in tests:
        result.append({
            'id': t.id,
            'title': t.title,
            'words': [w.english for w in t.words]
        })
    return {'tests': result}

if __name__ == '__main__':
    app.run(debug=True)
