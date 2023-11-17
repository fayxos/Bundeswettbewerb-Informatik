import os
from enum import Enum

def read_file(filename):
    map = [] # Liste zum Speichern des Labyrinths
    discovered = [] # Liste des Labyrinths, die angibt welche Felder schon besucht werden
    char_map = [] # Liste des Labyrinths für Ausgabe
    with open(os.path.dirname(__file__) + "/" + filename, "r") as f:
        dims = f.readline().split(" ")
        height = int(dims[0].replace("\n", "")) # Höhe des Labyrinths
        width = int(dims[1].replace("\n", "")) # Breite des Labyrinths

        input = f.read()
        floors = input.split("\n\n")
        floors = [f for f in floors if f] # Stockwerke des Labyrinths

        map.append([[False for _ in range(width)] for _ in range(height)]) # Ein Stockwerk voller Wände, damit vom obersten Stockwerk nicht noch höher gegangen werden kann
        discovered.append([[True for _ in range(width)] for _ in range(height)])

        # Durchlaufen der beiden Stockwerke
        for f, floor in enumerate(floors):
            map.append([[True for _ in range(width)] for _ in range(height)]) # Stockwerk mit True füllen, True = Freies Feld ohne Wand 
            discovered.append([[False for _ in range(width)] for _ in range(height)]) # Stockwerk mit False füllen, False = Feld wurde noch nicht besucht
            char_map.append([]) # Stockwerk zur Ausgabe-Liste hinzufügen
            rows = floor.split('\n') # Stockwerk in Reihen splitten

            # Durchlaufen der Reihen des Stockwerks
            for r, row in enumerate(rows):
                char_map[f].append([]) # Reihe zur Ausgabe-Liste hinzufügen
                # Durchlaufen der Felder der Reihe
                for c, char in enumerate(row):
                    char_map[f][r].append(char) # Zeiche zur Ausgabe-Liste hinzufügen

                    # Falls auf Feld eine Wand steht
                    if char == '#':
                        map[-1][r][c] = False # Feld als Wand auf Karte markieren

                    # Falls das Feld das Startfeld ist
                    if char == "A":
                        start = (c, r, len(map)-1) # Speichern der Startposition
                    # Falls das Feld das Endfeld ist
                    elif char == "B":
                        end = (c, r, len(map)-1) # Speichern der Endposition

            # Falls oberstes Stockwerk
            if f == 0:
                # Einfügen von zwei leeren Stockwerken zwischen den eigentlichen Stockwerken, für 3 Sekunden Dauer des Stockwerkwechsels
                map.append([[True for _ in range(width)] for _ in range(height)])
                map.append([[True for _ in range(width)] for _ in range(height)])
                discovered.append([[False for _ in range(width)] for _ in range(height)])
                discovered.append([[False for _ in range(width)] for _ in range(height)])

        map.append([[False for _ in range(width)] for _ in range(height)]) # Ein Stockwerk voller Wände, damit vom untersten Stockwerk nicht noch tiefer gegangen werden kann
        discovered.append([[True for _ in range(width)] for _ in range(height)])

    return char_map, map, discovered, start, end

# Wegpunkt bei der Suche eines Weges
class Node:
    def __init__(self, x, y, z, initial_dir, previous_node):
        self.x = x
        self.y = y 
        self.z = z
        self.initial_dir = initial_dir
        self.previous_node = previous_node # Referenze zum vorherigen Wegpunkt

# Alle Richtungen in die von einem zum nächsten Feld gelaufen werden kann
class Direction(Enum): 
    UP = (0, -1, 0, "^")
    RIGHT = (1, 0, 0, ">")
    DOWN = (0, 1, 0, "v")
    LEFT = (-1, 0, 0, "<")
    SWITCH_UP = (0, 0, -1, "!") # Wechseln des Stockwerkes nach oben
    SWITCH_DOWN = (0, 0, 1, "!") # Wechseln des Stockwerkes nach unten

