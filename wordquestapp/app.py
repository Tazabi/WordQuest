import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_login import LoginManager
import secrets
from flask import render_template
from flask_login import login_required

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'wordquest.db')
# Для MySQL строка была бы: mysql+pymysql://user:password@localhost/wordquest
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # отключает предупреждения
app.config['SECRET_KEY'] = secrets.token_hex(16)



db.init_app(app)
# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # куда перенаправлять неавторизованных
login_manager.login_message = 'Пожалуйста, войдите, чтобы получить доступ.'
login_manager.login_view = 'auth.login'


from models import User, Test, Question, Word, UserWord, UserTestProgress
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/')

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
