from flask import Flask
from flask_ask import Ask, statement, question, session
from flask_ask import statement, question, convert_errors
import json
import requests
import time
import unidecode
import os


#AFFIRMATIVE = ["yes", "yeah", "sure", "ok"]

current_carbs = 0
current_protein = 0
current_fat = 0
rec_carb = 0
rec_protien = 0
rec_fats = 0

app = Flask(__name__)
ask = Ask(app, "/swoltrition")

# added for testing purposes
#def add(carbs, protein, fat):
 #   current_carbs = current_carbs + carbs
 #   current_protein = current_protein + protein
 #   current_fat = current_fat + fat

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
    if 'NoIntent' in convert_errors:
        return question("Sorry, can you repeat that.")
    bye_text = 'Why did you ask me then? You gotta eat big, or stay small!'
    return statement(bye_text)


#def decide(choice):
 #   speech_text = "Would you like to know all meals?"
  #  for x in AFFIRMATIVE:
  #      if x == choice:
   #         print("yes")
   #         #ask for the meal
 #       else:
    #        print("no")
    #        #give complete meal history for that day


#Gates Work on this vvvvvv
# This will retrieve the food mentioned by the user from the USDA database, and then add its macros to the users macro totals
#def get_foods():

    #return food

@ask.intent("RecordFoodIntent")
def log(food):
    if 'RecordFoodIntent' in convert_errors:
        return question("Sorry, can you repeat that.")
    speech_text = "{} has been recorded".format(food)
    return statement(speech_text)
    #send to database

#user wants to know macros
@ask.intent("CurrentMacrosIntent")
def report_macros():
    if 'CurrentMacrosIntent' in convert_errors:
            return question("Sorry, can you repeat that.")
    macros_text = "You have eaten %d g carbs, %d g protein, and %d g fat." % (current_carbs, current_protein, current_fat)
    return statement(macros_text)


app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
    app.run()
    app.run(debug=True)
