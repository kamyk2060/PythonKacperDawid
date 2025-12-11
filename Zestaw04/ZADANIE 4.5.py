
def odwracanie_iter(L, left, right):
    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1

def odwracanie_rek(L, left, right):
    if left < right:
        L[left], L[right] = L[right], L[left]
        odwracanie_rek(L, left + 1, right - 1)


# Testowanie funkcji
L1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print("Przed:", L1)
odwracanie_iter(L1, 0, 9)
print("Po odwróceniu iteracyjnym):", L1)

L2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print("\nPrzed:", L2)
odwracanie_rek(L2, 2, 6)
print("Po odwróceniu rekurencyjnym:", L2)
