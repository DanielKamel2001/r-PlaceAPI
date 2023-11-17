import base64
import requests

url = 'http://localhost:5000'
endpoint = '/ImagePlace'

image_path = "testImage.jpg"

# open image file and convert to base64 String
#  file (r- read, b- binary mode) -> bytes -> base64 encoded bytes -> decode to string
imageB64String = base64.b64encode(open(image_path, 'rb').read()).decode('utf-8')


headers = {'Content-Type': 'application/json'}

response = requests.post(url + endpoint,json={'imageBase64String':imageB64String,
                                              'x_pos':16,
                                              'y_pos':16},headers=headers)

# Print the response from the server
print(response.text)
