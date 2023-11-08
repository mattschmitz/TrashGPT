import requests

# Replace 'your_api_key_here' with your actual OpenAI API key
api_key = ''
headers = {'Content-Type': 'application/json','Authorization': f'Bearer {api_key}'}

data = {'model': 'gpt-3.5-turbo','messages': [
    {'role': 'system','content': 'You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.'}, 
    {'role': 'user','content': 'Compose a poem that explains the concept of recursion in programming.'}
    ]
}

from machine import Pin
from time import sleep

pushbutton = Pin(8, Pin.IN, Pin.PULL_UP)

while True:
    print(pushbutton.value())
    if pushbutton.value() == 0:
        response = requests.get("https://catfact.ninja/fact")
        print("Response: " + str(response.content))
    sleep(1);