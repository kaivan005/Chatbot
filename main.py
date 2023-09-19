import json
import random
import re

with open('responses.json', 'r') as file:
    dataset = json.load(file)

def generate_response(user_input):
    user_input = user_input.lower()
    response = "I\'m sorry, I don't understand that."
    for item in dataset:
        keywords = item['keywords']
        responses = item['responses']
        for keyword in keywords:
            pattern = re.escape(keyword)
            if re.search(pattern, user_input):
                response = random.choice(responses)
                return response
    return response

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("LawMiner: Bye")
        break
    response = generate_response(user_input)
    print("LawMiner:", response)