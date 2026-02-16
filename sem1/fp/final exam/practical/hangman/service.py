import random

from domain import Sentence
from exceptions import ValidationException
from repo import TextFileRepo


class SentenceService:
    def __init__(self, repo: TextFileRepo):
        self._repo = repo

    def add_sentence_service(self, sentence:str):
        if len(sentence.strip()) < 1:
            raise ValidationException("The sentence must contain at least one word!")

        parts = sentence.strip().split(" ")
        for word in parts:
            if len(word) < 3:
                raise ValidationException("Every word must contain at least 3 letters!")

        new_sentence = Sentence(sentence)
        self._repo.add_sentence(new_sentence)

    def select_random(self):
        sentences = self._repo.get_all()
        return random.choice(sentences)

    def start_game(self):
        sentence = self.select_random()
        text = sentence.sentence

        revealed_letters = set()
        words = text.split()
        for word in words:
            revealed_letters.add(word[0])
            revealed_letters.add(word[-1])

        return text, revealed_letters

    def masked_sentence(self, text, revealed_letters):
        result = ""
        for char in text:
            if char == " ":
                result += " "
            elif char in revealed_letters:
                result += char
            else:
                result += "_"
        return result

    def process_guess(self, guess:str, secret_text, revealed_set, current_hangman):
        if len(guess) != 1 or not guess.isalpha():
            raise ValidationException("Your guess cannot be empty!")

        if guess in secret_text and guess not in revealed_set:
            revealed_set.add(guess)
            return True, current_hangman

        else:
            full_word = "hangman"
            next_letter = full_word[len(current_hangman)]
            current_hangman += next_letter
            return False, current_hangman