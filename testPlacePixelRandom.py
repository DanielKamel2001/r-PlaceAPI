from random import randint

import requests

url = 'http://localhost:5000'
endpoint = '/PlacePixel'
while 1:
    xval = randint(0, 31)
    yval = randint(0, 31)
    # colour = myCustomColours.colour_list[randint(0, 5)]
    colour = (randint(0, 255), randint(0, 255), randint(0, 255))
    # colour = f'{=}'.split('=')[0]
    try:
        headers = {'Content-Type': 'application/json'}

        print({'colour': colour,
               'x_pos': xval,
               'y_pos': yval,
               })
        response = requests.put(url + endpoint, json={'colour': colour,
                                                      'x_pos': xval,
                                                      'y_pos': yval,
                                                      }, headers=headers)
        if response.status_code == 200:
            print("request successful")
            print(response.text)
            # break
        else:
            print(f"request failed, status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
