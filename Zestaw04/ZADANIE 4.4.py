def fibonacci(n):
    if n < 0:
        raise ValueError("Numer wyrazu ciągu musi być nieujemny")

    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Dla n >= 2
    dwa_wstecz = 0  # F(n-2)
    jeden_wstecz = 1  # F(n-1)

    for i in range(2, n + 1):
        biezacy = dwa_wstecz + jeden_wstecz
        dwa_wstecz = jeden_wstecz
        jeden_wstecz = biezacy

    return jeden_wstecz


# Przykłady użycia
print(fibonacci(0))  # 0
print(fibonacci(1))  # 1
print(fibonacci(5))  # 5
print(fibonacci(10))  # 55