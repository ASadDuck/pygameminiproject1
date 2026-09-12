import math
from datetime import datetime
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame as pg

pg.init()
screen = pg.display.set_mode((700, 700))
clock = pg.time.Clock()
running = True
background_color = (207, 207, 207)

slider = Slider(screen, 20, screen.height-100, 100, 20, min=5, max=90, step=3, initial= 45)
output = TextBox(screen, slider.getX(), slider.getY()+20, 50, 50, fontSize=20)

output.disable()

font = pg.font.Font("ValveOccult-SemiBold.ttf", 30)
# TODO
# numbers using the points :P
# lines moving cooly
# lerp or whatever to other colors

def find_circle_points(r, degree_interval):
    points = []
    cur_degree = 0

    middle_x = screen.width/2
    middle_y = screen.height/2

    while cur_degree <= 360:
        angle = math.radians(cur_degree)
        x = middle_x + r * math.cos(angle)
        y = middle_y + r * math.sin(angle)
        points.append(pg.Vector2(x,y))
        cur_degree += degree_interval

    return points


while running:
    events = pg.event.get()
    screen.fill(background_color)
    slider_val= slider.getValue()

    points = find_circle_points(150, slider_val)

    output.setText(slider_val)

    curtime = datetime.now()

    pg.draw.lines(screen,
                  ((255 - background_color[0]),(255 - background_color[1]),(255 - background_color[2])),
                  True,
                  points,
                  width=3)
    text = font.render(f"Time: [{curtime.strftime('%H')}:{curtime.strftime('%M')}]", True, (0, 0, 0))
    screen.blit(text, (screen.width/2-text.width/2, 500))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pygame_widgets.update(events)
    pg.display.update()

    pg.display.flip()

    clock.tick(60)

pg.quit()