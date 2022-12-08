my_fav_numbers=set()
my_fav_numbers={1,5,23,30,50}
my_fav_numbers.add(34)
my_fav_numbers.add(70)
my_fav_numbers.remove(70)
friend_fav_numbers={0,3,4,9,25,45,100}
print(my_fav_numbers)
our_fav_numbers=my_fav_numbers.union(friend_fav_numbers)    #concatenation des 2 listes
print(our_fav_numbers)

