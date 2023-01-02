# 1. Création du dictionnaire brand
brand = {
    'name': 'Zara',
    'creation_date': 1975,
    'creator_name': 'Amancio Ortega Gaona',
    'type_of_clothes': ['men', 'women', 'children', 'home'],
    'international_competitors': ['Gap', 'H&M', 'Benetton'],
    'number_stores': 7000,
    'major_color': {
        'France': ['blue'],
        'Spain': ['red'],
        'US': ['pink', 'green']
    }
}

# 2. Modification du nombre de magasins à 2
brand['number_stores'] = 2

# 3. Impression des clients de Zara
print(f"Les clients de Zara sont les hommes, les femmes, les enfants et ceux qui cherchent de l'ameublement pour la maison.")

# 4. Ajout de la clé country_creation
brand['country_creation'] = 'Spain'

# 5. Vérification de la présence de la clé international_competitors et ajout de Desigual
if 'international_competitors' in brand:
    brand['international_competitors'].append('Desigual')

# 6. Suppression des informations sur la date de création
del brand['creation_date']

# 7. Impression du dernier concurrent international
print(f"Le dernier concurrent international de Zara est {brand['international_competitors'][-1]}.")

# 8. Impression des principales couleurs de vêtements aux États-Unis
print(f"Les principales couleurs de vêtements de Zara aux États-Unis sont {', '.join(brand['major_color']['US'])}.")

# 9. Impression du nombre de paires clé-valeur
print(f"Le dictionnaire brand contient {len(brand)} paires clé-valeur.")

# 10. Impression des clés du dictionnaire
print(f"Les clés du dictionnaire brand sont {', '.join(brand.keys())}.")

# 11. Création du dictionnaire more_on_zara
more_on_zara = {
    'creation_date': 1975,
    'number_stores': 10000
}

# 12. Ajout des informations du dictionnaire more_on_zara au dictionnaire brand
brand.update(more_on_zara)

# 13. Impression de la valeur de la clé number_stores
print(f"Le nombre de magasins de Zara est maintenant {brand['number_stores']}.")
