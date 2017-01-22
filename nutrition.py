from flask import Flask
from flask_ask import Ask, statement, question, session
from flask_ask import statement, question, convert_errors
import json
import requests
import time
import unidecode
import os

current_carbs = 0.0
current_protein = 0.0
current_fat = 0.0
rec_carbs = 0.0
rec_protein = 0.0
rec_fat = 0.0

'''
#  <---- incase we need to reinitialize JSON file
person1 = {"current_carbs": current_carbs,
         "current_fat": current_fat,
         "current_protein": current_protein,
         "rec_carbs": rec_carbs,
         "rec_fat": rec_fat,
         "rec_protein": rec_protein}
         
with open('data.json', 'w') as fp:
        json.dump(person1, fp)
'''        
        
person1 = {}
    
with open('data.json', 'r') as fp:
        person1 = json.load(fp)

print(person1)


app = Flask(__name__)
ask = Ask(app, "/swoltrition")

@app.route('/')
def homepage():
    return "Hello World"

# What Alexa greets the user when prompted on a response regarding this application
@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to see your current macros for the day, log a food, or view recomended macros?'
    return question(welcome_message)

# If the user says no
@ask.intent("NoIntent")
def no_intent():
    if 'NoIntent' in convert_errors:
        return question("Sorry, can you repeat that.")
    bye_text = 'Why did you ask me then? You gotta eat big, or stay small man!'
    return statement(bye_text)


# This will retrieve the food mentioned by the user from the USDA database, and then add its macros to the users macro totals

@ask.intent("RecordFoodIntent")
def log(food):
    #if 'RecordFoodIntent' in convert_errors:
    #    return question("Sorry, can you repeat that.")
    search_payload = {'format': 'json', 'q': food, 'ds': 'Standard Reference', 'max': '1', 'api_key': 'AY1U6UdBQKwgOcvSaQVhLqcu5QdHagIPWgAQvHtU'}
    search_request = requests.get('http://api.nal.usda.gov/ndb/search/?', params = search_payload)
    print (search_request.url)
    searchresults = json.loads(search_request.text)
    foodndbno = searchresults['list']['item'][0]["ndbno"]
    nutrients_payload = {'ndbno': foodndbno, 'type': 'b', 'format': 'json', 'api_key': 'AY1U6UdBQKwgOcvSaQVhLqcu5QdHagIPWgAQvHtU'}
    nutrients_request = requests.get('http://api.nal.usda.gov/ndb/reports/?', params = nutrients_payload)
    print(nutrients_request.url)

    food_data=json.loads(nutrients_request.text)
    foodname = food_data['report']['food']["name"]
    person1['food_name'].append(foodname)
    protein_added = food_data['report']['food']['nutrients'][2]["value"]
    fat_added = food_data['report']['food']['nutrients'][3]["value"]
    carbs_added = food_data['report']['food']['nutrients'][4]["value"]
    person1['current_protein'] = person1['current_protein'] + float(protein_added)
    person1['current_fat'] = person1['current_fat'] + float(fat_added)
    person1['current_carbs'] = person1['current_carbs'] + float(carbs_added)
    
    # save data
    with open('data.json', 'w') as fp:
        json.dump(person1, fp)
    
    speech_text = "{} has been recorded. {} g of protein added, {} g of fat added, {} g of carbs added".format(food, protein_added, fat_added, carbs_added)
    return statement(speech_text)
    #send to database

#user wants to know macros
@ask.intent("CurrentMacrosIntent")
def report_macros():
    if 'CurrentMacrosIntent' in convert_errors:
        return question("Sorry, can you repeat that.")
    macros_text = "You have eaten %d g of carbs, %d g of protein, and %d g of fat." % (person1['current_carbs'], person1['current_protein'], person1['current_fat'])
    return statement(macros_text)
    #if we have time add in a feature where we calculate how many macros more they need, so just simple subtractio"

#user wants to know goal macros
@ask.intent("MacrosLeftIntent")
def goal_macros():
    carbs_defficit = person1["rec_carbs"] - person1["current_carbs"]
    fat_defficit = person1["rec_fat"] - person1["current_fat"]
    protein_defficit = person1["rec_protein"] - person1["current_protein"]
    
    if (carbs_defficit < 0 or fat_defficit < 0 or protein_defficit < 0):
        advice_text = "You have exceeded %d grams of carbs, %d, grams of fats, and %d grams of proteins" % (-1*carbs_defficit, -1*fat_defficit, -1*protein_defficit)
    elif (carbs_defficit == 0 or fat_defficit == 0 or protein_defficit == 0):
        advice_text = "You have met all of your macro goals!"
    else:
        advice_text = "You need to eat  %d grams of carbs, %d, grams of fats, and %d grams of proteins to reach your goal" % (carbs_defficit, fat_defficit, protein_defficit)
    
    return statement(advice_text)

app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
    app.run()
    app.run(debug=True)
