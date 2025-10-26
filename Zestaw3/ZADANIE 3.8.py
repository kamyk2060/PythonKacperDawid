def operacje_na_sekwencjach(seq1, seq2):

    # (a)
    czesc_wspolna = list(set(seq1) & set(seq2))

    # (b)
    suma_elementow = list(set(seq1) | set(seq2))

    return czesc_wspolna, suma_elementow


# Dla liczb
print("liczby")
sekwencja1 = [1, 2, 3, 4, 5, 2, 3]
sekwencja2 = [4, 5, 6, 7, 8, 4]
czesc_wspolna, suma = operacje_na_sekwencjach(sekwencja1, sekwencja2)
print(f"Sekwencja 1: {sekwencja1}")
print(f"Sekwencja 2: {sekwencja2}")
print(f"(a) Część wspólna: {czesc_wspolna}")
print(f"(b) Suma wszystkich elementów: {suma}")

print("\nstring")
# Dla znaków
sekwencja1 = "abracadabra"
sekwencja2 = "alibaba"
czesc_wspolna, suma = operacje_na_sekwencjach(sekwencja1, sekwencja2)
print(f"Sekwencja 1: '{sekwencja1}'")
print(f"Sekwencja 2: '{sekwencja2}'")
print(f"(a) Część wspólna: {czesc_wspolna}")
print(f"(b) Suma wszystkich elementów: {suma}")
