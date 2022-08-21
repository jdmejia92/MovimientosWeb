import csv

name_f = input("file: ")

f = open(name_f, 'r')
d_reader = csv.DictReader(f, delimiter=",", quotechar='"')

list_movements = []

for fila in d_reader:
    list_movements.append(fila)

print(list_movements)