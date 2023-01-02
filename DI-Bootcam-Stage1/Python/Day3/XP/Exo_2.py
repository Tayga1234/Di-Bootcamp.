family = {}

while True:
    name = input("Entrez le nom d'un membre de la famille (ou tapez 'done' pour terminer) : ")
    if name == 'done':
        break
    age = int(input("Entrez l'âge de ce membre de la famille : "))
    family[name] = age

total_cost = 0

for name, age in family.items():
    if age < 3:
        cost = 0
    elif age >= 3 and age <= 12:
        cost = 10
    else:
        cost = 15
    print(f"{name} doit payer {cost}$ pour le billet.")
    total_cost += cost

print(f"Le coût total de la famille pour les films est de {total_cost}$.")
