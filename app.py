import base64
import threading

import pygame
from flask import Flask, send_file, request, Response

app = Flask(__name__)
# Initialize screen size, square split into block
display_width = 800
display_height = display_width
board_size = 32
block_length = display_height / board_size  # 25  # 32 blocks of length 25 pixels
background_image_filename = 'background.jpg'


@app.route('/')
def hello_world():  # put application's code here
    return ('This is a recreation or reddit\'s r/place! use our endpoints to place one pixel at a time. Note that '
            'EVERYONE can also place a pixel too\n\n'
            'There are 5 Endpoints to interact with the board'
            '\nImage'
            '\n - GET Request that returns a jpg of the current state of the board:'
            '\nPlacePixel'
            '\n - places a pixel on the screen at the given location in the given colour:'
            '\n - PUT Request that requires:'
            '\n   "x_pos" & "y_pos" where they represent x and y coordinates where (0,0) is the left-top, and (31,31) is the right-bottom'
            '\n   "colour" a tuple of 3 integers bellow 255 that represents an RGB colour'

            '\nPlaceImage'
            '\n - places an image on the screen at the given location resized to fit the allotted space:'
            '\n - POST Request that requires:'
            '\n   "x_pos" & "y_pos" where they represent x and y coordinates where (0,0) is the left-top, and (31,31) is the right-bottom'
            '\n   "imageBase64String" which represents a "jpg" image encoded in base64'

            '\nDeletePixel'
            '\n - Deletes the pixel or image on the board at the given location revealing the background image:'
            '\n - DELETE Request that requires:'
            '\n   "x_pos" & "y_pos" where they represent x and y coordinates where (0,0) is the left-top, and (31,31) is the right-bottom'
            '\nLineDraw'
            '\n - places a line of pixels on the screen at the given location acording to the shape of the line defined and in the given colour:'
            '\n - PUT Request that requires:'
            '\n   "x_pos" & "y_pos" where they represent x and y coordinates where (0,0) is the left-top, and (31,31) is the right-bottom'
            '\n         Reprsents the first pixel of the line as it\'s drawn left to right'
            '\n   "colour" a tuple of 3 integers bellow 255 that represents an RGB colour'
            '\n   "m" & "b" where they represent constants slope and offset from the equestion of a line (y=mx+b)'
            )


# Novel Feature 5
# Draws a line defined by y= mx +b where m and b are provided by the json
# also requires x_pos, y_pos, and 'length' - the amount of pixels to be drawn
# Line is drawn left to right
@app.route('/LineDraw', methods=['PUT'])
def draw_line():
    # get request data
    json_data = request.get_json()

    y = json_data['y_pos']
    x = json_data['x_pos']
    m = json_data['m']
    b = json_data['b']

    colour = tuple(json_data['colour'])
    # if the colour converts to a proper rgb tuple
    if (type(colour) == tuple and len(colour) == 3 and (colour[0] <= 255) and (colour[1] <= 255) and (
            colour[2] <= 255)):
        # draw each pixel of the line according to length
        for i in range(0, json_data['length'] + 1):

            print((x + i), (y + (x * m) + b))

            if ((x + i) >= 32 or (y + (x * m) + b) >= 32):
                break

            board[y + (x * m) + b][x] = colour
            x = x + 1

        return Response(
            "line has been drawn",
            status=200,
        )
    else:
        return Response("included colour is not a valid RGB",
                        status=400,

                        )


# Novel Feature 4
@app.route('/DeletePixel', methods=['DELETE'])
def delete_pixel():
    # get request data
    json_data = request.get_json()

    # Set nothing to display on the selected location
    board[json_data['y_pos']][json_data['x_pos']] = None

    return Response(
        "Pixel has been deleted",
        status=200,
    )


# Novel Feature 3
# Places an uploaded image onto the display
# Expects json request with imageBase64String (a jpg image encoded in a base 64 string) and the y_pos and x_pos to place
@app.route('/ImagePlace', methods=['POST'])
def image_place():
    # get request data
    json_data = request.get_json()

    # decode image as base64 string and save image
    new_filename = 'saved_images/' + 'temp.jpg'
    with open(new_filename, "wb") as fh:
        fh.write(base64.decodebytes(json_data['imageBase64String'].encode('utf-8')))

    # Load Image into pygame surface and store on board
    img = pygame.image.load(new_filename)
    img = pygame.transform.scale(img, (block_length, block_length))  # make image match slot size
    board[json_data['y_pos']][json_data['x_pos']] = img

    return Response(
        "Image has been placed",
        status=200,
    )


# Novel Feature 2 Allows users to place a pixel on the board.
# requires a json request with the colour, x_pos, y_pos values, (array->tuple of RGB values, integer, integer)
@app.route('/PlacePixel', methods=['GET', 'PUT'])
def place_pixel():
    request_params = request.get_json()
    # print(request_params)
    # colour = myCustomColours.stringToColour(request_params['colour'])
    colour = tuple(request_params['colour'])
    # if the colour converts to a proper rgb tuple
    if (type(colour) == tuple and len(colour) == 3 and (colour[0] <= 255) and (colour[1] <= 255) and (
            colour[2] <= 255)):
        board[request_params['y_pos']][request_params['x_pos']] = colour
    else:
        return Response("included colour is not a valid RGB",
                        status=400,

                        )
    return Response(
        status=200,
        mimetype="application/json"
    )


# Novel Feature 1
# Return image of the current state
@app.route('/image', methods=['GET'])
def get_place():
    response = send_file('place.JPG', mimetype='image/jpg')
    response.status_code = 200
    return response


# Function runs in a thread to manage Pygame Display. Pygame is initialized in thread as it is not normally thread safe
def manage_display():
    print("starting")
    pygame.init()

    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("The Place")

    clock = pygame.time.Clock()

    print("initialized display")

    quitting = False

    # next_draw_time = 0
    draw_delay = 500  # 0.5 seconds between frame draws

    while not quitting:

        for event in pygame.event.get():

            # print(event)
            if event.type == pygame.QUIT:
                quitting = True
                pass
            # else:

            # # draw on this loop only if it's been more than the delay time since last draw
            # current_time = pygame.time.get_ticks()
            # if current_time > next_draw_time:
            #     next_draw_time = current_time + draw_delay

        # game_display.fill(myCustomColours.black)
        background = pygame.image.load(background_image_filename)
        background = pygame.transform.scale(background, (display_width, display_height))
        game_display.blit(background, (0, 0))
        update_display(game_display, block_length)
        pygame.display.update()

        # Save the current state so it can be served later
        pygame.image.save(game_display, 'place.JPG')
        clock.tick(30)


#
def update_display(game_display, block_length_offset):
    y_pos = 0
    for row in board:
        x_pos = 0
        for column in row:
            if (column is None):
                pass
            elif (type(column) == tuple):
                pygame.draw.rect(game_display, column, (x_pos, y_pos, block_length, block_length))
            elif (type(column) == pygame.surface.Surface):
                game_display.blit(column, (x_pos, y_pos))

            x_pos += block_length_offset
        y_pos += block_length_offset
    # print("screen redraw")
    return game_display


# print(__name__) #'app', flask project run by pycharm default to this behaviour
if __name__ == 'app':  # '__main__':
    # Initialize board to be 2D array, each space represents a pixel on the board,
    # the contents being what should be drawn
    # (tuples with rgb values represent colours, otherwise it should be a pygame.surface.Surface)
    board = [[None] * 32 for i in range(32)]

    # Start the thread that creates the server display
    server_thread = threading.Thread(target=manage_display)
    server_thread.start()

    app.run()
