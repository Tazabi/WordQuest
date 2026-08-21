from app import db, app
from models import User, Test, Question, Word, UserTestProgress, UserWord
from werkzeug.security import generate_password_hash
from auxiliaries.data_manager import DataManager, TestBuilder
from auxiliaries.library.dictionary import VERB_DICTIONARY as VDICT
from auxiliaries.library.dictionary import NOUN_DICTIONARY as NDICT
from auxiliaries.library.dictionary import ADJ_DICTIONARY as ADICT
from auxiliaries.library.dictionary import GRAMMAR_DICT as GDICT
from auxiliaries.library.challenge_info import TOBE1, THIS1, TOBE2
from auxiliaries.library.challenge_data import VERB_FORMS as VFORMS
from auxiliaries.library.challenge_data import GRAMMAR as GR

DM = DataManager(Test, Word, Question)

NEXT = 'next'
CONTINUE = 'continue'

with app.app_context():
    # Очистка (осторожно: удалит все данные!)
    db.drop_all()
    db.create_all()

    # Инициализация тестов (при помощи класса TestBuilder)
    (
        TestBuilder(DM, db.session)
        .create_test("TO BE: Глагол-связка",
                     "Elementary",
                     "Verbs",
                     1)
        .batch_words(VDICT, ['am', 'are', 'is', 'continue'])
        .batch_words(ADICT, ['cool', 'nice'])
        .word(**NDICT['students'])
        .qbatch_info(TOBE1)
        .qbatch_choice(VFORMS, ['am0', 'is1', 'are0', 'are2'])
    )

    (
        TestBuilder(DM, db.session)
        .create_test("Первые TH: This / These",
                     "Elementary",
                     "Grammar",
                     2)
        .batch_words(GDICT, ['this1', 'this2', 'these1'])
        .qbatch_info(THIS1)
        .qbatch_choice(GR, ['this0', 'these2', 'these1', 'this2'])
    )

    (
        TestBuilder(DM, db.session)
        .create_test("IS / AM / ARE",
                     "Elementary",
                     "Verbs",
                     3)
        .batch_words(VDICT, ["am", "is", "are"])
        .batch_words(NDICT, ['teacher', 'student'])
        .batch_words(ADICT, ['strong', 'brave', 'smart', 'kind'])
        .qbatch_info(TOBE2)
        .qbatch_choice(GR, ['this3', 'this4', 'these3', 'these4'])
    )

    user = User(email='cheesedestroyer3000@gmail.com', password_hash=generate_password_hash('ILikeMozarella'))
    db.session.add(user)
    db.session.commit()

    # 1. Все тесты с их уровнями и порядком
    tests = Test.query.all()
    for t in tests:
        print(f"ID:{t.id}, {t.title}, Level:{t.level}, Order:{t.order}, Section:{t.section}")

    # 2. Все вопросы конкретного теста (например, test_id=1)
    questions = Question.query.filter_by(test_id=1).all()
    for q in questions:
        print(f"QID:{q.id}, Type:{q.question_type}, Prompt:{q.content}, Correct:{q.correct_answer}")

    # 3. Слова, привязанные к тесту
    test = Test.query.get(1)
    if test:
        print(f"Слова теста '{test.title}':")
        for w in test.words:
            print(f"  - {w.english} ({w.russian})")

    # 4. Все слова в базе
    words = Word.query.all()
    for w in words:
        print(f"Word ID:{w.id}, {w.english} - {w.russian}, Part:{w.part_of_speech}")

    # 5. Прогресс пользователей (если уже есть)
    progress = UserTestProgress.query.all()
    for p in progress:
        print(f"User:{p.user_id}, Test:{p.test_id}, Completed:{p.completed}")

    # 6. Слова у конкретного пользователя (user_id=1) и их ранг
    user_words = UserWord.query.filter_by(user_id=1).all()
    for uw in user_words:
        print(f"Word:{uw.word.english}, Rank:{uw.rank}, NextReview:{uw.next_review}")


    print("База данных заполнена тестовыми данными.")
