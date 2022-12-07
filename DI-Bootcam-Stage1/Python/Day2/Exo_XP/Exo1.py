######________Exercice 1 : Set________######

my_fav_numbers=[1,5,23,30,50]
my_fav_numbers.extend([34,70])
my_fav_numbers.remove(70)
friend_fav_numbers=[0,3,4,9,25,45,100]
print(my_fav_numbers)
our_fav_numbers=my_fav_numbers+friend_fav_numbers
print(our_fav_numbers)



######________Exercice 2 : Tuple________######

# Reponse: NON, on ne peut pas ajouter des element a un tuple dont la valeur est un entier



######________Exercice 3 : Liste________######

basket = ["Banana", "Apples", "Oranges", "Blueberries"];

basket.pop(0)

print(basket)

basket.append("Kiwi")

basket.insert(0,"Pommes")

print(len(basket))

basket=""

print("le panier contient: ",basket)


######________Exercice 4 : Flotteurs________######

# Un foat un un type de nombre. La différence c'est qu'il est plus qualifié comme un réel alors que le integer est un entier positif ou négatif
#Float peut comporter une virgule une puisance...

# Oui nous pouvons générer des float en utilisant des operateurs sur les entiers

L=[]
I=1
for i in range (1,8):
    L.append(I+0.5)
    I=I+0.5
print(L)



######________Exercice 5 : Boucle For________######

for i in range (1,21):
    print(i)
k=-1

for i in range (1,21):
    k=k+1
    if i%2==0:
        print(i,"idex",k)
        
######________Exercice 6 : Boucle While________######
name=""
while name!="Gaetan":
    name=input("Entrer votre nom: ")
    

######________ Exercice 7 : Fruits Préférés________######

f_pref=(input("Entrer votre ou vos fruits préférés: ")) # Demander à l'utilisateur de saisir son/ses fruit(s) préféré(s) (un ou plusieurs fruits).
L=[]
L=f_pref.split()

n_fruit=input("entrer le nom d'un fruit: ")
bool=False
for i in L:
    if n_fruit == i:
        
        bool=True
if bool==True:
    print("Vous avez choisi l'un de vos fruits préférés ! Prendre plaisir!")
else:
    print("Vous avez choisi un nouveau fruit. J'espère que tu apprécies")
    

######________ Exercice 8 : Qui A Commandé Une Pizza________######
garniture=[]        #liste des garnitures
S=0         # Somme total de la Pizza
garn="Pizza"        #garniture

while garn!="quitter":
    garn=(input("Nouvelle garniture: "))
    print("vous avez ajouez "+garn+" dans la liste des garniture")
    garniture.append(garn)
    S=S+2.5
    
print(garniture)
print("le prix total est de: ",10+S)


######________Exercice 9 : Cinémax________######

#************* 1_2_3 ****************#
P=0      #initialisation du prix
nb=int(input("Bonjour! Vous etes au nombre de: "))  #initialisation du nombre de la famille

#Cout a payer en fonction de l'age des membres de la famille
for i in range(0,nb):

    age=int(input("Entrer votre l'age de la personne: "))
    print("Personne suivante!")
    if age<3:
        #Billet gratuit
        P=P+0
        
    elif 3<age<=12:
        #Billet coute 10 dollars
        P=P+10
        
    elif age>12:
        #Billet coute 15 dollars
        P=P+15    
 
    
print("Pour tout les (",nb,") membre(s), le montant s'eleve à ",P)


#************* 4 **************#
P=0      #initialisation du prix
nb=int(input("Bonjour! Vous etes au nombre de: "))  #initialisation du nombre de la famille
Name=[]     #liste des noms enregistrés
k=nb
#Cout a payer en fonction de l'age des membres de la famille
for i in range(0,nb):
    name=input("Entrer votre nom: ")
    age=int(input("Entrer votre age: "))
    Name.append(name)
    print("Enregistré! Passer a la personne suivante...")
    
    
    # verification de l'age

    if 16<=age<=21:
        #Billet coute 10 dollars
        P=P+10
    else:
        #Billet gratuit
        print("Vous n'etes pas autorisé a regarder ce film")
        k=k-1
        
        Name.remove(name) #suppression du nom
           
print(Name)    
print("Pour tout les (",k,") membre(s), le montant s'eleve à ",P)



######________Exercice 10 : Commandes Sandwich________######

sandwich_orders = ["Tuna sandwich", "Avocado sandwich", "Egg sandwich", "Sabih sandwich", "Pastrami sandwich"]
finished_sandwiches=[]  # ma liste vide de sandwiches finis
k=0     # k nous permettra de determiner le nombre exact de sandwiches préparés

# processus pour montrer les supprimer les sandwiches deja faits
while sandwich_orders !=[]:
    sw=input("Quel sandwiche avez vous fini de preparer? ")
    if sw in sandwich_orders:
        sandwich_orders.remove(sw)
        finished_sandwiches.append(sw)
        k=k+1
        
# afficher les chandwiches faits
for i in range(0, k):
    print("I made your",finished_sandwiches[i])
    


######________Exercice 11 : Sandwich Orders#2________######

sandwich_orders = ["Pastrami sandwich", "Tuna sandwich", "Avocado sandwich", "Pastrami sandwich", "Egg sandwich", "Sabih sandwich", "Pastrami sandwich"]
finished_sandwiches=[]  # ma liste vide de sandwiches finis
k=0     # k nous permettra de determiner le nombre exact de sandwiches préparés
print("INFO!!! la charcuterie n'a plus de pastrami")

# processus pour montrer les supprimer les sandwiches deja faits

    #suppression des pastramis
while "Pastrami sandwich" in sandwich_orders:
    sandwich_orders.remove("Pastrami sandwich")
    
while sandwich_orders !=[]:
    sw=input("Quel sandwiche avez vous fini de preparer? ")
    if sw in sandwich_orders:
        sandwich_orders.remove(sw)
        finished_sandwiches.append(sw)
        k=k+1
        
# afficher les chandwiches faits sans les Pastamis
for i in range(0, k):
    print("I made your",finished_sandwiches[i])
    