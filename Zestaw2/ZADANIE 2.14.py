file = open("String.txt")
line = file.read().split()

def funA ():
    MaxWyraz = ""
    Dl = 0
    for i in range (len(line)):
        if len(line[i]) >= len(MaxWyraz):
            MaxWyraz = line[i]
            Dl = len(MaxWyraz)
    return MaxWyraz, Dl

print(funA())