matrix = [
    "7i3",
    "Tsi",
    "h%x",
    "i #",
    "sM ",
    "$a ",
    "#t%",
    "^r!"
]

# Initialise la chaîne de sortie
output = ""

# Pour chaque colonne de la matrice
for col in range(len(matrix[0])):
    # Pour chaque ligne de la matrice
    for row in range(len(matrix)):
        # Récupère le caractère de la colonne et de la ligne courantes
        char = matrix[row][col]
        # Si le caractère est alpha, ajoute-le à la chaîne de sortie
        if char.isalpha():
            output += char
        # Si le caractère n'est pas alpha et que la chaîne de sortie n'est pas vide, ajoute un espace à la chaîne de sortie
        elif output:
            output += " "

# Affiche la chaîne de sortie
print(output)
