# Ruben Sanduleac
import os
import requests
from datetime import datetime

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
USER_WEIGHT = 185
USER_HEIGHT = 70
USER_AGE = 28
USER_SEX = "male"
USER_GENDER = "male"
LB_CONSTANT = 2.20462262
INCH_CONSTANT = 0.393701


def pounds_to_kilograms():
    """Converts the user weight from pounds to kilograms
    Then returns the weight as a string to be used in the body"""
    kilograms = str(USER_WEIGHT / LB_CONSTANT)
    return kilograms


def inches_to_centimeters():
    """Converts the users height from inches to kilograms
    Then returns the weight as a string to be used in the body"""
    centimeters = str(USER_HEIGHT / INCH_CONSTANT)
    return centimeters


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Please enter the exercises that you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

body = {
    "query": exercise_text,
    "gender": USER_SEX,
    "weight_kg": pounds_to_kilograms(),
    "height_cm": inches_to_centimeters(),
    "age": USER_AGE,
}

response = requests.post(exercise_endpoint, json=body, headers=headers)
response.raise_for_status()
workout_data = response.json()

# TODO Setup the Sheety API
# TODO Save the data from nutrionix to sheets
# TODO Authenticate the Sheety API

sheety_endpoint = "https://api.sheety.co/4e12ce3dfb8293152e16533fafb5bf29/myWorkouts/workouts"
now = datetime.now()
today_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")
print(current_time)

for exercise in workout_data["exercises"]:
    parameters = {
      "workout": {
          "date": today_date,
          "time": current_time,
          "exercise": (exercise["name"]).title(),
          "duration": exercise["duration_min"],
          "calories": exercise["nf_calories"],
        }
    }
    response = requests.post(sheety_endpoint, json=parameters)
    response.raise_for_status()
