#!/bin/python

import sys
import math

class Vertex:
    def __init__(self,parent=None,position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self,other):
        return self.position == other.position

    def __lt__(self,other):
        if self.f == other.f:
            if self.position[0] > other.position[0]:
                return True
            elif self.position[0] < other.position[0]:
                return False
            else: 
                return self.position[1] > other.position[1]
        else:
            return self.f < other.f
            
    def __repr__(self):
        return str(self.position) + str(self.f)
class Graph:
    def __init__(self, matrix, isMountain):
        self.data = {}
        self.row = len(matrix)
        self.col = len(matrix[0])
        self.isMountain = isMountain
        self.matrix = matrix 

        # Here parse the values and create the graph
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col == 1:
                    continue
                v = (i,j)
                self.data[v] = []


                cur = matrix[i][j]

                # Now get the neighbours according to the problem type.
                if self.isMountain:
                    # Left 
                    if j > 0 and abs(matrix[i][j-1] - cur) <= 1:
                        left_neighbour = (i,j-1)
                        self.data[v].append(left_neighbour)
                    # Right 
                    if j < len(matrix[0])-1 and abs(matrix[i][j+1] - cur) <= 1:
                        right_neighbour = (i,j+1)
                        self.data[v].append(right_neighbour)
                    # Down
                    if i < len(matrix)-1 and abs(matrix[i+1][j] - cur) <= 1:
                        down_neighbour = (i+1,j)
                        self.data[v].append(down_neighbour)
                    # Up 
                    if i > 0 and abs(matrix[i-1][j] - cur) <= 1:
                        upper_neighbour = (i-1,j)
                        self.data[v].append(upper_neighbour)
                else:
                    # Left 
                    if j > 0 and matrix[i][j-1] != 1:
                        left_neighbour = (i,j-1)
                        self.data[v].append(left_neighbour)
                    # Right 
                    if j < len(matrix[0])-1 and matrix[i][j+1] != 1:
                        right_neighbour = (i,j+1)
                        self.data[v].append(right_neighbour)
                    # Down
                    if i < len(matrix)-1 and matrix[i+1][j] != 1:
                        down_neighbour = (i+1,j)
                        self.data[v].append(down_neighbour)
                    # Up 
                    if i > 0 and matrix[i-1][j] != 1:
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
def bfs(g,start,dest, filename):

    out_filename = filename + '_mine_bfs_out.txt'
    out_file = open(out_filename,'w')

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

        is_visited[node[0]][node[1]] = 1

        if node == dest:
            break
        
        for neighbour in g.data[node]:
            if is_visited[neighbour[0]][neighbour[1]] == 0:                
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    print_matrix(is_visited, out_file)
    print(len(path), file=out_file)
    print_list(path,out_file)
    
    if g.isMountain:
        path_len = path_length(path,g.matrix)
        print(f'{path_len:.2f}', end="" ,file=out_file)
    else:
        print(f"{(len(path) - 1.0):.2f}", end="" ,file=out_file)

def dfs(g,start,dest, filename):

    out_filename = filename + '_mine_dfs_out.txt'
    out_file = open(out_filename,'w')

    # Track Parents
    parent_map = {}

    # Sort the elements for stack order (descending)
    g.sort_dfs()
    # Initialize the is visited matrix.
    is_visited = [[0 for x in range(g.col)] for x in range(g.row)]
    
    # Push the first element into the stack
    stack = [(start)]
    while stack:
        node = stack.pop()

        # If the node is not visited
        if is_visited[node[0]][node[1]] == 0:
            # Mark as visited
            is_visited[node[0]][node[1]] = 1
        else:
            continue

        if node == dest:
            break
        
        for child in g.data[node]:
            if is_visited[child[0]][child[1]] == 0:
                stack.extend([child])
                if child not in parent_map:
                    parent_map[child] = node

    print_matrix(is_visited,out_file)
    path = dfs_path(parent_map,dest)
    print(len(path),file=out_file)
    print_list(path,out_file)
    
    if g.isMountain:
        path_len = path_length(path,g.matrix)
        print(f'{path_len:.2f}', end="" ,file=out_file)
    else:
        print(f"{(len(path) - 1.0):.2f}", end="" ,file=out_file)

