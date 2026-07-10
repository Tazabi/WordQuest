from datetime import datetime
from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    streak = db.Column(db.Integer, default=0)
    max_streak = db.Column(db.Integer, default=0)

    # Связи с прогрессом
    user_words = db.relationship('UserWord', backref='user', lazy=True)
    test_progress = db.relationship('UserTestProgress', backref='user', lazy=True)

last_activity_date = db.Column(db.Date, nullable=True)  # дата последней активности для стрика

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(50), nullable=False)      # например, 'Elementary'
    section = db.Column(db.String(100), nullable=False)   # раздел внутри уровня
    order = db.Column(db.Integer, nullable=False)         # порядок в roadmap

    questions = db.relationship('Question', backref='test', lazy=True)
    words = db.relationship('Word', secondary='test_word', lazy='subquery',
                            backref=db.backref('tests', lazy=True))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'match', 'fill', 'choice'
    content = db.Column(db.Text, nullable=False)               # JSON с вариантами ответов
    correct_answer = db.Column(db.Text, nullable=False)        # правильный ответ (или JSON)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), nullable=False)
    russian = db.Column(db.String(100), nullable=False)
    part_of_speech = db.Column(db.String(20))   # 'noun', 'verb', etc.
    # по умолчанию ранг 0, интервал 12 часов будет вычисляться в коде


# Связь многие-ко-многим между тестами и словами
test_word = db.Table('test_word',
    db.Column('test_id', db.Integer, db.ForeignKey('test.id'), primary_key=True),
    db.Column('word_id', db.Integer, db.ForeignKey('word.id'), primary_key=True)
)


class UserWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    rank = db.Column(db.Integer, default=0)
    last_review = db.Column(db.DateTime, default=datetime.utcnow)
    next_review = db.Column(db.DateTime, default=datetime.utcnow)  # сразу доступно для повторения
    times_reviewed = db.Column(db.Integer, default=0)


class UserTestProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
