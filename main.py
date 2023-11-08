import requests

response = requests.get("https://catfact.ninja/fact") # make the api call

print("Response: " + str(response.content))