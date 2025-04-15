from django.test import TestCase
import requests

request = requests.get('http://localhost:8000/api/')

print(request.json())


