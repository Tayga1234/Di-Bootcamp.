def show_magicians(names):
  for name in names:
    print(name)

magician_names = ['Harry Houdini', 'David Blaine', 'Criss Angel']

# Appel de la fonction show_magicians() avec la liste de noms de magiciens
show_magicians(magician_names)
def make_great(names):
  for i in range(len(names)):
    names[i] = names[i] + " the Great"

# Appel de la fonction make_great() avec la liste de noms de magiciens
make_great(magician_names)
# Appel de la fonction show_magicians() pour afficher la liste modifiée
show_magicians(magician_names)
def make_great(names):
  great_names = [name + " the Great" for name in names]
  return great_names

# Appel de la fonction make_great() pour obtenir une nouvelle liste modifiée
great_magician_names = make_great(magician_names)

# Appel de la fonction show_magicians() pour afficher la nouvelle liste modifiée
show_magicians(great_magician_names)
