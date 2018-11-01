#!/bin/python

import sys


class Vertex:
    def __init__(self, i, j, t):
        self.name = (i, j)
        self.value = t

class Graph:
    def __init__(self, matrix):
        self.data = {}

        # Here parse the values and create the graph
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                v = Vertex(i,j,col)
                self.data[v] = []

                # Now get the neighbours
                


def main():

    # Check for input file
    if (len(sys.argv) < 2):
        print('Please supply the input file name')
        return

    graph = []


# Invoke main.
if __name__ == "__main__":
    main()
