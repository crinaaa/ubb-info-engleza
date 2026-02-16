import random

from exceptions import ValidationException, GameException
from repo import TextFileRepo
from domain import Sentence


class ServiceSentence:
    def __init__(self, repo:TextFileRepo):
        self._repo = repo
        self._score = 0
        self._history = []


    def choose_sentence(self):
        sentences = self._repo.get_all()
        chosen = random.choice(sentences)
        original = chosen.sentence.strip()


        scrambled_text = self.shuffle_sentence(original)
        self._score = len(original.replace(" ", ""))
        self._history = [scrambled_text]

        return original, scrambled_text, self._score


    def shuffle_sentence(self, sentence:str):
        chars = list(sentence)

        shuffle_indices = []
        words = sentence.split(" ")

        current_pos = 0
        for word in words:
            start_idx = current_pos
            end_idx = len(word) + start_idx - 1
            for i in range(start_idx+1, end_idx):
                shuffle_indices.append(i)

            current_pos += len(word) + 1

        letters_to_shuffle = [chars[i] for i in shuffle_indices]

        random.shuffle(letters_to_shuffle)

        for i, index_in_sentence in enumerate(shuffle_indices):
            chars[index_in_sentence] = letters_to_shuffle[i]

        return "".join(chars)

    def swap_letters(self, word1:int, pos1:int, word2:int, pos2:int, sentence:str):
        words = sentence.split(" ")

        if word1 < 0 or word2 < 0 or word1 >= len(words) or word2 >= len(words):
            raise ValidationException("Index for word out of range!")

        if pos1 < 0 or pos2 < 0 or pos1 >= len(words[word1]) or pos2 >= len(words[word2]):
            raise ValidationException("Index for letter out of range!")

        word_to_check = words[word1]
        if pos1 == 0 or pos1 == len(word_to_check):
            raise ValidationException("You cannot swap first or last letter of a word!")

        word_to_check = words[word2]
        if pos2 == 0 or pos2 == len(word_to_check):
            raise ValidationException("You cannot swap first or last letter of a word!")


        if word1 ==  word2:
            word = list(words[word1])
            word[pos1], word[pos2] = word[pos2], word[pos1]
            words[word1] = "".join(word)

        else:
            source_word = list(words[word1])
            dest_word = list(words[word2])
            source_word[pos1], dest_word[pos2] = dest_word[pos2], source_word[pos1]

            words[word1] = "".join(source_word)
            words[word2] = "".join(dest_word)

        return " ".join(words)


    def undo(self):
        if len(self._history) < 2:
            raise GameException("Cannot undo anymore!")
        self._history.pop()
        return self._history[-1]

    def perform_swap(self, w1, p1, w2, p2, current_sentence):
        self._history.append(current_sentence)
        new_sentence = self.swap_letters(w1,p1,w2,p2, current_sentence)
        self._score -= 1

        return new_sentence, self._score