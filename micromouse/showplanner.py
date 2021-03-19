

import turtle
import sys
import os
from maze import Maze
from planner import best_path
from planner import length_count

if __name__ == '__main__':
    '''
    This function uses Python's turtle library to present the animation of micromouse solving the maze given as an argument when running the script.
    '''

     
    testmaze = Maze(str(sys.argv[1]))

	 
    starting = [0,0]
    movements = [0,1,2,3]

	 
    direction_list, movement_list, path_list = best_path(maze = testmaze, starting = starting, destinations = testmaze.destinations, movements = movements)

     
    window = turtle.Screen()
    wally = turtle.Turtle()
     
     
    wally.speed(0)
     
    wally.width(3)
     
    wally.shape('arrow')
    wally.hideturtle()
    wally.penup()
     
    wally.tracer(0, 0)

     
    sq_size = 30
    label_size = 20
    origin_x = testmaze.dim_x * sq_size / -2
    origin_y = testmaze.dim_y * sq_size / -2

     
    for x in range(testmaze.dim_x):
        for y in range(testmaze.dim_y):
            if not testmaze.is_permissible([x,y], 'up'):
                wally.goto(origin_x + sq_size * x, origin_y + sq_size * (y+1))
                 
                 
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            if not testmaze.is_permissible([x,y], 'right'):
                wally.goto(origin_x + sq_size * (x+1), origin_y + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

             
            if y == 0 and not testmaze.is_permissible([x,y], 'down'):
                wally.goto(origin_x + sq_size * x, origin_y)
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

             
            if x == 0 and not testmaze.is_permissible([x,y], 'left'):
                wally.goto(origin_x, origin_y + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

     
    for destination in testmaze.destinations:
        wally.goto(origin_x + sq_size * destination[0] + (sq_size - label_size) / 2, origin_y + sq_size * destination[1] + (sq_size - label_size) / 2)
        wally.color('','red')
        wally.begin_fill()
        wally.setheading(0)
        wally.forward(label_size)
        wally.setheading(90)
        wally.forward(label_size)
        wally.setheading(180)
        wally.forward(label_size)
        wally.setheading(270)
        wally.forward(label_size)
        wally.end_fill()

     
    wally.goto(origin_x + sq_size * starting[0] + (sq_size - label_size) / 2, origin_y + sq_size * starting[1] + (sq_size - label_size) / 2)
    wally.color('','green')
    wally.begin_fill()
    wally.setheading(0)
    wally.forward(label_size)
    wally.setheading(90)
    wally.forward(label_size)
    wally.setheading(180)
    wally.forward(label_size)
    wally.setheading(270)
    wally.forward(label_size)
    wally.end_fill()

     
     
    wally.goto(origin_x + sq_size * starting[0] + sq_size / 2, origin_y + sq_size * starting[1] + sq_size / 2)
    wally.color('orange')
    wally.setheading(90)
    wally.tracer(1, 200)
    wally.showturtle()
    wally.pendown()
     
    direction_dict = {'up': 90, 'down': 270, 'left': 180, 'right': 0}
    for direction, movement in zip(direction_list, movement_list):
        wally.setheading(direction_dict[direction])
        wally.forward(movement * sq_size)

     
    print('Given movement length options of 0, 1, 2 and 3, the least number of actions is %d.' % (len(path_list) - 1))

     
    result_directory = 'result/'
    if not os.path.exists('result/'):
        os.makedirs('result/')

    file_name = str(sys.argv[1]).split('.')[0] + '_optimial' + '.eps'
    ps = window.getcanvas().postscript(file = result_directory + file_name)

    window.exitonclick()