def a_star(g,start,dest, filename):
    
    # Open the files
    out_filename = filename + '_mine_a_star_out.txt'
    out_file = open(out_filename,'w')

    # Positions for checking the neighbours
    positions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    
    # Initialize the is visited matrix.
    is_visited = [[0 for x in range(g.col)] for x in range(g.row)]

    # Create the starting point
    start_node = Vertex(None,start)
    end_node = Vertex(None,dest)

    open_list = []
    closed_list = []
    open_list.append(start_node)

    while open_list:
        open_list = sorted(open_list)

        # Pop the current one from open list.
        current_node = open_list.pop(0)
        closed_list.append(current_node)

        if is_visited[current_node.position[0]][current_node.position[1]] == 1:
            continue

        is_visited[current_node.position[0]][current_node.position[1]] = 1
        
        # Check if it is the solution node
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            
            print_matrix(is_visited,out_file)
            print(len(path),file=out_file)
            print_list(path[::-1],out_file)
            print(f"{current_node.g:.2f}",end="", file=out_file)
            break

        children = []
        for new_pos in positions:
            # Construct the position to check
            pos = (current_node.position[0] + new_pos[0], current_node.position[1] + new_pos[1])
            
            # If the new neighbour is not in the bounds
            if (pos[0] > g.row - 1) or (pos[0] < 0) or (pos[1] > (g.col -1)) or (pos[1] < 0):
                continue

            # Check if its walkable
            if g.isMountain:
                if abs(g.matrix[pos[0]][pos[1]] - g.matrix[current_node.position[0]][current_node.position[1]]) > 1.0:
                    continue
            else:
                if g.matrix[pos[0]][pos[1]] == 1:
                    continue
            
            new_node = Vertex(current_node, pos)
            children.append(new_node)

        for child in children:
            # If the child is in the closed list ignore it
            if child in closed_list:
                continue
            
            # Calculate the g,f,h
            if g.isMountain:
                child.g = current_node.g + math.sqrt(1+((g.matrix[child.position[0]][child.position[1]] - g.matrix[current_node.position[0]][current_node.position[1]]))**2) 
                child.h = math.sqrt((child.position[0] - end_node.position[0])**2  
                        + (child.position[1] - end_node.position[1])**2 
                        + ((g.matrix[child.position[0]][child.position[1]])-(g.matrix[end_node.position[0]][end_node.position[1]]))**2)
            else:
                child.g = current_node.g + 1
                child.h = abs(end_node.position[0]-child.position[0]) + abs(end_node.position[1]-child.position[1])
            child.f = child.g + child.h

            # If the child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)

def path_length(path,matrix):
    path_length = 0
    for i in range(len(path) - 1):
        height_diff = matrix[path[i][0]][path[i][1]] - matrix[path[i+1][0]][path[i+1][1]]
        path_length = path_length + math.sqrt(height_diff**2 + 1)
    return path_length 

# Prints a list of tuple in the asked format
def print_list(l,out_file):
    for el in l:
        print(el[0],el[1],file=out_file)

# Returns the path for the dfs
def dfs_path(parent_map,target):
    path = []
    curr = target
    while (curr != None):
        path.insert(0,curr)
        if curr not in parent_map:
            break    
        curr = parent_map[curr]

    return path

# Prints a given matrix in the asked format
def print_matrix(matrix,out_file):
    for i, row in enumerate(matrix):
        for col in range(len(row)):
            print(matrix[i][col], end=" ",file=out_file)
        print(file=out_file)

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
            matrix.append([float(x) for x in line.split()])

    # Determine and assign graph type 
    problemMountain = False 
    if 'mountain' in filename:
        problemMountain = True
    
    graph = Graph(matrix,problemMountain)
    # Cut the .txt part
    filename = filename[:-4]
    bfs(graph,start,dest,filename)
    dfs(graph,start,dest,filename)
    a_star(graph,start,dest,filename)

# Invoke main.
if __name__ == "__main__":
    main()
