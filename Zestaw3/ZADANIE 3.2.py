# 1. BŁĄD: L.sort() sortuje listę w miejscu i zwraca None
L = [3, 5, 4]; L = L.sort()  # ŹLE - L stanie się None
L = [3, 5, 4]; L.sort()      # DOBRZE - L zostanie posortowana

# 2. BŁĄD: za mało zmiennych do rozpakowania
x, y = 1, 2, 3               # ŹLE - 3 wartości, 2 zmienne
x, y, z = 1, 2, 3            # DOBRZE - 3 wartości, 3 zmienne

# 3. BŁĄD: krotki są niemutowalne
X = 1, 2, 3; X[1] = 4        # ŹLE - nie można zmieniać elementów krotki
X = [1, 2, 3]; X[1] = 4      # DOBRZE - listy są mutowalne

# 4. BŁĄD: indeks poza zakresem listy
X = [1, 2, 3]; X[3] = 4      # ŹLE - indeksy: 0,1,2 (3 jest poza zakresem)
X = [1, 2, 3]; X[2] = 4      # DOBRZE - zmiana ostatniego elementu

# 5. BŁĄD: stringi są niemutowalne i nie mają append()
X = "abc"; X.append("d")     # ŹLE - stringi nie mają metody append()
X = "abc"; X = X + "d"       # DOBRZE - konkatenacja stringów

# 6. BŁĄD: funkcja pow() wymaga dwóch argumentów
L = list(map(pow, range(8))) # ŹLE - pow() potrzebuje base i exponent
L = list(map(lambda x: pow(x, 2), range(8))) # DOBRZE - podanie wykładnika
