# Demandez le mot à l'utilisateur
mot = input("Saisissez un mot : ")

# Créez un dictionnaire vide
lettres = {}

# Parcourez le mot et stockez les index de chaque lettre dans un dictionnaire
for i, lettre in enumerate(mot):
  if lettre not in lettres:
    lettres[lettre] = []
  lettres[lettre].append(i)

print(lettres)