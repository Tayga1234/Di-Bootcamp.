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


