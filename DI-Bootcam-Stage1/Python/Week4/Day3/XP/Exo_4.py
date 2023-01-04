# Recréation du 1er résultat
users = ["Mickey","Minnie","Donald","Ariel","Pluto"]
disney_users_A = {}

for i, user in enumerate(users):
    disney_users_A[user] = i
print(disney_users_A)

# Recréation du 2ème résultat
disney_users_B = {}

for i, user in enumerate(users):
    disney_users_B[i] = user
print(disney_users_B)

# Recréation du 3ème résultat
disney_users_C = {}

for user in sorted(users):
    disney_users_C[user] = users.index(user)
print(disney_users_C)

# Recréation du 1er résultat avec des caractères dont les noms contiennent la lettre "i"
disney_users_D = {}

for user in users:
    if 'i' in user:
        disney_users_D[user] = users.index(user)
print(disney_users_D)

# Recréation du 1er résultat avec des caractères, dont les noms commencent par la lettre « m » ou « p »
disney_users_E = {}

for user in users:
    if user.startswith(('m', 'p')):
        disney_users_E[user] = users.index(user)
print(disney_users_E)
