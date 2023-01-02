import random

def compare_numbers(num):
  random_num = random.randint(1, 100)
  if num == random_num:
    print("Réussite ! Les deux nombres sont égaux : " + str(num) + ".")
  else:
    print("Échec. Les deux nombres sont différents : " + str(num) + " et " + str(random_num) + ".")
compare_numbers(50)