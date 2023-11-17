import requests

url = 'http://localhost:5000'
endpoint = '/DeletePixel'

headers = {'Content-Type': 'application/json'}
for y in range(0, 33):
    for x in range(0, 33):

        response = requests.delete(url + endpoint, json={'x_pos': x,
                                                     'y_pos': y}, headers=headers)

        print(response.text)
