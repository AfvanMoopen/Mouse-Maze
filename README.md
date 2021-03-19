 
### Mouse Maze Solver 

 
 ## Codes
- maze.py   
  This script contains functions for constructing the maze objects.
- mouse.py  
  This script establishes the micromouse class controlling the actions of miromouse.
- observer.py
  This script contains some functions for micromouse movement visualization.
- planner.py
  This script contains the functions that decide micromouse's actions.
- showmaze.py
  This script can be used to create a visual demonstration of what a maze looks like.
  To run showmaze.py, run the following command in the shell:
  ```shell
  python showmaze.py test_maze_01.txt
  ```
- showmouse.py
  This script can be used to create a visual demonstration of how micromouse is exploring and solving the maze.
  To run showmouse.py, run the following command in the shell:
  ```shell
  python showmouse.py test_maze_01.txt complete
  ```
  or
  ```shell
  python showmouse.py test_maze_01.txt incomplete
  ```
  where "complete" and "incomplete" designate the strategy of micromouse.
  Please also remember to hit "Enter" once in the shell to start the micromouse
- showplanner.py
  This script can be used to create a visual demonstration of the optimal actions of micromouse in the maze.
  To run showplanner.py, run the following command in the shell:
  ```shell
  python showplanner.py test_maze_01.txt
  ```
- test.py
  This script allows you to test your micromouse in different modes on different mazes.
  To run test.py, run the following command in the shell:
  ```shell
  python test.py test_maze_01.txt
  ```
  
