import re

import hunspell
from textdistance import levenshtein, jaro_winkler, needleman_wunsch
import numpy as np
import nltk
from pyphonetics import Metaphone, RefinedSoundex


class SpellChecker:
    def __init__(self):
        self.spellchecker = hunspell.HunSpell("/usr/share/hunspell/en_US.dic", "/usr/share/hunspell/en_US.aff")
        self.metaphone = Metaphone()
        self.soundex = RefinedSoundex()

    def _features(self, word, candidates):
        features = np.array(
            [
                [
                    (1 - levenshtein(word, candidate)) / max(len(word), len(candidate)),
                    1 - jaro_winkler(word, candidate),
                    self.metaphone.distance(word, candidate) / max(len(word), len(candidate)),
                    self.soundex.distance(word, candidate) / max(len(word), len(candidate)),
                    (1 - needleman_wunsch(word, candidate)) / max(len(word), len(candidate)),
                ]
                for candidate in candidates
            ]
        )
        return features

    def _ranking(self, word, candidates):
        features = self._features(word, candidates)
        return np.argsort(np.mean(features, axis=1))

    def suggest_word(self, word, tag=None, eval=False):
        if tag is None:
            tag = nltk.pos_tag([word])[0][-1]

        if tag == "NNP":
            self.spellchecker.add(word)
            return [word] if eval else word

        candidates = self.spellchecker.suggest(word)
        if len(candidates) == 0:
            return [] if eval else ""
        if len(candidates) == 1:
            return candidates if eval else candidates[0]

        ranked_idx = self._ranking(word, candidates)
        candidates_ranked = [candidates[i] for i in ranked_idx]
        if eval:
            return candidates_ranked

        return candidates_ranked[0]

    def check(self, text):
        words = nltk.word_tokenize(text)
        tags = nltk.pos_tag(words)
        for (word, tag) in tags:
            if word.isalpha():
                substitution = self.suggest_word(word, tag)
                regex = r"\b" + word + r"\b"
                text = re.sub(regex, substitution, text)

        return text
