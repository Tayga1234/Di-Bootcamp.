######________EXO-1________######

my_fav_numbers=[1,5,23,30,50]
my_fav_numbers.extend([34,70])
my_fav_numbers.remove(70)
friend_fav_numbers=[0,3,4,9,25,45,100]
print(my_fav_numbers)
our_fav_numbers=my_fav_numbers+friend_fav_numbers
print(our_fav_numbers)

######________EXO-2________######

# Reponse: NON, on ne peut pas ajouter des element a un tuple dont la valeur est un entier

######________EXO-3________######

basket = ["Banana", "Apples", "Oranges", "Blueberries"];

basket.pop(0)

print(basket)

basket.append("Kiwi")

basket.insert(0,"Pommes")

print(len(basket))

basket=""

print("le panier contient: ",basket)


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
garniture=[]
S=0
garn="Pizza"
while garn!="quitter":
    garn=(input("Nouvelle garniture: "))
    print("vous avez ajouez "+garn+" dans la liste des garniture")
    garniture.append(garn)
    S=S+2.5
    
print(garniture)
print("le prix total est de: ",10+S)


######________Exercice 9 : Cinémax________######
