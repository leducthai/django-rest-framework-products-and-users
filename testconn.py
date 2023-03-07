import requests

test = requests.get('http://172.23.0.3:8000/comment/?pd=1').json()

print(len(test))