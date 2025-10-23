while True:
    user_input = input("Podaj liczbę: ")

    if user_input.lower() == 'stop':
        print("Program zakończony.")
        break

    try:
        x = float(user_input)

        trzecia_potega = x ** 3

        print(f"x = {x}, x^3 = {trzecia_potega}")

    except ValueError:
        print("Błąd: To nie jest poprawna liczba!.")