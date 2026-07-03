from app import db, app
from models import User, Test, Question, Word, test_word

with app.app_context():
    # Очистка (осторожно: удалит все данные!)
    db.drop_all()
    db.create_all()

    # Создаём несколько слов
    w1 = Word(english='say', russian='сказать', part_of_speech='verb')
    w2 = Word(english='tell', russian='рассказывать', part_of_speech='verb')
    w3 = Word(english='hear', russian='слышать', part_of_speech='verb')
    w4 = Word(english='listen', russian='слушать', part_of_speech='verb')
    db.session.add_all([w1, w2, w3, w4])
    db.session.commit()

    # Создаём тест
    test1 = Test(title='Глаголы речи и восприятия', level='Elementary', section='Глаголы', order=1)
    db.session.add(test1)
    db.session.commit()

    # Привязываем слова к тесту
    test1.words.append(w1)
    test1.words.append(w2)
    test1.words.append(w3)
    test1.words.append(w4)

    # Добавляем вопросы (упрощённо: тип choice, выбираем перевод)
    q1 = Question(
        test_id=test1.id,
        question_type='choice',
        content='{"options": ["сказать", "рассказывать", "слышать", "слушать"]}',
        correct_answer='сказать'
    )
    q2 = Question(
        test_id=test1.id,
        question_type='choice',
        content='{"options": ["сказать", "рассказывать", "слышать", "слушать"]}',
        correct_answer='рассказывать'
    )
    # Добавляем ещё вопросы на другие слова...
    db.session.add_all([q1, q2])
    db.session.commit()

    print("База данных заполнена тестовыми данными.")
