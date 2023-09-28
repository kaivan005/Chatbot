from spellchecker import SpellChecker

def spell_check(sentence):
    spell = SpellChecker()
    words = sentence.split()
    misspelled = spell.unknown(words)
    corrected_words = [spell.correction(word) if word in misspelled else word for word in words]
    corrected_sentence = " ".join(corrected_words)
    return corrected_sentence

user_input = input("Enter a sentence: ")
corrected_input = spell_check(user_input)
print("Spell-checked sentence:", corrected_input)
