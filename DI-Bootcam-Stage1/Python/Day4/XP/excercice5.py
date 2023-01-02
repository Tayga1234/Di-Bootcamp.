def make_shirt(size, text):
  print("The size of the shirt is " + size + " and the text is '" + text + "'.")

# Appel de la fonction make_shirt() avec des paramètres spécifiques
make_shirt("medium", "I love Python")
def make_shirt(size="large", text="J'aime Python"):
  print("The size of the shirt is " + size + " and the text is '" + text + "'.")

# Faire une grande chemise avec le message par défaut
make_shirt()

# Faire une chemise moyenne avec le message par défaut
make_shirt(size="medium")

# Faire une chemise de n'importe quelle taille avec un message différent
make_shirt(size="small", text="I love coding")
