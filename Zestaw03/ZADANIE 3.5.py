def RysujMiarke(dlugosc):
    gora = "|"
    dol = "0"

    for i in range(1, dlugosc + 1):
        gora += "....|"
        liczba_spacji = 5 - len(str(i))
        dol += " " * liczba_spacji + str(i)

    print(gora)
    print(dol)


# Test
RysujMiarke(12)
print()
RysujMiarke(25)