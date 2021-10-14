# Based on: https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
# To solve: https://challenge.dreambroker.jobs/245768c7-b82f-4a77-abbc-d1214acf7163

from flask import Flask
from flask_restful import Resource, Api, reqparse
from collections import defaultdict
import string

app = Flask(__name__)
api = Api(app)

class Analyze(Resource):
    def post(self):
        parser = reqparse.RequestParser() #initialize

        parser.add_argument('text', required=True)

        args = parser.parse_args()

        input_text = args.get('text')
        input_text = input_text.lower()

        withSpaces = len(input_text)
        withoutSpaces = withSpaces - input_text.count(" ")

        withoutPunct = input_text.translate(input_text.maketrans('', '', string.punctuation))

        wordList = withoutPunct.split()
        wordCount = len(wordList)

        characterCount = defaultdict(int)
        excludeList = [' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for char in withoutPunct:
            if (char not in excludeList):
                characterCount[char] += 1
        
        #print('#DBG:', [characterCount])
        characterCount = dict(sorted(characterCount.items())) # ordered

        listCharCount=[]
        for it in characterCount.items(): # to list
            listCharCount.append(dict([it]))
        return {'textLength':{'withSpaces':withSpaces, 'withoutSpaces':withoutSpaces},'wordCount':wordCount, 'characterCount':listCharCount}, 200

api.add_resource(Analyze, '/analyze')  # '/analyze' is the entry point

if __name__ == '__main__':
    app.run()  # run our Flask app

