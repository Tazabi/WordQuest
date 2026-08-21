from typing import Any
from flask import jsonify

class DataManager:
    def __init__(self, test_class: type, word_class: type, question_class: type):
        self.test = test_class
        self.word = word_class
        self.question = question_class

class TestBuilder:
    def __init__(self, data_manager, session):
        self.data_manager = data_manager
        self.session = session
        self.test = None

    def create_test(self, title: str, level: str, section: str, order: int):
        test_data = {
            "title": title,
            "level": level,
            "section": section,
            "order": order
        }
        test = self.data_manager.test(
            title=test_data['title'],
            level = test_data['level'],
            section = test_data['section'],
            order = test_data['order']
        )
        self._create_test_if_not_exists(test, test_data)
        self.test = test
        return self

    def _create_test_if_not_exists(self, test, td):
        existing_test = self.data_manager.test.query.filter_by(
            title=td['title'],
            level=td['level'],
            section=td['section'],
            order=td['order']
        ).first()

        if existing_test:
            return
        
        self._commit_data(test)

    def _commit_data(self, obj: Any):
        self.session.add(obj)
        self.session.commit()

    def _commit_several(self, objects: list):
        self.session.add_all(objects)
        self.session.commit()

    def batch_words(self, category: dict, words: list[str]):
        """Добавить несколько слов из указанного словаря (category) по ключам из списка (words)"""
        for word in words:
            w = category.get(word, None)
            if w:
                self = self.word(**w)
        return self

    def word(self, **kwargs):
        return self.word_from_dict(word_en=kwargs.get('word_en', "none"), 
                                   word_ru=kwargs.get('word_ru', 'нет'), 
                                   pos=kwargs.get('pos', 'none'))

    def word_from_dict(self, word_en="none", word_ru="none", pos="unk"):
        return self.add_word(word_en, word_ru, pos=pos)
    
    def add_word(self, word_en, word_ru, pos="unk"):
        if not self.test:
            print('[WARN]: Объект "Тест" не создан.')
            return self
        
        word = self.data_manager.word(english=word_en,
                                      russian=word_ru,
                                      part_of_speech=pos)
        
        self._add_word_if_not_exists(word, word_en, word_ru, pos)
        self.test.words.append(word)
        return self

    def _add_word_if_not_exists(self, word, word_en, word_ru, pos):
        existing_word = self.data_manager.word.query.filter_by(
            english=word_en,
            russian=word_ru,
            part_of_speech=pos
        ).first()

        if existing_word:
            return
        
        self._commit_data(word)

    def _format_prompt(self, prompt: str):
        prompt = prompt.replace("'", "\'")
        prompt = prompt.replace('"', '\"')
        return prompt
    
    def _format_options(self, options: tuple):
        options = list(options)
        options_string = '['
        for i, o in enumerate(options):
            if i != len(options) - 1:
                options_string += '\"{}\", '.format(o)
            else:
                options_string += '\"{}\"], '.format(o)
        return options_string

    def _format_content_string(self, args: tuple, prompt: str):
        options = self._format_options(args)
        prompt = self._format_prompt(prompt)
        content = "{"
        content += '\"options\": '
        content += options
        content += '\"prompt\": '
        content += '\"{}\"'.format(prompt)
        content += '}'
        return content
    
    def _get_correct_answer(self, args: tuple, correct: int):
        if correct not in range(len(args)):
            return args[0]
        
        return args[correct]
    
    def qbatch_choice(self, category: dict, qlist: list[str]):
        """Добавить несколько вопросов с выбором ответа из категории (category), по ключам из списка (qlist)"""
        for item in qlist:
            question = category.get(item, None)
            if question:
                self = self.q_choice(**question)
        return self
    
    def q_choice(self, **kwargs):
        """Принимает словарь с аргументами options, prompt и correct, где options - это список слов, prompt - это текст вопроса, а correct - это """
        options = kwargs.get('options', [])
        options = list(options)
        prompt = kwargs.get('prompt', "Текст вопроса отсутствует")
        correct = kwargs.get('correct', 0)
        return self.add_question_choice(*options, prompt=prompt, correct=correct)

    def qbatch_arginfo(self, *args):
        """Добавить множественные вопросы типа Информация. Принимает кортежи из двух элементов, на первом месте стоит вопрос, на втором - ответ"""
        return self.qbatch_info([arg for arg in args if isinstance(arg, tuple)])
    
    def qbatch_info(self, category: list[tuple]):
        """Добавить множественные вопросы типа Информация из категории (category), представленной в виде списка кортежей, на первом месте промт, на втором ответ."""
        for question in category:
            if not isinstance(question, tuple):
                continue
            if not len(question) == 2:
                continue
            self = self.q_info(question[0], question[1])
        return self

    def q_info(self, prompt, option):
        return self.add_question_choice(
            option, prompt=prompt
        )

    def add_question_choice(self, *args, prompt="Текст вопроса", correct=0):
        if not self.test:
            print('[WARN]: Объект "Тест" не создан.')
            return self
        
        test_id = self.test.id

        question_details = {
            "test_id": test_id,
            "question_type": 'choice',
            "content": self._format_content_string(args, prompt),
            "correct_answer": self._get_correct_answer(args, correct)
        }

        question = self.data_manager.question(**question_details)
        self._add_question_if_not_exists(question, question_details)
        return self

    def _add_question_if_not_exists(self, question, qd):
        existing_question = self.data_manager.question.query.filter_by(
            test_id=qd['test_id'],
            question_type=qd['question_type'],
            content=qd['content'],
            correct_answer=qd['correct_answer']
        ).first()

        if existing_question:
            return
        
        self._commit_data(question)

    def build(self):
        return None

