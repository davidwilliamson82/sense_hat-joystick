from sense_hat import SenseHat, ACTION_HELD, ACTION_RELEASED
from signal import pause

print('ok')

# instantiate joebob.
joebob = SenseHat()

# Draw the background.
b = 120 
interval = b/10
pattern = (0, -interval, -interval, -interval, 0, interval, interval, interval)
ground = []
for i in range(8):
    b += pattern[i]
    for j in range(8):        
        b += pattern[j]
        ground.append((0, 0, b))
 
# ball has rows of cells, and the cells are RGB tuples.
# TODO: alpha channel support
ball = (((0, 255, 0), (0, 255, 0)), ((0, 255, 0), (0, 255, 0)))
x, y = (3, 3)

# I copied the joystick event handling from the sense_hat docs.
def clamp(value, min_value=0, max_value=6):
    return min(max_value, max(min_value, value))

def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y - 1)

def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y + 1)

def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x - 1)

def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x + 1)

def refresh():
    # here, the screen is updated, whenever the joystick is moved.
    picture = [i for i in ground] 
    for i, row in enumerate(ball): # parse ball tuple.
        for j, cell in enumerate(row):
            picture[x + j + (y + i)*8] = cell 
    joebob.set_pixels(picture)

joebob.stick.direction_up = pushed_up
joebob.stick.direction_down = pushed_down
joebob.stick.direction_left = pushed_left
joebob.stick.direction_right = pushed_right
joebob.stick.direction_any = refresh
refresh()
pause()
