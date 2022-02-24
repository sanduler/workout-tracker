# Ruben Sanduleac
import os
import requests

# TODO: Create a "My Workouts" Google sheet that will be used to store all the information about the workouts.
# TODO: Use the Nutrionix API for the natural language engine
# TODO: GET the API key and access the request.

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
USER_WEIGHT = 185
USER_HEIGHT = 70
USER_AGE = 28
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
    "gender": "male",
    "weight_kg": pounds_to_kilograms(),
    "height_cm": inches_to_centimeters(),
    "age": USER_AGE,
}

response = requests.post(exercise_endpoint, params=body, headers=headers)
response.raise_for_status()
data = response.json()
print(data)
