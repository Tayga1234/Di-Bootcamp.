# Créez une liste des articles disponibles dans le magasin et leur prix
articles = {
    "Jus de pomme": 2.50,
    "Pomme": 0.50,
    "Bouteille d'eau": 1.50,
    "Barres de céréales": 3.00,
    "Soda": 2.00,
    "Lait": 1.50,
    "Yogourt": 0.75,
    "Banane": 0.25,
    "Poire": 0.50,
    "Orange": 0.75
}

# Demandez le montant d'argent que vous avez dans votre portefeuille
argent = float(input("Saisissez le somme d'argent que vous avez dans votre portefeuille : "))

# Créez une liste vide pour stocker les articles que vous pouvez acheter
achats = []

# Parcourez les articles et ajoutez ceux que vous pouvez acheter à la liste achats
for article, prix in articles.items():
  if argent >= prix:
    achats.append(article)
    argent -= prix

# Triez la liste achats par ordre alphabétique
achats.sort()

# Imprimez la liste achats
if achats:
  print("Voici les articles que vous pouvez acheter :")
  for article in achats:
    print(article)
else:
  print("Vous ne pouvez rien achéter")