import requests

url = 'http://127.0.0.1:5000/results'
headers = {'Content-Type': 'application/json'}
data = {"occupations": "Freelance I Editorial  Communication  Social media et fondateur de Histoire de Rue, Social Media Manager | Créateur de contenu, Head of Content & Communication | Content Strategy | Social Media | Digital Communication | French Government | France Televisions, Social Media - Content Manager CentraleSupélec"}

try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Raises an exception for 4xx or 5xx errors
except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")
else:
    print(f"Response status code: {response.status_code}")
    try:
        response_json = response.json()
    except ValueError as e:
        print(f"Error decoding response JSON: {e}")
    else:
        print(f"Response JSON: {response_json}")
