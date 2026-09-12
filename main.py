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

point_slider = Slider(screen, 20, screen.height - 100, 100, 20, min=5, max=90, step=3, initial= 45)
point_output = TextBox(screen, point_slider.getX(), point_slider.getY() + 20, 50, 50, fontSize=20)

num_slider = Slider(screen, 20, point_slider.getY() - 100, 100, 20, min=0, max=2, step=1, initial= 2)
num_output = TextBox(screen, num_slider.getX(), num_slider.getY() + 20, 50, 50, fontSize=20)

point_output.disable()
num_output.disable()

circ_rad = 150

font = pg.font.Font("ValveOccult-SemiBold.ttf", 30)
# TODO
# numbers using the points :P
# lines moving cooly
# lerp or whatever to other colors


def main():
    running = True
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # background, events thingy, define slider vals now so i can do function stuff and the current time as we have a clock no?
        events = pg.event.get()
        screen.fill(background_color)
        point_slider_val= point_slider.getValue()
        num_slider_val = num_slider.getValue()
        curtime = datetime.now()

        # use function to find each point for lines
        points = find_circle_points(circ_rad, point_slider_val)

        # slider outputs
        point_output.setText(point_slider_val)
        num_output.setText(num_slider_val)

        # draw the lines using the vectors from our function
        pg.draw.lines(screen, #sets the color to the opposite of the background maybe idk
                      (oppo_background(background_color)),
                      True,
                      points,
                      width=5)

        middle = pg.Vector2(screen.width/2, screen.height/2)
        for hand in "smh": # smh cause seconds minutes hours for hands
            pg.draw.aaline(screen,
                           (oppo_background(background_color)),
                           middle, get_line_point(circ_rad, curtime, hand),
                           width=3)
        text = font.render(f"Time: [{curtime.strftime('%H')}:{curtime.strftime('%M')}:{curtime.strftime('%S')}]", True, (oppo_background(background_color)))
        screen.blit(text, (screen.width/2-text.width/2, 500))

        pygame_widgets.update(events)
        pg.display.update()

        pg.display.flip()

        clock.tick(60)

    pg.quit()

# uses a radius and a chosen interval to set points on the circle
def find_circle_points(r, degree_interval):
    points = []
    cur_degree = 0

    middle_x = screen.width/2
    middle_y = screen.height/2

    while cur_degree <= 360:
        angle = math.radians(cur_degree)
        x = middle_x + r * math.cos(angle) # midpoint_x + radius * cos(angle)
        y = middle_y + r * math.sin(angle) # think really hard
        points.append(pg.Vector2(x,y))
        cur_degree += degree_interval

    return points

def oppo_background(background):
    return (255 - background[0]),(255 - background[1]),(255 - background[2])

def get_line_point(r,time, type):
    middle_x = screen.width / 2
    middle_y = screen.height / 2
    if type == 's':
        angle = math.radians(6 * time.second)
        x = middle_x + (r - r/3) * math.cos(angle)
        y = middle_y + (r - r/3) * math.sin(angle)
        point = pg.Vector2(x, y)
    if type == 'm':
        angle = math.radians(6 * time.minute)
        x = middle_x + (r - r/5) * math.cos(angle)
        y = middle_y + (r - r/5) * math.sin(angle)
        point = pg.Vector2(x, y)
    if type == 'h':
        angle = math.radians(0.5 * (60 * time.hour + time.minute))
        x = middle_x + (r - r/10) * math.cos(angle)
        y = middle_y + (r - r/10) * math.sin(angle)
        point = pg.Vector2(x, y)

    return point

if __name__ == "__main__":
    main()