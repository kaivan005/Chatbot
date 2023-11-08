import json
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import random
import re
from spellchecker import SpellChecker

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def rephrase_sentence(var1):
    list2 = list(var1.split(" "))
    var1_len = len(list2)
    result = []
    for i in range(0, var1_len, 1):
        list1 = list(list2)
        for j in range(0, var1_len, 1):
            temp = list1[i]
            list1[i] = list1[j]
            list1[j] = temp
            str = " ".join(list1)
            new = rephrase_text(str)
            for k in range(0, len(list1), 1):
                result.append(new[k])
            temp = list1[i]
            list1[i] = list1[j]
            list1[j] = temp
    return result

def rephrase_text(input_sentence):
    words = input_sentence.split()
    result = []

    for i in range(len(words)):
        new_sentence = ' '.join(words[i:] + words[:i])
        result.append(new_sentence)

    return result

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
    response = "I'm sorry, I don't understand that."
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

    if response == "I'm sorry, I don't understand that.":
        misspelled_words = spell_checker.unknown(user_words)
        if misspelled_words:
            suggestions = [spell_checker.correction(word) for word in misspelled_words]
            suggestion_text = ', '.join(suggestions)
            response = f"I couldn't understand your input. Did you mean: {suggestion_text}?"
            for suggestion in suggestions:
                for item in dataset:
                    keywords = item['keywords']
                    responses = item['responses']
                    if suggestion in keywords:
                        response = random.choice(responses)
                        break

    if response == "I'm sorry, I don't understand that.":
        rephrased_user_input =  list(set(rephrase_sentence(user_input)))
        lenth_input = len(rephrased_user_input)
        i = 0
        while i < lenth_input and response == "I'm sorry, I don't understand that.":
            for user_input in rephrased_user_input:
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

            i = i + 1

    return response
import pandas as df

key_data = []
res_data = []
for item in dataset:
    keywords = item['keywords']
    responses = item['responses']
    key_data.append(keywords)
    res_data.append(responses)

giv_data =[]
for i in range(0,len(key_data)):
    for j in range(0,len(key_data[i])):
        giv_data.append(key_data[i][j])
        giv_data.append(generate_response(key_data[i][j]))
        giv_data.append(res_data[i][0])


lst_fin = []
for l in range(0,len(giv_data),3):
    lst = []
    lst.append(giv_data[l])
    lst.append(giv_data[l+1])
    lst.append(giv_data[l+2])
    lst_fin.append(lst)

df12 = df.DataFrame(lst_fin, columns=["keyword_given", "response_generated","response_for_it"])
df12.to_csv('chat_data.csv', index=False)
