def factorial(n):
    if n < 0:
        raise ValueError("Silnia jest zdefiniowana tylko dla liczb nieujemnych")
    result = 1
    for i in range(1, n + 1):
        result *= i

    return result


# Przykłady użycia
print(factorial(1))  # 1
print(factorial(5))  # 120
print(factorial(10))  # 3628800