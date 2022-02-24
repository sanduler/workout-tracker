# Name: Ruben Sanduleac
# Date: February 24, 2022
# Description: This program uses the nutritionix api to track the exercise of the individual it takes the
#              input from the user and coverts the information in corresponding form.
import os
import requests
from datetime import datetime

# the api keys and id
APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
# user information
# weight measured in pounds
USER_WEIGHT = 185
# user hieght in inches
USER_HEIGHT = 70
# age of the user measured in years
USER_AGE = 28
# user gender
USER_GENDER = "male"
# constants/conversion factors
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

# endpoint for nutrionix used to track the exercise
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
# input from the user which will used to parse the information to generate exersise data
exercise_text = input("Please enter the exercises that you did: ")

# header
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

# body with all the parameters needed for the nutrionix API
body = {
    "query": exercise_text,
    "gender": USER_GENDER,
    "weight_kg": pounds_to_kilograms(),
    "height_cm": inches_to_centimeters(),
    "age": USER_AGE,
}

# response of the post
response = requests.post(exercise_endpoint, json=body, headers=headers)
# raise status in case of an error
response.raise_for_status()
# save the data to workout data
workout_data = response.json()
# sheety endpoint API that will POST all the parsed info from nutrionix API
sheety_endpoint = "https://api.sheety.co/4e12ce3dfb8293152e16533fafb5bf29/myWorkouts/workouts"
# format the time for both the data and time which will be POST on the Google Sheets
now = datetime.now()
today_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")
# use a for loop to add the existing and requested exersises to the Google Sheets
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
    # get the response for the POST
    response = requests.post(sheety_endpoint, json=parameters)
    # raise a status in case of an error
    response.raise_for_status()