# Lee Algorithmus
def find_fastest_path(map, discovered, start, end): 
    queue = [] # Queue für Wegpunkte, die als nächstes betrachtet werden müssen
    queue.append(Node(start[0], start[1], start[2], None, None)) # Startpunkt des Weges 
    discovered[start[2]][start[1]][start[0]] = True # Feld als besucht markieren

    # Solange die Queue nicht leer ist
    while not(len(queue) == 0): 
        node = queue.pop(0) # Herausnehmen des vordersten Wegpunktes aus der Queue
        
        # Durchlaufen aller Richtungen, in die von einem Wegpunkt gegangen werden kann
        for dir in Direction: 
            # Falls in Zwischenstockwerk, nur Stockwerk kann gewechselt werden
            if node.z != 1 and node.z != 4 and dir != Direction.SWITCH_DOWN and dir != Direction.SWITCH_UP:
                continue

            newX = node.x + dir.value[0] # Berechnen der neuen x-Koordinate nach gehen in diese Richtung
            newY = node.y + dir.value[1] # Berechnen der neuen y-Koordinate nach gehen in diese Richtung
            newZ = node.z + dir.value[2] # Berechnen der neuen z-Koordinate nach gehen in diese Richtung (Stockwerk)

            # Falls die neue Position dem gesuchten Ende entspricht
            if newX == end[0] and newY == end[1] and newZ == end[2]: 
                return Node(newX, newY, newZ, dir, node) # Zurückgeben des letzten Wegpunktes des gefundenen Weges zum Ziel
            
            # Falls an dieser Position im Labyrinth keine Wand steht und das Feld noch nicht besucht wurde
            if map[newZ][newY][newX] == True and not(discovered[newZ][newY][newX]):
                discovered[newZ][newY][newX] = True # Wegpunkt als besucht markieren
                queue.append(Node(newX, newY, newZ, dir, node)) # Wegpunkt zur Queue hinzufügen

    return None # Kein Weg wurde gefunden 

def create_output_map(char_map, path, start):
    previous_field = start
    # Durhclaufen des Weges
    while len(path) > 0:
        step = path.pop() # Herausnehmen des letzten Wegpunktes

        # Nur Bewegungen im oberen und unteren Stockwerk müssen berücksichtigt werden, Zwischenstockwerke nicht
        if step[2] == 1:
            char_map[0][previous_field[1]][previous_field[0]] = step[3].value[3] # Speichern des Richtungszeichen an der jeweiligen Stelle der Karte (oberes Stockwerk)
        elif step[2] == 4:
            char_map[1][previous_field[1]][previous_field[0]] = step[3].value[3] # Speichern des Richtungszeichen an der jeweiligen Stelle der Karte (unteres Stockwerk)

        previous_field = (step[0], step[1], step[2])

    output_string = ""

    # Liste in String umwandeln
    for floor in char_map:
        for row in floor:
            for col in row:
                output_string += col
            output_string += '\n'
        output_string += "\n"

    return output_string # String zurückgeben

def output(char_map, end_node, filename):
    time = 0
    path = []

    new_node = end_node
    # Durchlaufen des Weges von hinten nach vorne (Linked List)
    while(new_node.previous_node != None):
        time += 1 # Bei jedem Schritt 1s zur Zeit addieren

        path.append((new_node.x, new_node.y, new_node.z, new_node.initial_dir)) # Koordinaten und Richtung zum Weg hinzufügen
        new_node = new_node.previous_node # Aktuellen Wegpunkt auf vorherigen wegpunkt setzen

    output_map = create_output_map(char_map, path, start) # Weg in Output-Karte eintragen

    print(f"Zeit: {time} Sekunden\n") # Zeit ausgeben
    print(output_map) # Karte mit Lösung ausgeben

    save_output(output_map, time, filename) # Lösung in Textdatei speichern

def save_output(output_map, time, filename): 
    with open(os.path.dirname(__file__) + f"/{filename.split('.')[0]}_Loesung.txt", "w") as f:
        f.write(f"Zeit: {time} Sekunden\n")
        f.write(output_map)

if __name__ == '__main__':
    filename = ""

    while not(filename in os.listdir(os.path.dirname(__file__))):
        filename = input("Dateiname: ")
        if not(filename in os.listdir(os.path.dirname(__file__))):
            print("Datei wurde nicht gefunden!\n")

    char_map, map, discovered, start, end = read_file(filename) # Einlesen der Eingabedatei

    end_node = find_fastest_path(map, discovered, start, end) # Finden des schnellsten Weges von A nach B, gibt letzten Wegpunkt des Weges zurück

    if end_node == None: # Es wurde kein Weg gefunden
        print("Es wurde kein Weg von A nach B gefunden!")
    else:
        output(char_map, end_node, filename) # Ausgeben der Lösung in der Konsole und Speichern in Textdatei
        

