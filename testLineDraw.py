from random import randint

import requests

url = 'http://localhost:5000'
endpoint = '/LineDraw'

colour = (randint(0, 255), randint(0, 255), randint(0, 255))

headers = {'Content-Type': 'application/json'}

response = requests.put(url + endpoint, json={'m': 1,
                                               'b': 1,
                                               'length': 15,
                                               'x_pos': 1,
                                               'colour': colour,
                                               'y_pos': 3}, headers=headers)

# Print the response from the server
print(response.text)
