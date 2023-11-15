from random import randint, shuffle
from enum import Enum
from copy import deepcopy
import os

def find_position(grid, number):
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == number:
                return (c, r) # Position der Zahl im Gitter
            
    return None

class Node: # Wegpunkt bei der Suche eines Weges 
    def __init__(self, x, y, previous_node):
        self.x = x 
        self.y = y 
        self.previous_node = previous_node # vorheriger Wegpunkt des Weges

class Direction(Enum): # Alle Richtungen in die man von einem feld aus gehen kann
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

# Lee-Algorithmus
def find_path(grid, number, x, y, number_count): 
    end = find_position(grid, number) # Zu findendes Ende des Weges ist die Position der bereits vorhandenen Zahl im Gitter

    queue = []
    queue.append(Node(x, y, None)) # Startpositions wird zur Queue hinzugefügt, Node speichert Position, sowie vorherige Node des Weges

    discovered = deepcopy(grid) # Kopie des Gitters wird erstellt, discovered beinhaltet, welche Felder beim Suchen des Weges schon besucht wurden
    discovered[y][x] = number # Startposition wird als besucht markiert

    while(not(len(queue) == 0)):
        node = queue.pop(0) # Vorderste Node wird aus Queue entfernt
        
        for dir in Direction: # Jede Richtung (oben, rehcts, unten, links) wird durchlaufen
            newX = node.x + dir.value[0] # neuer y-Wert in jeweilige Richtung
            newY = node.y + dir.value[1] # neuer x-Wert in jeweilige Richtung

            if newX == end[0] and newY == end[1]: # Ende wurde gefunden
                return Node(newX, newY, node) # Letzter Schritt des Weges wird zurückgegeben
            
            # Überprüfung ob neue Position innerhalb des Gitters liegt, an dieser Position noch keine andere Zahl oder Linienzug vorhanden ist und diese Position noch nicht besucht wurde
            if newY >= 0 and newY < len(grid) and newX >= 0 and newX < len(grid[newY]) and (grid[newY][newX] == 0 or grid[newY][newX] == number) and (discovered[newY][newX] == 0 or discovered[newY][newX] == number): 
                new_discovered = deepcopy(discovered)
                new_discovered[newY][newX] = -1

                if numbers_have_space(new_discovered, number_count): # Überprüfung ob nach setzten des Linienzuges noch alle Zahlen Platz haben
                    discovered[newY][newX] = -1 # Position wird als besucht markiert
                    queue.append(Node(newX, newY, node)) # Wegpunkt wird zur Queue hinzugefügt

    return None

def number_has_space(grid, number):
    number_count = 0 # Anzahl, wie oft eine Zahl im Gitter vorkommt
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == number:
                number_count += 1 # Zahl kommt im Gitter vor

    if number_count == 0 or number_count == 2: # Falls die Zahl noch nicht oder schon zwei mal im Gitter vorhanden ist, muss nichts weiter Überprüft werden
        return True
    elif number_count == 1: # Falls Zahl erst einmal im Gitter vorhanden ist, muss sie mindestens zwei leere benachbarte Felder in eine Richtung haben, um Platz für die zweite Zahl zu haben
        x, y = find_position(grid, number) # Position der Zahl im Gitter finden
        up = y-1 >= 0 and y-2 >= 0 and grid[y-1][x] == 0 and grid[y-2][x] == 0 # zwei leere benachbarte Felder nach oben?
        right = x+1 < len(grid[y]) and x+2 < len(grid[y]) and grid[y][x+1] == 0 and grid[y][x+2] == 0 # zwei leere benachbarte Felder nach rechts?
        down = x-1 >= 0 and x-2 >= 0 and grid[y][x-1] == 0 and grid[y][x-2] == 0 # zwei leere benachbarte Felder nach unten?
        left = y-1 >= 0 and y-2 >= 0 and grid[y-1][x] == 0 and grid[y-2][x] == 0 # zwei leere benachbarte Felder nach links?

        if up or right or down or left: # Zahl ht mindestens zwei leere banchbarte Felder in eine Richtung
            return True
    
    return False

def numbers_have_space(grid, number_count):
    for i in range(1, number_count+1): # Durchlaufen aller Zahlen im Gitter
        has_space = number_has_space(grid, i) # Überprüfung ob Zahl mindestens ein leeres benachbartes Feld im Gitter hat
        if not(has_space):
            return False

    return True

