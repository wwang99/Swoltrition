from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import os


AFFIRMATIVE = ["yes", "yeah", "sure", "ok"]
lowCarb = 0
lowProt = 0
lowFiber = 0
highFat = 0
highSugar = 0
carbs = 0
protien = 0
fat - 0


app = Flask(__name__)
ask = Ask(app, "/alexa_nutrition")

@app.route('/')
def homepage():
    return "Hello World"
    

# What Alexa greets the user when prompted on a response regarding this application 
@ask.launch
def start_skill():
    welcome_message = 'Hello there, would do you want to see your current macros for the day, or log a food?'
    return question(welcome_message)

# If the user says no
@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)
    
    
#user wants to know macros
@ask.intent("CurrentMacros")
def report_macros():
    macros_text = "You have eaten %d g carbs, %d g protien, and %d g fat." % (carbs, protien, fat)
    return statement(macros_text)

#def decide(choice):
 #   speech_text = "Would you like to know all meals?"
def get
  #      if x == choice:
   #         print("yes")
   #         #ask for the meal
 #       else:
    #        print("no")
    #        #give complete meal history for that day
        
# This will retrieve the food mentioned by the user from the USDA database, and then add its macros to the users macro totals        
def get_foods():
    
    return food

@ask.launch('PromptLogFood')
def prompt():
    question_text = "What food would you like to log?"
    return question(question_text)
    
@ask.intent('RecordFood')
def log(food):
    speech_text = "{} has been recorded".format(food)
    return statement(speech_text)
    #send to database


app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
    app.run()
    app.run(debug=True)

    