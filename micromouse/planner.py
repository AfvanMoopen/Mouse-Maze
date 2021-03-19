

import numpy as np
import sys
from maze import Maze

def best_action(maze, utility, state, destinations, movements):
    '''
    Given a rectangle maze and its current utility values, calculate the best option to take at the state given to maximize the future reward.
    maze: Maze class. maze.walls is a numpy array containing the wall information of the maze. The wall property can only be 'wall' or 'no wall'. maze numpy array format: maze[0] - the first vertical cells in maze, maze[1] - the second vertical cells in maze, etc.
    state: the coordinates of grid which you want to find the best action on.
    utility: a numpy array containing the utility values of all the states possible in the maze.
    movements: a list of movement length allowed.
    return: the best direction to take, the best movement to take, the state after taking the action, the utility of the state after taking the action.
    '''
     
    if (state in destinations) or (maze.walls[tuple(state)] == 0):
         
        return ('up', 0, state, 0)
     
    distance_dict = dict()
    directions = ['up', 'down', 'left', 'right']
    for direction in directions:
        distance_dict[direction] = maze.dist_to_wall(cell = tuple(state), direction = direction)
     
     
     
    state_next = state
    reward_max = utility[tuple(state_next)]
    direction_best = 'up'
    movement_best = 0
    state_next_best = state_next[:]
     
    for direction in directions:
        for movement in movements:
             
            if direction == 'up':
                state_next = [state[0], state[1] + min(distance_dict['up'], movement)]
            elif direction == 'down':
                state_next = [state[0], state[1] - min(distance_dict['down'], movement)]
            elif direction == 'left':
                state_next = [state[0] - min(distance_dict['left'], movement), state[1]]
            elif direction == 'right':
                state_next = [state[0] + min(distance_dict['right'], movement), state[1]]
             
             
            if utility[tuple(state_next)] > reward_max:
                reward_max = utility[tuple(state_next)]
                direction_best = direction
                movement_best = movement
                state_next_best = state_next[:]

    return (direction_best, movement_best, state_next_best, reward_max)

def utility_calculation(maze, destinations, movements):
    '''
    Given a rectangle maze, starting point and destination point, calculate the utility value of each state.
    maze: Maze class. maze.walls is a numpy array containing the wall information of the maze. The wall property can only be 'wall' or 'no wall'. maze numpy array format: maze[0] - the first vertical cells in maze, maze[1] - the second vertical cells in maze, etc.
    destination: the coordinates of destination points. There can be multiple destination points.
    return: equilibrated utility value of each state in maze.
    '''
     
    dim_x = maze.walls.shape[0]
    dim_y = maze.walls.shape[1]
     
    utility = np.zeros((dim_x, dim_y), dtype = np.float)
     
     
    gamma = 0.95
     
    reward = np.full((dim_x, dim_y), fill_value = -1, dtype = np.int32)
     
    for x in xrange(dim_x):
        for y in xrange(dim_y):
            if maze.walls[x][y] == 0:
                reward[x][y] = (-5 * (dim_x * dim_y))
     
    for destination in destinations:
        reward[tuple(destination)] = (5 * (dim_x * dim_y))
     
     
    utility_updated = utility.copy()
    convergence_threhold = 0.00001 * (dim_x * dim_y)
    utility_difference = 0.1

    while utility_difference > convergence_threhold:
        for x in xrange(dim_x):
            for y in xrange(dim_y):
                utility_updated[x][y] = reward[x][y] + gamma * best_action(maze = maze, state = [x,y], utility = utility, destinations = destinations, movements = movements)[3]
        utility_difference = np.sum(np.square(utility_updated - utility))
        utility = utility_updated.copy()

     
     

    return utility

def best_path(maze, starting, destinations, movements):
    '''
    Given a rectangle maze, starting point and destination point, calculate the best path from starting to destination.
    maze: Maze class. maze.walls is a numpy array containing the wall information of the maze. The wall property can only be 'wall' or 'no wall'. maze numpy array format: maze[0] - the first vertical cells in maze, maze[1] - the second vertical cells in maze, etc.
    starting: the coordinates of starting point.
    destination: the coordinates of destination point. There can be multiple destination points.
    return: list of direction, list of movement, list of path
    '''
     
    utility = utility_calculation(maze = maze, destinations = destinations, movements = movements)
    
     
    action_threhold = maze.walls.shape[0] * maze.walls.shape[1]

    path_list = list()
    path_list.append(list(starting))
    direction_list = list()
    movement_list = list()

    state_last = starting
    action = best_action(maze = maze, utility = utility, state = state_last, destinations = destinations, movements = movements)
    direction_list.append(action[0])
    movement_list.append(action[1])
    path_list.append(action[2])

    while (action[2] not in destinations):
        if (len(path_list) - 1) > action_threhold:
            print('Warning: number of actions exceeds threhold!')
            print(maze.walls[tuple(destinations[0])])
            break
        state_last = action[2]
        action = best_action(maze = maze, utility = utility, state = state_last, destinations = destinations, movements = movements)
        direction_list.append(action[0])
        movement_list.append(action[1])
        path_list.append(action[2])

    return direction_list, movement_list, path_list

def length_count(path_list):
    '''
    Given a path_list, calculate the length of path.
    path_list: list of path coordinates.
    '''
    length = 0
    i = 0
    while i < (len(path_list) - 1):
         
        length += np.sum(np.absolute(np.array(path_list[i]) - np.array(path_list[i + 1])))
        i += 1
    return length

if __name__ == '__main__':

     
    testmaze = Maze(str(sys.argv[1]))

     
    starting = [0,0]
    print(' 

    print('Mathmatics Notes:')
    print('Mathematically, the series of actions costs takes number of actions might be different to the series of actions takes shortest path.')
    print('Mathematically, there might be multiple series of actions cost the same number of actions. Only one series of the actions will be presented.')
    print(' 

     
    movements = [1]
    direction_list, movement_list, path_list = best_path(maze = testmaze, starting = starting, destinations = testmaze.destinations, movements = movements)
    print('Mathematically, given this maze, the length of the shortest path to the destination is %d.' %(length_count(path_list = path_list)))

     
    movements = [0,1,2,3]

     
    direction_list, movement_list, path_list = best_path(maze = testmaze, starting = starting, destinations = testmaze.destinations, movements = movements)

    print('Given movement length options of 0, 1, 2 and 3, the least number of actions is %d.' % (len(path_list) - 1))
    print('The series of actions could be:')
    print(path_list)
    print('The length of the path to the destination is %d.' % (length_count(path_list = path_list)))











