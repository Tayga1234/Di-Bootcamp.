# Demande à l'utilisateur de saisir une séquence de mots séparés par des virgules
words = input("Saisissez une séquence de mots séparés par des virgules : ")

# Sépare la chaîne de mots en une liste de mots
words_list = [word.strip() for word in words.split(',')]

# Trie la liste de mots par ordre alphabétique
words_list.sort()

# Affiche la liste de mots séparés par des virgules
print(', '.join(words_list))
