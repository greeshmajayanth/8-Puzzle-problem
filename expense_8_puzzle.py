import sys

from uninformed_searches.bfs import bfs_search
from uninformed_searches.dfs import dfs_search
from uninformed_searches.ucs import ucs_search
from uninformed_searches.dls import dls_search
from uninformed_searches.ids import ids_search
from informed_searches.greedy import greedy_search
from informed_searches.a_star import astar_search


def main():

    #Obtain information from calling parameters
    n = len(sys.argv)                             #Get the length of arguments to check if any method is mentioned

    method = ''                                   #Initialise a variable to check the method for search
    dumpflag = False                              #Initialise a variable to get the dump flag value

    if n == 5 :
        method = str(sys.argv[3])                 #Getting the method from the arguments
        if str(sys.argv[4]) == 'true':
            dumpflag = True
    
    if n == 4:
        if str(sys.argv[3]) == 'true':
            dumpflag = True
        else:
            method = str(sys.argv[3])

    #Build initial board state
    InitialState = []
    for line in open(sys.argv[1]).readlines():         #To read the start file
        singleLine1 = []
        for i in line.split():
            if i != 'END' and i != 'OF' and i != 'FILE':
                singleLine1.append(int(i))
        if singleLine1 != []:
            InitialState.append(singleLine1)

    #Build goal state
    GoalState = []
    for line in open(sys.argv[2]).readlines():         #To read the goal file
        singleLine2 = []
        for i in line.split():
            if i != 'END' and i != 'OF' and i != 'FILE':
                singleLine2.append(int(i))
        if singleLine2 != []:
            GoalState.append(singleLine2)
    

    if method != '':
        if method == 'bfs':
            result = bfs_search(InitialState, GoalState, dumpflag)
        elif method == 'dfs':
            result = dfs_search(InitialState, GoalState, dumpflag)
        elif method == 'ucs':
            result = ucs_search(InitialState, GoalState, dumpflag)
        elif method == 'dls':
            result = dls_search(InitialState, GoalState, dumpflag)
        elif method == 'ids':
            result = ids_search(InitialState, GoalState, dumpflag) 
        elif method == 'greedy':
            result = greedy_search(InitialState, GoalState, dumpflag)
        elif method == 'a*':
            result = astar_search(InitialState, GoalState, dumpflag) 
        else:
            print("Invalid method")
    else:
        result = astar_search(InitialState, GoalState, dumpflag)
 
    cost = 0
    for i in result[5]:
        cost = cost + i[1]                                   #To calculate cost of the search

    #To print all the results
    print("Nodes Popped: ",result[0])
    print("Nodes Expanded: ",result[1])
    print("Nodes Generated: ",result[2])
    print("Max Fringe size: ",result[3])
    print("Soloution Found at depth " + str(result[4]) + " with cost of " + str(cost))
    print("Steps: ")
    for j in result[5]:
        print("Move " + str(j[1]) + " " + j[0] + "\n")

if __name__ == '__main__':
    main()