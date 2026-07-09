from app import db, app
from models import User, Test, Question, Word, UserTestProgress, UserWord
from werkzeug.security import generate_password_hash
from auxiliaries.data_manager import DataManager, TestBuilder

DM = DataManager(Test, Word, Question)

NEXT = 'next'
CONTINUE = 'continue'

with app.app_context():
    # Очистка (осторожно: удалит все данные!)
    db.drop_all()
    db.create_all()

    (
        TestBuilder(DM, db.session)
        .create_test("TO BE: Глагол-связка",
                     "Elementary",
                     "Verbs",
                     1)
        .add_word("am", "являюсь", "verb-irr")
        .add_word("are", "являетесь", "verb-irr")
        .add_word("is", "является", "verb-irr")
        .add_word("next", "следующий", "adj")
        .add_word("continue", "продолжить", "verb")
        .add_question_choice(
            NEXT,
            prompt="Нажми 'next' чтобы продолжить. 'next' значит 'далее'."
        )
        .add_question_choice(
            "My name is (...)",
            prompt="Отлично! Теперь ты знаешь свое первое слово. Теперь представься. Подставь своё имя вместо точек, мысленно."
        )
        .add_question_choice(
            NEXT,
            prompt="Супер! Теперь ты знаешь как представиться. Запомни: мы используем 'is' потому что слово 'name' (имя) единственного числа. Теперь, давай тренироваться."
        )
        .add_question_choice(
            "I am (...)",
            prompt="Ты можешь сказать 'Меня зовут ...' иначе. Для этого скажи..."
        )
        .add_question_choice(
            NEXT,
            prompt="Мы сейчас работаем с разными формами глагола TO BE (быть). Он особенный, но очень важный."
        )
        .add_question_choice(
            "I am Alex. / He is Alex. / This cat is Tom.",
            prompt="Запомни. С местоимением I (я) мы используем TO BE в форме 'am'. С существительными и местоимениями единственного числа - 'is'."
        )
        .add_question_choice(
            "We are friends. / They are students. / You are cool.",
            prompt="Когда чего-то много, мы в настоящем времени используем 'are'. Запомни, что 'you' (ты/вы) в английском во множественном числе. Он просто так устроен."
        )
        .add_question_choice(
            NEXT,
            prompt="Теперь, давай практиковаться."
        )
        .add_question_choice(
            "am", "is", "are",
            prompt="Какой глагол подставить в: I (???) Alex ?",
            correct=0
        )
        .add_question_choice(
            "am", "is", "are",
            prompt="Какой глагол подставим в: He/She/It (???) Alex ?",
            correct=1
        )
        .add_question_choice(
            "am", "is", "are",
            prompt="Какой глагол подставим в: You (???) Alex ?",
            correct=2
        )
        .add_question_choice(
            "am", "is", "are",
            prompt="Какой глагол подставим в: They (???) students ?",
            correct=2
        ) 
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
