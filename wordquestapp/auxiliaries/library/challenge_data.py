from auxiliaries.library.classes.builders import ChallengeBuilder, Prompt, Tray

# Конструктор челленджей (зачаток процедурной генерации)

VERB_FORMS = (
    ChallengeBuilder()
    .add(
        "am0",
        (
            Prompt()
            .ru("Меня зовут Алекс")
            .en("I ___ Alex")
            .build()
        ),
        (
            Tray()
            .addall("am", "is", "are")
            .build()
        ),
        0
    )
    .add(
        "am2",
        (
            Prompt()
            .ru("Я зелёный?")
            .en("___ I green?")
            .build()
        ),
        (
            Tray()
            .addall("is", "are", "am")
            .build()
        ),
        2
    )
    .add(
        "is1",
        (
            Prompt()
            .ru("Это - Алекс")
            .en("This ___ Alex")
            .build()
        ),
        (
            Tray()
            .addall("are", "is", "am")
            .build()
        ),
        correct=1
    )
    .add(
        "is2",
        (
            Prompt()
            .ru("Это - я")
            .en("This ___ me")
            .build()
        ),
        (
            Tray()
            .addall("are", "am")
            .add("is")
            .build()
        ),
        correct=2
    )
    .add(
        "are0",
        (
            Prompt()
            .ru("Ты хороший")
            .en("You ___ nice")
            .build()
        ),
        (
            Tray()
            .addall("are", "is")
            .add("be")
            .build()
        ),
        correct=0
    )
    .add(
        "are2",
        (
            Prompt()
            .ru("Они студенты / ученики")
            .en("They ___ students")
            .build()
        ),
        (
            Tray()
            .addall("am", "is")
            .add("are")
            .build()
        ),
        correct=2
    )

    .build()
)

GRAMMAR = (
    ChallengeBuilder()
    .add("this0",
         (
             Prompt()
             .ru("Это я")
             .en("___ is me")
             .build()
         ),
         (
             Tray()
             .add("this")
             .add("these")
             .build()
         ),
         correct=0)
    .add(
        "these1",
        (
            Prompt()
            .ru("Эти яблоки вкусные")
            .en("___ apples are tasty")
            .build()
        ),
        (
            Tray()
            .add("this")
            .add("these")
            .build()
        ),
        correct=1
    )
    .add(
        "these2",
        (
            Prompt()
            .ru("Это - студенты")
            .en("___ are students")
            .build()
        ),
        (
            Tray()
            .add("this")
            .add("these")
            .build()
        ),
        correct=1
    )
    .add(
        "this2",
        (
            Prompt()
            .ru("Эта книга - интересная")
            .en("___ book is interesting")
            .build()
        ),
        (
            Tray()
            .add("this")
            .add("these")
            .build()
        ),
        correct=0
    )
    .build()
)

    

