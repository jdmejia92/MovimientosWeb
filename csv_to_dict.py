nf = input("file: ")

f = open(nf, "r")

headline_line = f.readline()
headline = headline_line.split(',')

line = f.readline()
list_dict = []
while line != "":
    campos = line.split(',')
    d = {}
    for clave, value in zip(headline, campos):
        d[clave] = value
    list_dict.append(d)
    line = f.readline()

print(list_dict)