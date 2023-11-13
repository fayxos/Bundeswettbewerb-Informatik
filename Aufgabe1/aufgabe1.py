from random import randint, shuffle
from enum import Enum
from copy import deepcopy

def find_position(grid, number):
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == number:
                return (c, r)
            
    return None

class Node:
    def __init__(self, x, y, previous_node):
        self.x = x
        self.y = y 
        self.previous_node = previous_node

class Direction(Enum): # x, y, z
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

def find_path(grid, number, x, y, number_count):
    end = find_position(grid, number)

    queue = []
    queue.append(Node(x, y, None))

    discovered = deepcopy(grid)
    discovered[y][x] = number

    while(not(len(queue) == 0)):
        node = queue.pop(0)
        
        for dir in Direction:
            newX = node.x + dir.value[0]
            newY = node.y + dir.value[1]

            if newX == end[0] and newY == end[1]:
                return Node(newX, newY, node)
            
            if newY >= 0 and newY < len(grid) and newX >= 0 and newX < len(grid[newY]) and (grid[newY][newX] == 0 or grid[newY][newX] == number) and (discovered[newY][newX] == 0 or discovered[newY][newX] == number): 
                new_discovered = deepcopy(discovered)
                new_discovered[newY][newX] = -1

                if numbers_have_space(new_discovered, number_count):
                    discovered[newY][newX] = -1
                    queue.append(Node(newX, newY, node))

    return None

def number_has_space(grid, number):
    number_count = 0
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == number:
                number_count += 1

    if number_count == 0 or number_count == 2:
        return True
    elif number_count == 1:
        x, y = find_position(grid, number)
        up = y-1 >= 0 and y-2 >= 0 and grid[y-1][x] == 0 and grid[y-2][x] == 0
        right = x+1 < len(grid[y]) and x+2 < len(grid[y]) and grid[y][x+1] == 0 and grid[y][x+2] == 0
        down = x-1 >= 0 and x-2 >= 0 and grid[y][x-1] == 0 and grid[y][x-2] == 0
        left = y-1 >= 0 and y-2 >= 0 and grid[y-1][x] == 0 and grid[y-2][x] == 0

        if up or right or down or left:
            return True
    
    return False

def numbers_have_space(grid, number_count):
    for i in range(1, number_count+1):
        has_space = number_has_space(grid, i)
        if not(has_space):
            return False

    return True

def generate_arukone(n):
    if n % 2 != 0 or n < 4:
        print("Ungültige Gittergröße. Sie muss gerade und mindestens 4 sein.")
        return
        

    grid = [[0 for _ in range(n)] for _ in range(n)]

    number_count = randint(n // 2, n)

    numbers = []
    for i in range(1, number_count+1):
        numbers.append(i)
        numbers.append(i)

    shuffle(numbers)
    
    while len(numbers) > 0:
        number = numbers.pop(0)

        placed = False

        posible_positions = []

        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                if col == 0:
                    posible_positions.append((c, r))

        while len(posible_positions) > 0:
            x, y = posible_positions.pop(randint(0, len(posible_positions)-1) if len(posible_positions) > 1 else 0)

            number_pos = find_position(grid, number)
            if number_pos == None:
                new_grid = deepcopy(grid)
                new_grid[y][x] = number

                if numbers_have_space(new_grid, number_count):
                    grid[y][x] = number
                    break

                continue
            elif (number_pos[1] == y and abs(number_pos[0]-x) <= 1) or (number_pos[0] == x and abs(number_pos[1]-y) <= 1):
                continue

            end_node = find_path(grid, number, x, y, number_count)        
            if end_node == None:
                continue
            else:
                new_grid = deepcopy(grid)
                new_grid[y][x] = number

                if not(numbers_have_space(new_grid, number_count)):
                    continue

                grid[y][x] = number

                prev_node = end_node.previous_node
                while prev_node.previous_node != None:
                    grid[prev_node.y][prev_node.x] = -1
                    prev_node = prev_node.previous_node

        print_grid(grid)

    # Clear -1s
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == -1:
                grid[r][c] = 0

    print(n)
    print(number_count)
    print_grid(grid)

if __name__ == "__main__":
    n = 10
    generate_arukone(n)