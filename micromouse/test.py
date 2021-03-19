

import numpy as np
import pandas as pd
import random
import sys
import time
from maze import Maze
from maze import Maze_Learned
from planner import best_path
from planner import length_count
from mouse import Mouse
from observer import orientation_observed
from observer import coordinate_observed
from observer import destination_expectation


def mouse_test(maze, mouse, mode):
    
     
    if (mode != 'complete') and (mode != 'incomplete'):
        raise Exception('Argument Error!')

    testmaze = maze
    testmouse = mouse

     
    starting = [0,0]
    destination_final = testmaze.destinations
    location_real = starting[:]
    orientation_real = 'up'
     
    location_reference = starting[:]
    orientation_reference = orientation_real
     
    location_last = starting[:]

     

     
    num_actions_1 = 0
    length_movement_1 = 0
    num_actions_2 = 0
    length_movement_2 = 0
    num_actions_3 = 0
    length_movement_3 = 0
    exploration_time = 0
    maze_visited_observed = np.zeros((testmaze.dim_x, testmaze.dim_y), dtype = np.int32)
    maze_visited_observed[tuple(starting)] = 1
    percentage_maze_visited_observed = float(np.sum(maze_visited_observed))/(maze_visited_observed.shape[0] * maze_visited_observed.shape[1])

     

     
     

    exploration_start = time.time()

    while ((testmouse.percentage_visited < 1.0) if (mode == 'complete') else (testmouse.found_destination == False)):

         
        destination_best, direction_list, movement_list, path_list = testmouse.mouse_action(maze = testmaze, location_real = location_real, orientation_real = orientation_real)

         
         
        direction_list_observed = list()
        for direction in direction_list:
            direction_list_observed.append(orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = direction))
         
        movement_list_observed = movement_list[:]
        
         
        location_real = coordinate_observed(reference_mouse = testmouse.location_reference, reference_observed = location_reference, coordinate_mouse = testmouse.location_defined)

         
        orientation_real = orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = testmouse.orientation)

         
        location_expected = destination_expectation(maze = testmaze, starting = location_last, direction_list = direction_list_observed, movement_list = movement_list_observed)

         
        if location_real != location_expected:
            print('Warning: location_expected did not match location_real.')

         
        maze_visited_observed[tuple(location_real)] = 1
        percentage_maze_visited_observed = float(np.sum(maze_visited_observed))/(maze_visited_observed.shape[0] * maze_visited_observed.shape[1])

         
        if location_real in destination_final:
            testmouse.found_destination = True
            testmouse.destinations.append(testmouse.location_defined)

         
        num_actions_1 += (len(path_list) - 1)

         
        length_movement_1 += length_count(path_list = path_list)

         
        location_last = location_real

         
         
         
         
    
    exploration_end = time.time()
    exploration_time = exploration_end - exploration_start


     
     

    direction_list, movement_list, path_list = testmouse.return_origin()

     
     
    direction_list_observed = list()
    for direction in direction_list:
        direction_list_observed.append(orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = direction))
     
    movement_list_observed = movement_list[:]

     
    location_real = coordinate_observed(reference_mouse = testmouse.location_reference, reference_observed = location_reference, coordinate_mouse = testmouse.location_defined)

     
    orientation_real = orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = testmouse.orientation)

     
    location_expected = destination_expectation(maze = testmaze, starting = location_last, direction_list = direction_list_observed, movement_list = movement_list_observed)

     
    if location_real != location_expected:
        print('Warning: location_expected did not match location_real.')
    
     
    location_last = location_real

     
    num_actions_2 += (len(path_list) - 1)

     
    length_movement_2 += length_count(path_list = path_list)
    
     

    direction_list, movement_list, path_list = testmouse.go_destinations()

     
     
    direction_list_observed = list()
    for direction in direction_list:
        direction_list_observed.append(orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = direction))
     
    movement_list_observed = movement_list[:]

     
    location_real = coordinate_observed(reference_mouse = testmouse.location_reference, reference_observed = location_reference, coordinate_mouse = testmouse.location_defined)

     
    orientation_real = orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = testmouse.orientation)

     
    location_expected = destination_expectation(maze = testmaze, starting = location_last, direction_list = direction_list_observed, movement_list = movement_list_observed)

     
    if location_real != location_expected:
        print('Warning: location_expected did not match location_real.')
    
     
    location_last = location_real  
    
     
    num_actions_3 += (len(path_list) - 1)

     
    length_movement_3 += length_count(path_list = path_list)

     
     
     

    score = num_actions_3 + 1./30 * (num_actions_1 + num_actions_2)

    return (num_actions_1, length_movement_1, num_actions_2, length_movement_2, num_actions_3, length_movement_3, percentage_maze_visited_observed, score, exploration_time)



if __name__ == '__main__':
    '''
    Simulate the mouse in the maze multiple times and record the simulation results.
    '''

     
    column_names = ['maze', 'mode', 'intuition', 'heuristic', 'num_actions_1', 'length_movement_1', 'num_actions_2', 'length_movement_2', 'num_actions_3', 'length_movement_3', 'true_coverage', 'score', 'exploration_time', 'computation_time']
    df = pd.DataFrame(columns = column_names)

    num_tests = 10
    modes = ['complete', 'incomplete']
    intuitions = [False, True]
    heuristics = [False, True]

    for mode in modes:
        for intuition in intuitions:
            for heuristic in heuristics:
                for i in xrange(num_tests):
                    print('Simulation: %d. Mode: %s. Intuition: %s. Heuristic: %s.' %(i, mode, intuition, heuristic))
                    testmaze = Maze(str(sys.argv[1]))
                    testmouse = Mouse(memory_size = 40, movements = [0,1,2,3], heuristic = heuristic, intuition = intuition)
                    time_start = time.time()
                    result = mouse_test(maze = testmaze, mouse = testmouse, mode = mode)
                    time_end = time.time()
                    computation_time = time_end - time_start
                    df = df.append({column_names[0]: (str(sys.argv[1]).split('.')[0]).split('_')[-1], column_names[1]:mode, column_names[2]:intuition, column_names[3]:heuristic, column_names[4]:result[0], column_names[5]:result[1], column_names[6]:result[2], column_names[7]:result[3], column_names[8]:result[4], column_names[9]:result[5], column_names[10]:result[6], column_names[11]:result[7], column_names[12]:result[8], column_names[13]:computation_time}, ignore_index=True)
                     
                    print('The final score is %f.' %result[7])
                     
                    print('The computation time is %f.' %computation_time)
                     
                    df.to_csv('test_result_maze_' + (str(sys.argv[1]).split('.')[0]).split('_')[-1] + '.csv', sep=',',  index=False)