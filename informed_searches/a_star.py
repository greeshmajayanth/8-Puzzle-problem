from queue import PriorityQueue
from datetime import datetime

date = str(datetime.today().date())     #To get the date for dump file
time = str(datetime.today().time())     #To get the time for dump
t = str(time[0:1]+time[3:4])                      #To skip the seconds in time

class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0, moved_value=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  # cost to get to this node
        self.h = h  # heuristic value of this node
        self.moved_value = moved_value

    def f(self):
        """
        Returns the sum of the cost to get to this node and the heuristic value of this node.
        """
        return self.g + self.h

    def expand(self, goal_state):
        """
        Returns a list of nodes reachable from this node's state.
        """
        successors = []
        for action in self.get_actions():
            next_state, moved_value = self.get_next_state(action)
            g = self.g + 1  # cost to get to the next node
            h = self.get_heuristic_value(next_state, goal_state)
            successors.append(Node(next_state, self, action, g, h, moved_value))
        return successors

    def __lt__(self, other):
        """
        Comparison function used to order nodes in the priority queue.
        """
        return self.g < other.g

    def get_actions(self):
        """
        Returns a list of possible actions that can be taken from this state.
        """
        actions = []
        i, j = self.get_blank_position()
        if i > 0:
            actions.append('down')
        if i < 2:
            actions.append('up')
        if j > 0:
            actions.append('right')
        if j < 2:
            actions.append('left')
        return actions

    def get_next_state(self, action):
        """
        Returns a tuple containing the state that results from taking the given action from this state
        and the value of the tile that was moved to get to the next state.
        """
        i, j = self.get_blank_position()
        if action == 'down':
            next_state = self.swap((i, j), (i - 1, j))
        elif action == 'up':
            next_state = self.swap((i, j), (i + 1, j))
        elif action == 'right':
            next_state = self.swap((i, j), (i, j - 1))
        elif action == 'left':
            next_state = self.swap((i, j), (i, j + 1))
        moved_value = next_state[i][j]
        return next_state, moved_value

    def get_blank_position(self):
        """
        Returns the position of the blank tile in this state.
        """
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def swap(self, pos1, pos2):
        """
        Returns a new state where the tiles at the given positions are swapped.
        """
        new_state = [row[:] for row in self.state]
        new_state[pos1[0]][pos1[1]], new_state[pos2[0]][pos2[1]] = new_state[pos2[0]][pos2[1]], new_state[pos1[0]][pos1[1]]
        return new_state

    def is_goal(self, goal_state):
        """
        Returns True if this state matches the goal state.
        """
        return self.state == goal_state

    def get_heuristic_value(self, state, goal_state):
        """
        Returns the heuristic value of this state, which is the sum of the Manhattan distances between each tile
        in this state and its goal position.
        """
        h = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    value = state[i][j]
                    goal_position = self.get_goal_position(value, goal_state)
                    h += abs(i - goal_position[0]) + abs(j - goal_position[1])
        return h

    def get_goal_position(self, value, goal_state):
        """
        Returns the position of the given value in the goal state.
        """
        for i in range(3):
            for j in range(3):
                if goal_state[i][j] == value:
                    return i, j

def astar_search(start_state, goal_state, dumpflag):
    """
    A* search algorithm to find the shortest path from start_state to goal_state.
    Returns a tuple containing nodes_popped, nodes_expanded, nodes_generated, max_frontier_length,
    depth, cost, and steps (a list of actions taken to get from start to goal).
    """
    start_node = Node(start_state)
    if start_node.is_goal(goal_state):
        return 0, 0, 0, 0, 0, 0, []

    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_length = 0
    visited = set()
    frontier = PriorityQueue()
    frontier.put((start_node.f(), start_node))

    while not frontier.empty():
        max_frontier_length = max(max_frontier_length, frontier.qsize())
        f, node = frontier.get()
        nodes_popped += 1
        visited.add(tuple(map(tuple, node.state)))

        for successor in node.expand(goal_state):
            if tuple(map(tuple, successor.state)) not in visited:
                if successor.is_goal(goal_state):
                    steps = []
                    while successor.parent is not None:
                        action = successor.action
                        moved_value = successor.moved_value
                        steps.append([action, moved_value])
                        successor = successor.parent
                    steps.reverse()
                    return [nodes_popped, nodes_expanded, nodes_generated, max_frontier_length, len(steps), steps]

                frontier.put((successor.g+successor.h, successor))
                nodes_generated += 1

            if dumpflag == True :
                            with open('trace-'+date+ "-"+ t + ".txt", 'a') as f:
                                f.write(str(successor)+'\n')
                                f.write("Number of nodes expanded "+str(nodes_expanded)+'\n')
                                f.write("Number of nodes Generated "+str(nodes_generated)+'\n')

        nodes_expanded += 1

    return [nodes_popped, nodes_expanded, nodes_generated, max_frontier_length, None, None, None]
