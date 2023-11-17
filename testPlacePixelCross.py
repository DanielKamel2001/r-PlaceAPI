import requests

url = 'http://localhost:5000'
endpoint = '/PlacePixel'
colour = (0, 0, 0)  # Black

yval = 0
for xval in range(0, 32, 1):
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
            yval += 1
        else:
            print(f"request failed, status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

xval = 0
for yval in range(32, -1, -1):
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
            xval += 1
        else:
            print(f"request failed, status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
