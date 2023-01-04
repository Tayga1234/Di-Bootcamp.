# Représentation de la grille sous forme de liste de listes
# ' ' représente une case vide, 'O' représente une case occupée par O et 'X' représente une case occupée par X
grid = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

# Liste des joueurs
players = ['O', 'X']

# Indice du joueur courant dans la liste des joueurs
current_player_index = 0

# Fonction pour afficher la grille
def print_grid():
    for row in grid:
        print(' '.join(row))

# Fonction pour vérifier si un joueur a gagné
def check_win(player):
    # Vérifie les lignes
    for row in grid:
        if row == [player, player, player]:
            return True
    # Vérifie les colonnes
    for col in range(3):
        if grid[0][col] == player and grid[1][col] == player and grid[2][col] == player:
            return True
    # Vérifie les diagonales
    if grid[0][0] == player and grid[1][1] == player and grid[2][2] == player:
        return True
    if grid[0][2] == player and grid[1][1] == player and grid[2][0] == player:
        return True
    # Aucun joueur n'a gagné
    return False

# Boucle de jeu
while True:
    # Affiche la grille
    print_grid()
    # Demande à l'utilisateur de saisir une ligne et une colonne
    row = int(input("Saisissez une ligne (0, 1 ou 2) : "))
    col = int(input("Saisissez une colonne (0, 1 ou 2) : "))
    # Vérifie que la case saisie est vide
    if grid[row][col] == ' ':
        # Place le marque du joueur courant dans la case
        grid[row][col] = players[current_player_index]
        # Vérifie si le joueur courant a gagné
        if check_win(players[current_player_index]):
            print("Le joueur " + players[current_player_index] + " a gagné !")
            break
        # Passe au joueur suivant
        current_player_index = (current_player_index + 1) % 2
    else:
        print("Case déjà occupée, veuillez en choisir une autre.")
    # Vérifie si la grille est pleine
    if all(all(cell != ' ' for cell in row) for row in grid):
        print("Match nul !")
        break
