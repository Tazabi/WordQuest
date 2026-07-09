import os
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import secrets
from flask import render_template
import json
from flask import session
from datetime import timedelta
from flask import request, jsonify
import datetime

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
    return redirect('/dashboard')

@app.route('/tests_debug')
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

@app.route('/tests')
@login_required
def tests_catalog():
    return redirect('/challenges')
    
@app.route('/wordbag')
@login_required
def wordbag():
    return render_template('wordbag.html')  # Заглушка
    
@app.route('/stats')
@login_required
def stats():
    return render_template('stats.html')  # Заглушка

@app.route('/challenges')
@login_required
def challenges():
    tests = Test.query.order_by(Test.level, Test.order).all()
    completed_set = {t.test_id for t in UserTestProgress.query.filter_by(user_id=current_user.id, completed=True).all()}
    # Определим доступность: если order==1, или (order-1) есть в completed_set
    accessible = []
    for t in tests:
        accessible.append(t.order == 1 or (t.order - 1) in completed_set)
    return render_template('challenges.html', tests=tests,
                           completed=completed_set,
                           accessible=accessible)

@app.route('/test/<int:test_id>')
@login_required
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    # Проверим доступность: либо первый тест в уровне, либо предыдущий пройден.
    # Эта логика будет использоваться и при старте, и при ответах.
    return render_template('test.html', test=test)

@app.route('/test/<int:test_id>/question/<int:question_index>')
@login_required
def get_question(test_id, question_index):
    test = Test.query.get_or_404(test_id)
    questions = Question.query.filter_by(test_id=test_id).order_by(Question.id).all()
    if question_index >= len(questions):
        return jsonify({'finished': True, 'score': ..., 'total': len(questions), 'new_words': [...]})
    q = questions[question_index]
    content = json.loads(q.content)  # предполагаем, что content – это JSON с 'options' и 'prompt'
    print('[DEBUG]', content)
    return jsonify({
        'index': question_index,
        'prompt': content.get('prompt', 'Выберите перевод'),
        'options': content.get('options', []),
        'total': len(questions)
    })

@app.route('/test/<int:test_id>/answer', methods=['POST'])
@login_required
def answer_question(test_id):
    data = request.get_json()
    question_index = data['question_index']
    user_answer = data['answer']
    test = Test.query.get_or_404(test_id)
    questions = Question.query.filter_by(test_id=test_id).order_by(Question.id).all()
    q = questions[question_index]
    correct = (user_answer.strip().lower() == q.correct_answer.strip().lower())

    # Сохраняем прогресс: можно хранить временные данные в сессии или создать таблицу для ответов.
    # Для MVP будем хранить прогресс в сессии Flask.
    if 'test_progress' not in session:
        session['test_progress'] = { 'correct': 0, 'answers': [] }
    progress = session['test_progress']
    if correct:
        progress['correct'] += 1
    progress['answers'].append({'qid': q.id, 'correct': correct})

    # Если это последний вопрос – завершаем тест
    if question_index + 1 >= len(questions):
        # Отмечаем тест как пройденный
        progress_record = UserTestProgress.query.filter_by(user_id=current_user.id, test_id=test_id).first()
        if not progress_record:
            progress_record = UserTestProgress(user_id=current_user.id, test_id=test_id)
            db.session.add(progress_record)
        progress_record.completed = True
        # Добавляем слова пользователю (из связи test.words)
        new_words = []
        now = datetime.utcnow()
        for word in test.words:
            # Проверяем, нет ли уже записи (чтобы не дублировать)
            existing = UserWord.query.filter_by(user_id=current_user.id, word_id=word.id).first()
            if not existing:
                new_word = UserWord(user_id=current_user.id, word_id=word.id,
                                    rank=0, last_review=now,
                                    next_review=now + timedelta(hours=12))
                db.session.add(new_word)
                new_words.append(word.english)
        db.session.commit()
        # Очищаем прогресс в сессии
        session.pop('test_progress', None)
        return jsonify({'correct': correct, 'next_question': None, 'finished': True,
                        'score': progress['correct'], 'total': len(questions),
                        'new_words': new_words})
    else:
        session['test_progress'] = progress
        next_idx = question_index + 1
        return jsonify({'correct': correct, 'next_question': next_idx, 'finished': False})

if __name__ == '__main__':
    app.run(debug=True)
