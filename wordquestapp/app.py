from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db


app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordquest.db'  # SQLite
# Для MySQL строка была бы: mysql+pymysql://user:password@localhost/wordquest
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # отключает предупреждения

db.init_app(app)
from Models import User, Test, Question, Word, UserWord, UserTestProgress

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
