#!/bin/python

import sys

class Graph:
    def __init__(self, matrix):
        self.data = {}
        self.row = len(matrix)
        self.col = len(matrix[0])

        # Here parse the values and create the graph
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col == 1:
                    continue
                v = (i,j)
                self.data[v] = []

                # Now get the neighbours
                # Left 
                if j > 0 and matrix[i][j-1] == 0:
                    left_neighbour = (i,j-1)
                    self.data[v].append(left_neighbour)
                # Right 
                if j < len(matrix[0])-1 and matrix[i][j+1] == 0:
                    right_neighbour = (i,j+1)
                    self.data[v].append(right_neighbour)
                # Down
                if i < len(matrix)-1 and matrix[i+1][j] == 0:
                    down_neighbour = (i+1,j)
                    self.data[v].append(down_neighbour)
                # Up 
                if i > 0 and matrix[i-1][j] == 0:
                    upper_neighbour = (i-1,j)
                    self.data[v].append(upper_neighbour)

    def sort_bfs(self):
        for el in self.data:
            self.data[el].sort(key= lambda x: x[0] * self.col + x[1], reverse=True)
    
    def sort_dfs(self):
        for el in self.data:
            self.data[el].sort(key= lambda x: x[0] * self.col + x[1], reverse=False)
    
    def print_graph(self):
        for key in self.data:
            print('Key:', key, end = " ----> ")
            for value in self.data[key]:
                print(value, end=" ")
            print()

# Breadth First Search
def bfs(g,start,dest):
    # Sort the elements for queue order (ascending)
    g.sort_bfs()

    # Initialize the is visited matrix.
    is_visited = [[0 for x in range(g.col)] for x in range(g.row)]
    
    # Mark start as visited
    is_visited[start[0]][start[1]] = 1
    
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        # Get the last node from the path
        node = path[-1]
        if node == dest:
            break
        for neighbour in g.data[node]:
            if is_visited[neighbour[0]][neighbour[1]] == 0:
                is_visited[neighbour[0]][neighbour[1]] = 1
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    print_matrix(is_visited)
    print(len(path))
    print_list(path)
    print((len(path) - 1) * 1.0)

def dfs(g,start,dest):
    # Sort the elements for stack order (descending)
    g.sort_bfs()
    # Initialize the is visited matrix.
    is_visited = [[0 for x in range(g.col)] for x in range(g.row)]
    
    # Push the first element into the stack
    stack = [(start)]
    while stack:
        node = stack[-1]

        # If the node is not visited
        if is_visited[node[0]][node[1]] == 0:
            # Mark as visited
            is_visited[node[0]][node[1]] = 1

        if node == dest:
            break

        remove_from_stack = True
        
        for next_node in g.data[node]:
            if is_visited[next_node[0]][next_node[1]] == 0:
                stack.extend([next_node])
                remove_from_stack = False
                break
        if remove_from_stack:
            stack.pop()

    print_matrix(is_visited)
    
def print_list(l):
    for el in l:
        print(el[0],el[1])

def print_matrix(matrix):
    for i, row in enumerate(matrix):
        for col in range(len(row)):
            print(matrix[i][col], end=" ")
        print()

def main():

    # Check for input file
    if (len(sys.argv) < 2):
        print('Please supply the input file name')
        return

    # Read file and fill fields
    filename = sys.argv[1]

    with open(filename) as f:
        start_x, start_y = (int(x) for x in next(f).split())
        start = (start_x,start_y)

        dest_x, dest_y = (int(x) for x in next(f).split())
        dest = (dest_x,dest_y)

        matrix = []
        for line in f:
            matrix.append([int(x) for x in line.split()])

    print('Start: ', start)
    print('Destination: ', dest)

    graph = Graph(matrix)
    # graph.print_graph()
    # bfs(graph,start,dest)
    dfs(graph,start,dest)
# Invoke main.
if __name__ == "__main__":
    main()
