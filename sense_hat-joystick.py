from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED
from signal import pause

print('ok')

# instantiate joebob.
joebob = SenseHat()

# Draw the background.
b = 182 
interval = b/8
pattern = (0, -interval, -interval, -interval, 0, interval, interval, interval)
ground = []
for i in range(8):
    b += pattern[i]
    for j in range(8):        
        b += pattern[j]
        ground.append((0, 0, b))
 
# figure has rows of cells, and the cells are RGB-alpha tuples.
empty, yellow, green = (0, 0, 0, 0), (255, 255, 0, 1), (0, 255, 0, 0.4)
duck  = [(empty, empty, empty, yellow, (255, 127, 0, 1)),
       (yellow, yellow, yellow, yellow, empty),
       (empty, yellow, yellow, yellow, empty)]
box = [(green, green), (green, green)]

direction = 'right'
figure = duck
x, y = (1,2)

# I copied the joystick event handling from the sense_hat docs.
# There are two 'clamp' functions, to accomodate differences between the width and height of the figure.
def x_clamp(value, min_value=0, max_value=8 - len(figure[0])):
    return min(max_value, max(min_value, value))
def y_clamp(value, min_value=0, max_value=8 - len(figure)):
    return min(max_value, max(min_value, value))

def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y = y_clamp(y - 1)
def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y = y_clamp(y + 1)
# Support has been added for flipping the figure, horizontally
def pushed_left(event):
    global x, direction,figure
    if direction == 'right':
        direction = 'left'
        for i, row in enumerate(figure):
            figure[i] = tuple(reversed(row))    
    if event.action != ACTION_RELEASED:
        x = x_clamp(x - 1)
def pushed_right(event):
    global x, direction, figure
    if direction == 'left':
        direction = 'right'
        for i, row in enumerate(figure):
            figure[i] = tuple(reversed(row)) 
    if event.action != ACTION_RELEASED:
        x = x_clamp(x + 1)

def refresh():
    # here, the screen is updated, whenever the joystick is moved.
    picture = [i for i in ground] 
    for i, row in enumerate(figure): # parse box tuple.
        for j, cell in enumerate(row):
            pixel = list(picture[x + j + (y + i)*8])
            for k, channel in enumerate(pixel):
                pixel[k] = int(round(cell[k]*cell[3])) + int(round( channel*(1 - cell[3])))
            picture[x + j + (y + i)*8] = tuple(pixel)
    joebob.set_pixels(picture)

joebob.stick.direction_up = pushed_up
joebob.stick.direction_down = pushed_down
joebob.stick.direction_left = pushed_left
joebob.stick.direction_right = pushed_right
joebob.stick.direction_any = refresh
refresh()
pause()
