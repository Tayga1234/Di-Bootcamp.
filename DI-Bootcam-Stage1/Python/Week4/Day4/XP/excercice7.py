#1.Créez une fonction appelée get_random_temp()
import random

def get_random_temp():
    return random.uniform(-10, 40)

# Test de la fonction
for i in range(10):
    print(get_random_temp())

import random

def get_random_temp():
    return random.randint(-10, 40)


#############################################################
#2.Créez une fonction appelée main()

def main():
    # Obtention d'une température aléatoire
    temp = get_random_temp()

    # Affichage d'un message à l'utilisateur
    print("La température actuelle est de"+temp+ "degrés Celsius.")

# Appel de la fonction main
main()


###############################################################################
import random

def get_random_temp():
    return random.randint(-10, 40)

def main():
    # Obtention d'une température aléatoire
    temp = get_random_temp()

    # Affichage d'un message à l'utilisateur en fonction de la température
    if temp < 0:
        print(f"Brrr, c'est glacial ! Portez des couches supplémentaires aujourd'hui. La température actuelle est de {temp} degrés Celsius.")
    elif temp >= 0 and temp <= 16:
        print(f"Assez froid ! N'oubliez pas votre manteau. La température actuelle est de {temp} degrés Celsius.")
    elif temp > 16 and temp <= 23:
        print(f"Il fait frais. Pensez à mettre un pull. La température actuelle est de {temp} degrés Celsius.")
    elif temp > 23 and temp <= 32:
        print(f"Il fait agréable. N'oubliez pas de prendre une veste si vous sortez. La température actuelle est de {temp} degrés Celsius.")
    elif temp > 32:
        print(f"Il fait chaud ! N'oubliez pas de boire de l'eau et de mettre de la crème solaire. La température actuelle est de {temp} degrés Celsius.")

# Appel de la fonction main
main()



################################################################

import random

def get_random_temp(saison):
  # Définissez les limites de température en fonction de la saison
  if saison == "été":
    lower_bound = 16
    upper_bound = 40
  elif saison == "automne" or saison == "printemps":
    lower_bound = -10
    upper_bound = 16
  elif saison == "hiver":
    lower_bound = -10
    upper_bound = 16
  else:
    # Si la saison n'est pas reconnue, utilisez les limites par défaut
    lower_bound = -10
    upper_bound = 40

  # Générez un nombre aléatoire entre les limites de température
  return random.randint(lower_bound, upper_bound)

def main():
  # Demandez à l'utilisateur de saisir une saison
  saison = input("Saisissez une saison (été, automne, hiver, printemps) : ")

  # Appelez la fonction get_random_temp() avec la saison comme argument
  temp = get_random_temp(saison)
  print("La température est de", temp, "degrés.")

main()



################bonus 1 ##############
def main():
  # Demandez à l'utilisateur de saisir une saison
  saison = input("Saisissez une saison (été, automne, hiver, printemps) : ")

  # Appelez la fonction get_random_temp() avec la saison comme argument
  temp = get_random_temp(saison)
  print("La température est de", temp, "degrés.")

main()
#################################

def main():
  # Demandez le numéro du mois à l'utilisateur
  mois = int(input("Saisissez le numéro du mois (1-12) : "))

  # Déterminez la saison en fonction du mois
  if mois == 12 or mois == 1 or mois == 2:
    saison = "hiver"
  elif mois >= 3 and mois <= 5:
    saison = "printemps"
  elif mois >= 6 and mois <= 8:
    saison = "été"
  elif mois >= 9 and mois <= 11:
    saison = "automne"
  else:
    # Si le mois n'est pas valide, utilisez l'hiver comme saison par défaut
    saison = "hiver"

  # Appelez la fonction get_random_temp() avec la saison comme argument
  temp = get_random_temp(saison)
  print("La température est de", temp, "degrés.")

main()
