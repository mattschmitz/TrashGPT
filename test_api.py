import requests
import json

api_key = "fill in your api key here"

url = "https://api.openai.com/v1/chat/completions"
bottle_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNOHR3L0nC-AhhfZ4HcUYJ9BF5m9X1ag5uxw&usqp=CAU"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": 'gpt-4-vision-preview',
    'messages': [
        {'role': 'system' , 'content': "You are a poetic assistant"},
        {'role': 'user', 'content': "Compose a haiku about the esp32"}
    ],
    "max_tokens": 60
}

data_with_image = {
    "model": 'gpt-4-vision-preview',
    'messages': [
        {'role': 'system', 'content': "You are an expert at identifying different types of trash"},
        {'role': 'user', 'content': [
            {'type': 'text', 'text': "What type of trash is this?"},
            {'type': "image_url", 'image_url': {'url': f"{bottle_image_url}"}}
        ]
        }
    ]
}
        

# Make the POST request
response = requests.post(url, headers=headers, json=data_with_image)

# Print the response
print ("Response: " + str(response. content))
