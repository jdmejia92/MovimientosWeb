import csv

name_f = input("file: ")

f = open(name_f, 'r')

f_reader = csv.reader(f, delimiter=",", quotechar='"')

list_movements = []

for fila in f_reader:
    list_movements.append(fila)

print(list_movements)