def print_grid(grid): # Ausgeben des Gitters in der Konsole
    for row in grid:
        print(" ".join(map(str, row)))

def save_grid(n , number_count, grid): # Speichern der Ausgabe in Textdatei
    arukone_count = 0
    files = os.listdir(os.path.dirname(__file__))
    for file in files:
        if "arukone" in file:
            arukone_count += 1

    with open(os.path.dirname(__file__) + f"/arukone{arukone_count}.txt", "w") as f:
        f.write(f"{n}\n{number_count}\n")
        for row in grid:
            f.write(" ".join(map(str, row)) + "\n")

def generate_arukone(n):
    if n % 2 != 0 or n < 4:
        print("Ungültige Gittergröße. Sie muss gerade und mindestens 4 sein.")
        return

    grid = [[0 for _ in range(n)] for _ in range(n)] # Gitter der Größe n x n

    number_count = randint(n // 2, n) # Anzahl der Zahlen von n/2 bis n

    numbers = [] # Liste mit allen Zahlen
    for i in range(1, number_count+1): # Jede Zahl wird zwei mal hinzugefügt
        numbers.append(i)
        numbers.append(i)

    shuffle(numbers) # Zahlen werden zufällig durchgemischt
    
    while len(numbers) > 0: 
        number = numbers.pop(0) # Jede Zahl wird nacheinander aus der Liste herausgenommen

        posible_positions = []

        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                if col == 0:
                    posible_positions.append((c, r)) # Alle Positionen an denen noch keine Zahl oder Linienzug vorhanden ist werden zu den möglichen Positionen hinzugefügt

        while len(posible_positions) > 0:
            x, y = posible_positions.pop(randint(0, len(posible_positions)-1) if len(posible_positions) > 1 else 0) # Zufällige mögliche Position wird der Liste entnommen

            number_pos = find_position(grid, number) # Position der Zahl, falls diese bereits einmal im Gitter vorhanden ist
            if number_pos == None: # Zahl ist noch nicht im Gitter vorhanden
                new_grid = deepcopy(grid) # Kopie des Gitters
                new_grid[y][x] = number # Hinzufügen der Zahl zur Gitter-Kopie

                if numbers_have_space(new_grid, number_count): # Überprüfung ob jetzt noch alle Zahlen mindestens ein leeres benachbartes Feld haben
                    grid[y][x] = number # Hinzufügen der Zahl zum Gitter
                    break # Weiter mit nächster Zahl

                continue
            elif (number_pos[1] == y and abs(number_pos[0]-x) <= 1) or (number_pos[0] == x and abs(number_pos[1]-y) <= 1): # Überprüfung ob Position direkt neben der bereits vorhandenen Zahl ist
                continue # Wenn nicht, weiter mit nächster möglicher Position

            end_node = find_path(grid, number, x, y, number_count) # Finden des schnellsten Weges von der Zahl zu der bereits vorhandenen gleichen Zahl      
            if end_node == None: # Kein Weg gefunden
                continue # Weiter mit nächster möglicher Position 
            else: # Weg gefunden
                new_grid = deepcopy(grid) # Kopie des Gitters
                new_grid[y][x] = number # Hinzufügen der Zahl zur Gitter-Kopie

                if not(numbers_have_space(new_grid, number_count)): # Überprüfung ob jetzt noch alle Zahlen mindestens ein leeres benachbartes Feld haben
                    continue # Wenn nicht, weiter mit nächster möglicher Position

                grid[y][x] = number # Hinzufügen der Zahl zum Gitter

                prev_node = end_node.previous_node
                while prev_node.previous_node != None: # Durchlaufen des Weges von Zahl zu Zahl
                    grid[prev_node.y][prev_node.x] = -1 # Eintragen der Linienzügen im Gitter
                    prev_node = prev_node.previous_node

        print_grid(grid)

    # Clear -1s
    for r in range(len(grid)): # Entfernen der Linienzüge im Gitter
        for c in range(len(grid[r])):
            if grid[r][c] == -1:
                grid[r][c] = 0

    print(n) # Ausgeben der Größe des Gitters
    print(number_count) # Ausgeben der Anzahl an Zahlen
    print_grid(grid) # Ausgeben des Gitters

    save_grid(n, number_count, grid) # Speichern des Rätsels in Textdatei

if __name__ == "__main__":
    n = 10 # Gittergröße n x n
    generate_arukone(n)