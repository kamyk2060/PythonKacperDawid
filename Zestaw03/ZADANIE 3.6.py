def RysujProstokat(kolumny, wiersze):
    if kolumny == 0 or wiersze == 0:
        return ""

    result = ""

    # Górna krawędź
    result += "+" + "---+" * kolumny + "\n"

    for w in range(wiersze):
        # Wiersz z komórkami
        result += "|" + "   |" * kolumny + "\n"
        # Separator między wierszami
        result += "+" + "---+" * kolumny + "\n"

    return result


# Test
print(RysujProstokat(4, 2))
print(RysujProstokat(3, 3))
print(RysujProstokat(5, 1))