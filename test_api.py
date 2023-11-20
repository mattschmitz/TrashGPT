import requests
import json
import base64
from dotenv import load_dotenv
import os


load_dotenv() # Load the .env file
api_key = os.getenv('OPENAI_API_KEY') # Retrieve the API key from a .env file located in this repo (not committed to github)


image_path = 'test_images/apple_core.jpeg'

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# encode the image
base64_image = encode_image(image_path)

url = "https://api.openai.com/v1/chat/completions"
bottle_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNOHR3L0nC-AhhfZ4HcUYJ9BF5m9X1ag5uxw&usqp=CAU"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# data = {
#     "model": 'gpt-4-vision-preview',
#     'messages': [
#         {'role': 'system' , 'content': "You are a poetic assistant"},
#         {'role': 'user', 'content': "Compose a haiku about the esp32"}
#     ],
#     "max_tokens": 60
# }

data_with_image = {
    "model": 'gpt-4-vision-preview',
    'messages': [
        {'role': 'system', 'content': 
            '''
            You are an expert at identifying different types of trash.
            Please respond with only "recyclable", "compostable", or "landfill"
            '''
        },
        {'role': 'user', 'content': [
            {'type': 'text', 'text': "What type of trash is this?"},
            {'type': "image_url", 'image_url': {'url': f"data:image/jpeg;base64,{base64_image}"}}
        ]
        }
    ]
}
        

# Make the POST request
response = requests.post(url, headers=headers, json=data_with_image)

# Print the response
print ("Response: " + str(response. content))
