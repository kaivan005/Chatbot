from flask import Flask, request, render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import json
import random
import re

from spellchecker import SpellChecker

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

with open('responses.json', 'r') as file:
    dataset = json.load(file)

spell_checker = SpellChecker()

def generate_response(user_input):
    user_words = preprocess_text(user_input)
    user_input = ' '.join(user_words)
    response = "LawMiner: I'm sorry, I don't understand that."
    best_match_score = 0

    for item in dataset:
        keywords = item['keywords']
        responses = item['responses']
         
        for keyword in keywords:
            pattern = r'\w*' + re.escape(keyword) + r'\w*'
            match = re.search(pattern, user_input)
            if match:  
                match_score = len(match.group()) / len(keyword)
                if match_score > best_match_score:
                    best_match_score = match_score
                    response = random.choice(responses)

    if response == "LawMiner: I'm sorry, I don't understand that.":
        misspelled_words = spell_checker.unknown(user_words)
        if misspelled_words:
            suggestions = [spell_checker.correction(word) for word in misspelled_words]
            suggestion_text = ', '.join(suggestions)
            response = f"LawMiner: I couldn't understand your input. Did you mean: {suggestion_text}?"
            for suggestion in suggestions:
                for item in dataset:
                    keywords = item['keywords']
                    responses = item['responses']
                    if suggestion in keywords:
                        response = random.choice(responses)
                        break
    return response

def spell_check(sentence):
    spell = SpellChecker()
    words = sentence.split()
    misspelled = spell.unknown(words)
    corrected_words = [spell.correction(word) if word in misspelled else word for word in words]
    corrected_sentence = " ".join(corrected_words)
    return corrected_sentence

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = generate_response(user_input)
    return {'response': response}

if __name__ == '__main__':
    app.run(debug=True)
