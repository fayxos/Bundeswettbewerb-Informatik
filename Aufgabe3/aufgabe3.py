import os
from enum import Enum

def read_file(filename):
    map = []
    char_map = []
    discovered = []
    with open(os.path.dirname(__file__) + "/" + filename, "r") as f:
        dims = f.readline().split(" ")
        height = int(dims[0].replace("\n", ""))
        width = int(dims[1].replace("\n", ""))

        input = f.read()
        floors = input.split("\n\n")

        map.append([[False for _ in range(width)] for _ in range(height)])
        discovered.append([[True for _ in range(width)] for _ in range(height)])

        for f, floor in enumerate(floors):
            map.append([[True for _ in range(width)] for _ in range(height)])
            discovered.append([[False for _ in range(width)] for _ in range(height)])
            char_map.append([])
            rows = floor.split('\n')

            for r, row in enumerate(rows):
                char_map[f].append([])
                for c, char in enumerate(row):
                    char_map[f][r].append(char)

                    if char == '#':
                        map[f+1][r][c] = False

                    if char == "A":
                        start = (c, r, f+1)
                        discovered[f+1][r][c] = True
                    elif char == "B":
                        end = (c, r, f+1)

        map.append([[False for _ in range(width)] for _ in range(height)])
        discovered.append([[True for _ in range(width)] for _ in range(height)])

    print(len(map), len(map[0]), len(map[0][0]))
    print(len(discovered), len(discovered[0]), len(discovered[0][0]))

    return char_map, map, discovered, start, end

class Node:
    def __init__(self, x, y, z, initial_dir, previous_node):
        self.x = x
        self.y = y 
        self.z = z
        self.initial_dir = initial_dir
        self.previous_node = previous_node

class Direction(Enum): # x, y, z
    UP = (0, -1, 0, "^")
    RIGHT = (1, 0, 0, ">")
    DOWN = (0, 1, 0, "v")
    LEFT = (-1, 0, 0, "<")
    SWITCH_UP = (0, 0, -1, "!")
    SWITCH_DOWN = (0, 0, 1, "!")

def find_fastest_path(map, discovered, start, end): # Lee Algorithmus
    queue = []
    queue.append(Node(start[0], start[1], start[2], None, None))

    switch_queue = [None, None, None]

    while(not(len(queue) == 0)):
        node = queue.pop(0)
        
        for dir in Direction:
            newX = node.x + dir.value[0]
            newY = node.y + dir.value[1]
            newZ = node.z + dir.value[2]

            if newX == end[0] and newY == end[1] and newZ == end[2]:
                return Node(newX, newY, newZ, dir, node)
            
            if newZ < len(map) and newZ >= 0 and newY < len(map[newZ]) and newY >= 0 and newX < len(map[newZ][newY]) and newX >= 0 and map[newZ][newY][newX] == True and not(discovered[newZ][newY][newX]) and newZ != 3:
                if dir == Direction.SWITCH_DOWN or dir == Direction.SWITCH_UP:
                    switch_queue.append(Node(newX, newY, newZ, dir, node))
                    continue
                
                discovered[newZ][newY][newX] = True
                queue.append(Node(newX, newY, newZ, dir, node))
                switch_queue.append(None)

        next_switch = switch_queue.pop(0)
        if next_switch != None:
            if next_switch.x == end[0] and next_switch.y == end[1] and next_switch.z == end[2]:
                return next_switch

            if next_switch.z < len(map) and next_switch.z >= 0 and next_switch.y < len(map[next_switch.z]) and next_switch.y >= 0 and next_switch.x < len(map[next_switch.z][next_switch.y]) and next_switch.x >= 0 and map[next_switch.z][next_switch.y][next_switch.x] and not(discovered[next_switch.z][next_switch.y][next_switch.x]):
                discovered[next_switch.z][next_switch.y][next_switch.x] = True
                queue.append(next_switch)

        if len(queue) == 0 and len(switch_queue) > 0:
            next_switch = None
            while next_switch == None and len(switch_queue) > 0:
                next_switch = switch_queue.pop(0)

                if next_switch != None:
                    if next_switch.x == end[0] and next_switch.y == end[1] and next_switch.z == end[2]:
                        return next_switch

                    if next_switch.z < len(map) and next_switch.z >= 0 and next_switch.y < len(map[next_switch.z]) and next_switch.y >= 0 and next_switch.x < len(map[next_switch.z][next_switch.y]) and next_switch.x >= 0 and map[next_switch.z][next_switch.y][next_switch.x] and not(discovered[next_switch.z][next_switch.y][next_switch.x]):
                        discovered[next_switch.z][next_switch.y][next_switch.x] = True
                        queue.append(next_switch)
                    else:
                        next_switch = None

    return None

def create_output_map(char_map, path, start):
    previous_field = start
    while len(path) > 0:
        step = path.pop()
        char_map[previous_field[2]-1][previous_field[1]][previous_field[0]] = step[3].value[3]
        previous_field = (step[0], step[1], step[2])

    output_string = ""

    for floor in char_map:
        for row in floor:
            for col in row:
                output_string += col
            output_string += '\n'
        output_string += "\n"

    return output_string

def output(end_node):
    time = 0
    path = []

    new_node = end_node
    while(new_node.previous_node != None):
        if new_node.initial_dir == Direction.SWITCH_DOWN or new_node.initial_dir == Direction.SWITCH_UP:
            time += 3
        else:
            time += 1 

        path.append((new_node.x, new_node.y, new_node.z, new_node.initial_dir))
        new_node = new_node.previous_node

    output_map = create_output_map(char_map, path, start)

    print(f"Zeit: {time} Sekunden\n")
    print(output_map)


if __name__ == '__main__':
    filename = "zauberschule3.txt"

    while not(filename in os.listdir(os.path.dirname(__file__))):
        filename = input("Dateiname: ")
        if not(filename in os.listdir(os.path.dirname(__file__))):
            print("Datei wurde nicht gefunden!\n")

    char_map, map, discovered, start, end = read_file(filename)

    end_node = find_fastest_path(map, discovered, start, end)

    print(end)

    print(end_node.x, end_node.y, end_node.z)

    if end_node == None:
        print("Es wurde kein Weg von A nach B gefunden!")
    else:
        output(end_node)

