import requests

url = 'http://localhost:5000'
endpoint = '/DeletePixel'

headers = {'Content-Type': 'application/json'}
x=0
for y in range(0, 32):


        response = requests.delete(url + endpoint, json={'x_pos': x,
                                                     'y_pos': y}, headers=headers)
        x+=1

        print(response.text)
