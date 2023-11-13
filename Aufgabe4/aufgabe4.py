import os

def white(left, right): # weißer Baustein
    on = not(left and right) 
    return (on, on)

def red(_, right): # roter Baustein mit Lichtsensor oben
    return (not(right), not(right)) # ¬right, ¬right

def red_turned(left, _): # roter Baustein gedreht mit Lichtsensor unten
    return (not(left), not(left)) # ¬left, ¬left

def blue(left, right): # blauer Baustein
    return (left, right) # left, right

def get_output(comb, structure, width, height):
    light = [[False for _ in range(width)] for _ in range(height-1)]

    i = 0
    for n, block in enumerate(structure[0]): 
        if block:
            light[0][n] = comb[i]
            i += 1

    for i, row in enumerate(structure[1:]):
        for j, block in enumerate(row):

            if block == True: # Auf diesem und dem nächsten Feld befindet sich ein Baustein
                erg = structure[i+1][j+1](light[i][j], light[i][j+1]) # Bsp: (true, true) = white(true, false)
                light[i+1][j] = erg[0]
                light[i+1][j+1] = erg[1]

    output = []
    for n, block in enumerate(structure[-1]):
        if block:
            output.append(light[-1][n])

    return output

def bool_permutations(n, l, i_c):
    if n == 0:
        i_c.append(l)
    else:
        return [bool_permutations(n-1, l+[True], i_c)] + [bool_permutations(n-1, l+[False], i_c)]

def create_output_string(structure, width, height):
    output_string = ""
    inputs = 0
    outputs = []
    for block in structure[0]:
        if block:
            inputs += 1
            output_string += block + "    "

    for n, block in enumerate(structure[-1]):
        if block:
            output_string += block + "    "

    output_string += "\n"

    input_combinations = []
    bool_permutations(inputs, [], input_combinations)   

    for comb in reversed(input_combinations):
        for bool in comb:
            output_string += "An    " if bool else "Aus   "

        outputs = get_output(comb, structure, width, height)

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

        structure = [[None for _ in range(0, width)] for _ in range(0, height)]

        lines = f.readlines()
        split_lines = []
        for n, line in enumerate(lines):
            split_lines.append([])
            for char in line.split(" "):
                if char:
                    split_lines[n].append(char)

        skip = []
        for i in range(0, height):
            for j in range(0, width):

                if (i, j) in skip:
                    continue

                block = split_lines[i][j].strip().replace("\n", "")
                
                if "Q" in block:
                    structure[i][j] = block
                elif "L" in block:
                    structure[i][j] = block
                elif block != "X":
                    structure[i][j] = True
                    structure[i][j+1] = dispatcher[block]
                    skip.append((i, j+1))

    return structure, width, height


if __name__ == '__main__':
    filename = "nandu2.txt"

    while not(filename in os.listdir(os.path.dirname(__file__))):
        filename = input("Dateiname: ")
        if not(filename in os.listdir(os.path.dirname(__file__))):
            print("Datei wurde nicht gefunden!\n")

    structure, width, height = read_file(filename)

    output = create_output_string(structure, width, height) 

    print("Ausgabe: ")
    print(output)
    print()