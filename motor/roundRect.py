import cairo
import math

# Creating function for make roundrect shape
def roundrect(context, x, y, width, height, r):
    context.arc(x+r, y+r, r,
                math.pi, 3*math.pi/2)

    context.arc(x+width-r, y+r, r,
                3*math.pi/2, 0)

    context.arc(x+width-r, y+height-r,
                r, 0, math.pi/2)

    context.arc(x+r, y+height-r, r,
                math.pi/2, math.pi)

    context.close_path()
    # creating a SVG surface
    # here geek95 is file name &
    # 700, 700 is dimension