#!/bin/python

import sys


class Vertex:
    def __init__(self, i, j, t):
        self.name = (i, j)
        self.value = t

    def __str__(self):
        return str(self.name) + str(self.value)

class Graph:
    def __init__(self, matrix):
        self.data = {}
        self.vertices = []

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
    
    def print_graph(self):
        for key in self.data:
            print('Key:', key)
            for value in self.data[key]:
                print(value)
            print('____________')

def main():

    # Check for input file
    if (len(sys.argv) < 2):
        print('Please supply the input file name')
        return

    # Read file and fill fields
    filename = sys.argv[1]

    with open(filename) as f:
        start = (int(x) for x in next(f).split())
        destination = (int(x) for x in next(f).split())
        matrix = []
        for line in f:
            matrix.append([int(x) for x in line.split()])

    print('Start: ', start)
    print('Destination: ', destination)

    graph = Graph(matrix)
    graph.print_graph()

# Invoke main.
if __name__ == "__main__":
    main()
