import os

def white(left, right): # weißer Baustein
    on = not(left and right) # ¬(right ∧ ¬right)
    return (on, on)

def red(_, right): # roter Baustein mit Lichtsensor oben
    return (not(right), not(right)) # ¬right, ¬right

def red_turned(left, _): # roter Baustein gedreht mit Lichtsensor unten
    return (not(left), not(left)) # ¬left, ¬left

def blue(left, right): # blauer Baustein
    return (left, right) # left, right

def get_output(comb, structure, width, height):
    light = [[False for _ in range(width)] for _ in range(height-1)] # Speichern der Lichter, False = Licht aus

    # Einsetzen der True und False Werte an den Stellen der Lichtquellen
    i = 0
    for n, block in enumerate(structure[0]): 
        if block:
            light[0][n] = comb[i]
            i += 1

    # Durhclaufen des Aufbaus von oben nach unten und links nach rechts
    for i, row in enumerate(structure[1:]):
        for j, block in enumerate(row):

            # Auf diesem und dem nächsten Feld befindet sich ein Baustein
            if block == True: 
                erg = structure[i+1][j+1](light[i][j], light[i][j+1]) # Bestimmen der Ausgabe des Bausteins, Bsp: (true, true) = white(true, false)
                light[i+1][j] = erg[0] # Speichern der Ausgabe in Lichter-Liste
                light[i+1][j+1] = erg[1]

    # Speichern der Ausgaben an den gekennzeichneten Stellen (L1, L2, ...)
    output = []
    for n, block in enumerate(structure[-1]):
        if block:
            output.append(light[-1][n])

    return output

# Erstellen einer Liste mit allen Permutation von True und False, bei n Lichtquellen
def bool_permutations(n, l, i_c):
    if n == 0:
        i_c.append(l)
    else:
        return [bool_permutations(n-1, l+[True], i_c)] + [bool_permutations(n-1, l+[False], i_c)]

def create_output_string(structure, width, height):
    output_string = ""
    inputs = 0
    outputs = []

    # Zählen der Lichtquellen
    for block in structure[0]:
        if block:
            inputs += 1

            # Hinzufügen der Lichtquelle zum Output
            output_string += block + "    "

    for block in structure[-1]:
        if block:
            # Hinzufügen der Ausgaben zum Output
            output_string += block + "    "

    output_string += "\n"

    # Erstellen aller Permutation von True und False, bei Anzahl der Lichtquellen
    input_combinations = []
    bool_permutations(inputs, [], input_combinations)

    # Durchlaufen aller Permutationen
    for comb in reversed(input_combinations):
        for bool in comb:
            # Wert der Lichtquelle (True = An, False = Aus) zur Output hinzufügen
            output_string += "An    " if bool else "Aus   "

        # Ermitteln der Ausgaben der unteren Bausteine
        outputs = get_output(comb, structure, width, height)

        # Hinzufügen der Ergebnisse zum Output
        for bool in outputs:
            output_string += "An    " if bool else "Aus   "

        output_string += "\n"

    return output_string

def read_file(filename):
    dispatcher = {"W": white, "r": red, "R": red_turned, "B": blue}
    with open(os.path.dirname(__file__) + "/" + filename, "r") as f:

        dims = f.readline().split(" ")
        width = int(dims[0].replace("\n", ""))
        height = int(dims[1].replace("\n", ""))

        structure = [[None for _ in range(0, width)] for _ in range(0, height)] # Zweidimensionale Liste für Aufbau der Bausteine, None = kein Baustein

        lines = f.readlines() # Zeilen der Eingabe
        split_lines = [] # Einzelne Zeichen der Eingabe

        # Aufsplitten der Zeilen der Eingabe
        for n, line in enumerate(lines):
            split_lines.append([])
            for char in line.split(" "):
                if char:
                    split_lines[n].append(char)

        skip = [] # Position die überspungen werden sollen

        # Durchlaufen des Aufbaus
        for i in range(0, height):
            for j in range(0, width):

                if (i, j) in skip:
                    continue

                block = split_lines[i][j].strip().replace("\n", "") # Zeichen an der gegebenen Position
                
                # Falls an der Stelle eine Lichtquelle ist
                if "Q" in block:
                    structure[i][j] = block
                # Falls an der Stelle eine Ausgabe ist
                elif "L" in block:
                    structure[i][j] = block
                # Falls die Stelle nicht leer ist
                elif block != "X":
                    structure[i][j] = True # True gibt an das an Position (i, j) und (i, j+1) ein Baustein ist
                    structure[i][j+1] = dispatcher[block] # Speichern der Funktion je nach Baustein
                    skip.append((i, j+1)) # Position (i, j+1) muss nicht nochmal untersucht werden

    return structure, width, height

def save_output(output, filename): 
    with open(os.path.dirname(__file__) + f"/{filename.split('.')[0]}_Loesung.txt", "w") as f:
        f.write(output)

if __name__ == '__main__':
    filename = "nandu5.txt"

    while not(filename in os.listdir(os.path.dirname(__file__))):
        filename = input("Dateiname: ")
        if not(filename in os.listdir(os.path.dirname(__file__))):
            print("Datei wurde nicht gefunden!\n")

    structure, width, height = read_file(filename) # Einlesen der Eingabedatei

    output = create_output_string(structure, width, height) # Erstellen der Ausgabe

    print("Ausgabe: ")
    print(output) 
    save_output(output, filename) # Speichern der Ausgabe in Textdatei