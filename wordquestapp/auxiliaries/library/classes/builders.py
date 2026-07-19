from typing import Any

class Tray:
    def __init__(self):
        self.tray = list()

    def add(self, item):
        self.tray.append(item)
        return self
    
    def addall(self, *items):
        self.tray.extend(items)
        return self
    
    def build(self):
        return self.tray

class Prompt:
    def __init__(self):
        self.string = "{}: {}"
        self.prompt_ru = "Предложение на русском"
        self.prompt_en = "Предложение на английском"
    
    def ru(self, string):
        self.prompt_ru = string
        return self

    def en(self, string):
        self.prompt_en = string
        return self
    
    def build(self):
        return self.string.format(self.prompt_ru, self.prompt_en)

class ChallengeBuilder:
    def __init__(self):
        self.dictionary = dict()

    def add(self, id: Any, challenge: str, options: list, correct: int):
        self.dictionary[id] = {
            "prompt": challenge,
            "options": options,
            "correct": correct
        }
        return self
    
    def build(self):
        return self.dictionary
    

class ChallengeInfoBuilder:
    def __init__(self):
        self.info = list()

    def add(self, prompt, response):
        self.info.append((prompt, response))
        return self

    def build(self):
        return self.info
    
class DictWord:
    def __init__(self):
        self.data = dict()

    def eng(self, word):
        self.data['word_en'] = word
        self.data['key'] = word
        return self

    def ru(self, word):
        self.data['word_ru'] = word
        return self

    def pos(self, pos):
        self.data['pos'] = pos
        return self
    
    def key(self, pos):
        self.data['key'] = pos
        return self
    
    def build(self):
        return self.data

class DictionaryBuilder:
    def __init__(self):
        self.dictionary = dict()

    def add(self, value: dict):
        key = value.pop('key', 'unknown')
        self.dictionary[key] = value
        return self
    
    def build(self):
        return self.dictionary