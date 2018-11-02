#!/bin/python

import sys


class Vertex:
    def __init__(self, i, j, t):
        self.name = (i, j)
        self.value = t

    def __str__(self):
        return str(self.name)

'''
    def __eq__(self,other):
        return self.name[0] == other.name[0] and self.name[1] == other.name[1]
'''

class Graph:
    def __init__(self, matrix):
        self.data = {}
        self.vertices = []
        self.row = len(matrix)
        self.col = len(matrix[0])

        # Here parse the values and create the graph
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col == 1:
                    continue
                v = Vertex(i,j,col)
                self.data[v] = []

                # Now get the neighbours
                # Left 
                if j > 0 and matrix[i][j-1] == 0:
                    left_neighbour = Vertex(i,j-1,matrix[i][j-1])
                    self.data[v].append(left_neighbour)
                # Right 
                if j < len(matrix[0])-1 and matrix[i][j+1] == 0:
                    right_neighbour = Vertex(i,j+1,matrix[i][j+1])
                    self.data[v].append(right_neighbour)
                # Down
                if i < len(matrix)-1 and matrix[i+1][j] == 0:
                    down_neighbour = Vertex(i+1,j,matrix[i+1][j])
                    self.data[v].append(down_neighbour)
                # Up 
                if i > 0 and matrix[i-1][j] == 0:
                    upper_neighbour = Vertex(i-1,j,matrix[i-1][j])
                    self.data[v].append(upper_neighbour)

    def sort_bfs(self):
        for el in self.data:
            self.data[el].sort(key= lambda x: x.name[0] * self.col + x.name[1], reverse=True)
    
    def sort_dfs(self):
        for el in self.data:
            self.data[el].sort(key= lambda x: x.name[0] * self.col + x.name[1], reverse=False)
    
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
    
    queue = [start]
    path = []
    while queue:
        node = queue.pop(0)
        is_visited[node[0]][node[1]] = 1
        path.append(node)
        if node == dest:
            break
        print(g.data)
        queue = queue + g.data[node]

    print(is_visited)
    print(len(path))
    print(path)
    print((len(path) - 1) * 1.0)

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
    graph.print_graph()
    print('--------------------------')
    bfs(graph,start,dest)
# Invoke main.
if __name__ == "__main__":
    main()
