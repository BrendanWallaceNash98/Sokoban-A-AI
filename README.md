# Sokoban-A-AI
Sokoban is an interesting challenge for the field of artificial intelligence largely due to its difficulty. Sokoban has been proven NP-hard. Sokoban is difficult not because of its branching factor, but because of the huge depth of the solutions. Many actions (box pushes) are needed to reach the goal state! However, given that the only available actions are moving the worker up, down, left or right, the branching factor is small (only 4). 

The worker can only push a single box at a time and is unable to pull any box. The boxes have individual weights. The weight of a box is taking into account when computing the cost of a push.

Files:
  - search.py contains a number of search algorithms and related classes.
  - sokoban.py contains a class Warehouse that allows you to load puzzle instances from text files.
  - sokoban_gui.py a GUI implementation of Sokoban that allows you to play and explore puzzles. This GUI program can call your planner function         solve_weighted_sokoban
  - mySokobanSolver.py Contains the main function used to solve the sokoban puzzle. Including directional functions using A* and a function to mark cell that would cause a tabboo state (a place where the ware houser cannot move)
  - sanity_check.py script to perform very basic tests on your solution. The marker will use a
different scrip
