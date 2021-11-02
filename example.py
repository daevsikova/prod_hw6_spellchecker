from spellchecker import SpellChecker

if __name__ == "__main__":
    spellchecker = SpellChecker()

    text = "It iss vry nise dai"
    print(spellchecker.check(text))

    word = "cucimbre"
    print(spellchecker.suggest_word(word))
