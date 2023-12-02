import requests
import json

OPENAI_API_KEY=""

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# IMPORTANT!!!    
# GPT-4 does not take encoded image, it takes an encoded image that is already decoded to utf-8 format

# Make the POST request
def CallApi(decodedImage):
    try:
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
                    {'type': "image_url", 'image_url': {'url': f"data:image/jpeg;base64,{decodedImage}"}}
                ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data_with_image)
    except Exception as e:
        print("Reached Exception in CallApi()")
        print(str(e))
        return
    return ("Response: " + str(response.content))