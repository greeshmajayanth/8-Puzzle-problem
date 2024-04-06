Name - Greeshma Jayanth
UTA ID - 1002084507

Programming language used - Python 3.10.6 

Structure of the program:
expense_8_puzzle.py - main file that takes in the arguments from the command line and passes it on to the algorithm mentioned

informed_searches folder - contains the files of informed searches, i.e - Greedy search and A* search 

uninformed_searches folder - contains the files of uninformed searches, i.e - BFS, DFS, UCS, DLS, IDS

start.txt - Contains the start node of the puzzle

goal.txt - Contains the goal node of the puzzle

How to run the code:
Extract the files from the zip folder

Enter the gxj4507_assmt1 folder - cd gxj4507_assmt1

run command - 'python expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>'

method can be bfs, dfs, ucs, dls, ids, greedy, a* or empty

dumpflag can be true, false or empty

example command - python expense_8_puzzle.py start.txt goal.txt bfs true