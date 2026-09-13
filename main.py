import math
from datetime import datetime
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
import pygame as pg


pg.init()
screen = pg.display.set_mode((1000,700))
pg.display.set_caption('The Big Ugly Clock')

icon = pg.image.load('clock_logo.svg').convert()
icon = pg.transform.smoothscale(icon, (512, 512))
icon.set_colorkey((0,0,0))
pg.display.set_icon(icon)

background_colors_dict = {"Light": (207, 207, 207),
                     "Dark": (255-207,255-207,255-207),
                     "Crimson": (197, 18, 54),
                     "Violet":  (148,0,255),
                     "Deadlock": (238, 223, 190)}

num_vals_dict = {0: 2,
                 1: 4,
                 2: 12}

clock = pg.time.Clock()
running = True

main_font = pg.font.Font("ValveOccult-SemiBold.ttf", 30)
num_font = pg.font.Font("ValveOccult-SemiBold.ttf", 15)

background_dropdown = Dropdown(screen,
                               20, 20, 80, 30,
                               choices=[
                                   'Light',
                                   'Dark',
                                   'Crimson',
                                   'Violet',
                                   'Deadlock',
                               ],
                               name="Light", font=num_font, textHAlign="centre")



circ_rad = 150
# TODO
# lerp or whatever to other colors
# zero numbers effect (duh)

def main():
    background_color = (207, 207, 207)
    running = True
    point_slider = Slider(screen, 20, screen.get_height() - 100, 100, 20, min=5, max=90, step=3, initial=45,
                          colour=background_color, point_slider=oppo_background(background_color))
    point_output = TextBox(screen, point_slider.getX(), point_slider.getY() + 20, point_slider.getWidth(), point_slider.getHeight()+20,
                           fontSize=25, textHAlign= "centre")

    num_slider = Slider(screen, 20, point_slider.getY() - 100, 100, 20, min=0, max=2, step=1, initial=2,
                        colour=background_color, point_slider=oppo_background(background_color)) # state 0: 2 numbers (12 and 6), State 1: 4 numbers (12, 3, 6, 9), State 3: allem numbers
    num_output = TextBox(screen, num_slider.getX(), num_slider.getY() + 20, num_slider.getWidth(), num_slider.getHeight() + 20,
                         fontSize=25, textHAlign="centre")

    point_output.disable()
    num_output.disable()

    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        # background, color, define slider vals now so i can do function stuff and the current time as we have a clock no?
        for x in background_colors_dict:
            if x == background_dropdown.getSelected():
                background_color = background_colors_dict[f"{x}"]
        screen.fill(background_color)
        point_slider_val= point_slider.getValue()
        num_slider_val = num_slider.getValue()
        curtime = datetime.now()
        middle = pg.Vector2(screen.get_width()/2, screen.get_height()/2)

        # use function to find each point for lines
        points = find_circle_points(middle, circ_rad, point_slider_val)

        if points[0] != points[len(points)-1]:
            circle_closing = True
        else: circle_closing = False

        # slider outputs
        point_output.setText(point_slider_val)
        num_output.setText(num_vals_dict[num_slider_val])

        # draw the lines using the vectors from our function
        pg.draw.lines(screen,
                      (oppo_background(background_color)),
                      circle_closing,
                      points,
                      width=5)

        # Hands
        for hand in "smh": # smh cause seconds minutes hours for hands
            pg.draw.aaline(screen,
                           (oppo_background(background_color)),
                           middle, get_line_point(middle, circ_rad, curtime, hand))

        # the time text
        text = main_font.render(f"Time: [{curtime.strftime('%H')}:{curtime.strftime('%M')}:{curtime.strftime('%S')}]", True, (oppo_background(background_color)))

        # display the numbers
        clock_numbers = range(1,13)
        clock_num_points = find_num_points(middle, circ_rad, num_slider_val)
        if len(clock_num_points) == 2:
            for num in range(2):
                temp_text = num_font.render(f"{clock_numbers[num*6 + 5]}", True, (oppo_background(background_color)))
                screen.blit(temp_text, (clock_num_points[num].x - temp_text.get_width() / 2, clock_num_points[num].y - temp_text.get_height()/2))
        if len(clock_num_points) == 4:
            for num in range(4):
                temp_text = num_font.render(f"{clock_numbers[num*3 + 2]}", True, (oppo_background(background_color)))
                screen.blit(temp_text, (clock_num_points[num].x - temp_text.get_width() / 2, clock_num_points[num].y - temp_text.get_height()/2))
        if len(clock_num_points) == 12:
            for num in range(12):
                temp_text = num_font.render(f"{clock_numbers[(num+2) % 12]}", True, (oppo_background(background_color))) #thank you https://stackoverflow.com/questions/47880511/python-loop-back-to-beginning-of-list
                screen.blit(temp_text, (clock_num_points[num].x - temp_text.get_width() / 2, clock_num_points[num].y - temp_text.get_height()/2))


        screen.blit(text, (screen.get_width()/2-text.get_width()/2, middle.y+circ_rad))

        pygame_widgets.update(events)
        pg.display.update()

        pg.display.flip()

        clock.tick(60)

    pg.quit()

# uses a radius and a chosen interval to set points on the circle
def find_circle_points(middle, r, degree_interval):
    points = []
    cur_degree = 0

    while cur_degree <= 360:
        angle = math.radians(cur_degree)
        x = middle.x + r * math.cos(angle) # midpoint_x + radius * cos(angle)
        y = middle.y + r * math.sin(angle) # think really hard
        points.append(pg.Vector2(x,y))
        cur_degree += degree_interval

    return points


def find_num_points(middle, r, state):
    nums = []
    r_adj = r - r/5
    curr_angle = 0
    if state == 0:
        for num in range(2):
            angle = math.radians(curr_angle+90)
            x = middle.x + r_adj * math.cos(angle)
            y = middle.y + r_adj * math.sin(angle)
            nums.append(pg.Vector2(x, y))
            curr_angle += 180
    if state == 1:
        for num in range(4):
            angle = math.radians(curr_angle)
            x = middle.x + r_adj * math.cos(angle)
            y = middle.y + r_adj * math.sin(angle)
            nums.append(pg.Vector2(x, y))
            curr_angle += 90
    if state == 2:
        for num in range(12):
            angle = math.radians(curr_angle)
            x = middle.x + r_adj * math.cos(angle)
            y = middle.y + r_adj * math.sin(angle)
            nums.append(pg.Vector2(x, y))
            curr_angle += 30
    return nums

#sets the color to the opposite of the background maybe idk
def oppo_background(background):
    return (255 - background[0]),(255 - background[1]),(255 - background[2])

# pretty much the same shit as the find circle points one but uses this for finding the angle: https://envyen.com/tools/misc/clock-angle/
def get_line_point(middle, r, time, type):
    middle_x = middle.x
    middle_y = middle.y
    if type == 's':
        angle = math.radians((6 * time.second)-90)
        x = middle_x + (r - r/2.2) * math.cos(angle)
        y = middle_y + (r - r/2.2) * math.sin(angle)
        point = pg.Vector2(x, y)
    if type == 'm':
        angle = math.radians((6 * time.minute)-90)
        x = middle_x + (r - r/3) * math.cos(angle)
        y = middle_y + (r - r/3) * math.sin(angle)
        point = pg.Vector2(x, y)
    if type == 'h':
        angle = math.radians((0.5 * (60 * time.hour + time.minute))-90)
        x = middle_x + (r - r/5) * math.cos(angle)
        y = middle_y + (r - r/5) * math.sin(angle)
        point = pg.Vector2(x, y)

    return point


if __name__ == "__main__":
    main()