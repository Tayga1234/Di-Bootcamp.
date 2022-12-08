#---------- Exercice 2 : Quel Est Votre Livre Préféré ?-----------#

import random       # cet import me permet d'utiliser la fonction random
def function(number):
    if number in range (1,101):
        nb=random.randint(1, 101)
        print(nb)
        nbr=int(input("Essayez de trouver le nombre: "))
        if nbr==nb:
            print("Reussite!! Vous avez touvé le nombre")
        else:
            print("Echec")
    else:
        print("Ce nombre n'est pas compris entre 1 et 100")
   
function(10)
