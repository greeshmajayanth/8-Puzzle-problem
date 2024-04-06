from datetime import datetime

date = str(datetime.today().date())     #To get the date for dump file
time = str(datetime.today().time())     #To get the time for dump
t = str(time[0:1]+time[3:4])                      #To skip the seconds in time

class Node:
    def __init__(self, state, parent=None, action=None, moved_value=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.moved_value = moved_value
        self.depth = 0 if parent is None else parent.depth + 1

    def expand(self):
        """
        Returns a list of nodes reachable from this node's state.
        """
        successors = []
        for action in self.get_actions():
            next_state, moved_value = self.get_next_state(action)
            successors.append(Node(next_state, self, action, moved_value))
        return successors

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


def dls_search(node, goal_state, depth_limit):
    """
    Depth-limited search algorithm to find the path from node to goal_state within the given depth limit.
    Returns a tuple containing nodes_expanded, nodes_generated, and steps (a list of actions taken to get from node to goal).
    """
    if node.is_goal(goal_state):
        return 0, 1, []

    if depth_limit == 0:
        return 1, 1, None

    nodes_expanded = 0
    nodes_generated = 1
    for successor in node.expand():
        nodes_generated += 1
        nodes_exp, nodes_gen, steps = dls_search(successor, goal_state, depth_limit - 1)
        nodes_expanded += nodes_exp
        nodes_generated += nodes_gen

        if steps is not None:
            steps.append([successor.action, successor.moved_value])
            return nodes_expanded, nodes_generated, steps

    return nodes_expanded, nodes_generated, None


def ids_search(start_state, goal_state, dumpflag):
    """
    Iterative deepening search algorithm to find the shortest path from start_state to goal_state.
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

    for depth_limit in range(1, 100):  # Set a reasonable maximum depth limit
        nodes_exp, nodes_gen, steps = dls_search(start_node, goal_state, depth_limit)
        nodes_expanded += nodes_exp
        nodes_generated += nodes_gen

        if dumpflag == True :
                            with open('trace-'+date+ "-"+ t + ".txt", 'a') as f:
                                f.write("Depth limit of each itteration"+str(depth_limit)+'\n')
                                f.write("Number of nodes expanded "+str(nodes_expanded)+'\n')
                                f.write("Number of nodes Generated "+str(nodes_generated)+'\n')

        if steps is not None:
            steps.reverse()
            return [nodes_popped, nodes_expanded, nodes_generated, max_frontier_length, len(steps), steps]

    return [nodes_popped, nodes_expanded, nodes_generated, max_frontier_length, None, None, None]

