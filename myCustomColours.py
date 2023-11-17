black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green= (0,128,0)
blue = (0,0,255)
yellow= (255,255,0)

colour_list = [black
               ,white
               ,red
               ,green
               ,blue
               ,yellow]
def stringToColour(colour_name):
    colour_name = str.lower(colour_name)
    if(colour_name == 'black'):
        return black
    elif(colour_name == 'white'):
        return white
    elif(colour_name == 'red'):
        return red
    elif(colour_name == 'green'):
        return green
    elif(colour_name == 'blue'):
        return blue
    elif(colour_name == 'yellow'):
        return yellow
    else:
        raise Exception("invalid Colour name")