from auxiliaries.library.classes.builders import DictionaryBuilder, DictWord

### Часто повторяющиеся части речи
VERB = "verb"
VERB_IRR = "verb-irr"
INF = "inf."
GER = "ger."
ADJ = "adj."
NOUN = "noun"
PREP = "prep."
PRON = "pron."

# Конструктор словарей

VERB_DICTIONARY = (
    DictionaryBuilder()
    .add(
        (
            DictWord()
            .eng("to be")
            .ru("быть")
            .pos(INF)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("am")
            .ru("являюсь")
            .pos(VERB_IRR)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("are")
            .ru("являетесь / являются")
            .pos(VERB_IRR)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("is")
            .ru("является")
            .pos(VERB_IRR)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("next")
            .ru("следующий")
            .pos(ADJ)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("continue")
            .ru("продолжить")
            .pos(VERB)
            .build()
        )
    )
    .build()
)

ADJ_DICTIONARY = (
    DictionaryBuilder()
    .add(
        (
            DictWord()
            .eng("nice")
            .ru("хороший / добрый")
            .pos(ADJ)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("cool")
            .ru("крутой / прохладный")
            .pos(ADJ)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("strong")
            .ru("сильный / крепкий")
            .pos(ADJ)
            .build()
        )
    )
    .add(
            (
                DictWord()
                .eng("brave")
                .ru("смелый / отважный")
                .pos(ADJ)
                .build()
            )
    )
    .add(
            (
                DictWord()
                .eng("smart")
                .ru("умный / хитрый")
                .pos(ADJ)
                .build()
            )
    )
    .add(
            (
                DictWord()
                .eng("kind")
                .ru("добрый / хороший")
                .pos(ADJ)
                .build()
            )
    )
    .build()
)

NOUN_DICTIONARY = (
    DictionaryBuilder()
    .add(
        (
            DictWord()
            .eng("student")
            .ru("студент")
            .pos(NOUN)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("a student")
            .ru("один студент")
            .pos(NOUN)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("the student")
            .ru("этот студент")
            .pos(NOUN)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("students")
            .ru("студенты")
            .pos(NOUN)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("apple")
            .ru("яблоко")
            .pos(NOUN)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("an apple")
            .ru("одно яблоко")
            .pos(NOUN)
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("the apple")
            .ru("это яблоко")
            .pos(NOUN)
            .build()
        )
    )
    .build()
)

GRAMMAR_DICT = (
    DictionaryBuilder()
    .add(
        (
            DictWord()
            .eng("this")
            .ru("этот")
            .pos(PRON)
            .key("this1")
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("this")
            .ru("это")
            .pos(PRON)
            .key("this2")
            .build()
        )
    )
    .add(
        (
            DictWord()
            .eng("these")
            .ru('эти')
            .pos(PRON)
            .key('these1')
            .build()
        )
    )
    .build()
)
