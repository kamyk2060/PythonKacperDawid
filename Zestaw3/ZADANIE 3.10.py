
# Sposób 1
rzymskie_dict1 = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

# Sposób 2
klucze = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
wartosci = [1, 5, 10, 50, 100, 500, 1000]
rzymskie_dict3 = dict(zip(klucze, wartosci))

# Sposób 3
rzymskie_dict4 = {}
symbole = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
wartosci = [1, 5, 10, 50, 100, 500, 1000]

for i in range(len(symbole)):
    rzymskie_dict4[symbole[i]] = wartosci[i]

# Funkcja liczaca

rzymskie = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

def roman2int(liczba_rzymska):
    liczba_arabska = 0
    poprzednia = 0

    for znak in reversed(liczba_rzymska.upper()):
        aktualna = rzymskie[znak]

        if aktualna < poprzednia:
            liczba_arabska -= aktualna
        else:
            liczba_arabska += aktualna

        poprzednia = aktualna

    return liczba_arabska


print(roman2int("III"))     # 3
print(roman2int("IV"))      # 4
print(roman2int("IX"))      # 9
print(roman2int("XII"))     # 12
print(roman2int("XLV"))     # 45
print(roman2int("XC"))      # 90
print(roman2int("CD"))      # 400
print(roman2int("CM"))      # 900
print(roman2int("MCMXC"))   # 1990
