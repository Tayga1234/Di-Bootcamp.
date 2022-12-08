##----------Exercice 1 : Qu'apprenez-Vous ?-----------#

def display_message():      #Declaration de fnct
    print("Nous apprenons le langage Phyton dans ce cour!")
    
display_message()       #Appel de la fnct


#---------- Exercice 2 : Quel Est Votre Livre Préféré ?-----------#

def favorite_book(title):
    print("One of my favorite books is",title)
    

favorite_book("Les frassques d'Ebinto")



#----------Exercice 3 : Un Peu De Géographie-----------#

def describe_city(ville, pays):     # fonction
    print(ville,"est une ville de",pays)
    
describe_city("Ouagadougou", "Burkina faso")        #appel de la fonction

#fixation par defaut du pays
def describe_city(ville, pays="France"):
    print(ville,"est une ville de",pays)
    
describe_city("Bordeaux")



#----------Exercice 4 : Aléatoire-----------#

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
    
    nbr=int(input("Essayez de trouver le nombre: "))
    if nbr==nb:
        print("Reussite!! Vous avez touvé le nombre")
    else:
        print("Echec")
        
function(10)


#----------Exercice 4 : Aléatoire-----------#

