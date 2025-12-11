import tkinter as tk
import random


class ProstaGraPKN:
    def __init__(self, root):
        self.root = root
        self.root.title("Papier-Kamień-Nożyce")
        self.root.geometry("400x400")

        # Wyniki
        self.punkty_gracz = 0
        self.punkty_komputer = 0

        # Główne etykiety
        self.label_gracz = tk.Label(root, text="Twój wybór: ", font=("Arial", 12))
        self.label_gracz.pack(pady=10)

        self.label_komputer = tk.Label(root, text="Komputer: ", font=("Arial", 12))
        self.label_komputer.pack(pady=10)

        self.label_wynik = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.label_wynik.pack(pady=20)

        # Ramka z przyciskami
        ramka_przyciskow = tk.Frame(root)
        ramka_przyciskow.pack(pady=20)

        # Przyciski
        tk.Button(ramka_przyciskow, text="✋ Papier", font=("Arial", 12),
                  width=12, command=lambda: self.graj("P")).grid(row=0, column=0, padx=5)

        tk.Button(ramka_przyciskow, text="✊ Kamień", font=("Arial", 12),
                  width=12, command=lambda: self.graj("K")).grid(row=0, column=1, padx=5)

        tk.Button(ramka_przyciskow, text="✌️ Nożyce", font=("Arial", 12),
                  width=12, command=lambda: self.graj("N")).grid(row=0, column=2, padx=5)

        # Wyniki
        self.label_punkty = tk.Label(root,
                                     text="Gracz: 0 | Komputer: 0",
                                     font=("Arial", 12, "bold"))
        self.label_punkty.pack(pady=10)

        # Przycisk resetu
        tk.Button(root, text="Nowa gra", font=("Arial", 10),
                  command=self.resetuj).pack(pady=10)

    def graj(self, wybor_gracza):
        # Komputer losuje
        opcje = ['P', 'K', 'N']
        wybor_komputera = random.choice(opcje)

        # Wyświetl wybory
        self.label_gracz.config(text=f"Twój wybór: {self.nazwa(wybor_gracza)}")
        self.label_komputer.config(text=f"Komputer: {self.nazwa(wybor_komputera)}")

        # Sprawdź wynik
        if wybor_gracza == wybor_komputera:
            wynik = "Remis!"
        elif (wybor_gracza == 'P' and wybor_komputera == 'K') or \
                (wybor_gracza == 'K' and wybor_komputera == 'N') or \
                (wybor_gracza == 'N' and wybor_komputera == 'P'):
            wynik = "Wygrałeś!"
            self.punkty_gracz += 1
        else:
            wynik = "Przegrałeś!"
            self.punkty_komputer += 1

        self.label_wynik.config(text=wynik)
        self.label_punkty.config(text=f"Gracz: {self.punkty_gracz} | Komputer: {self.punkty_komputer}")

    def nazwa(self, wybor):
        if wybor == 'P':
            return "Papier"
        elif wybor == 'K':
            return "Kamień"
        else:
            return "Nożyce"

    def resetuj(self):
        self.punkty_gracz = 0
        self.punkty_komputer = 0
        self.label_gracz.config(text="Twój wybór: ")
        self.label_komputer.config(text="Komputer: ")
        self.label_wynik.config(text="")
        self.label_punkty.config(text="Gracz: 0 | Komputer: 0")


# Uruchomienie
if __name__ == "__main__":
    root = tk.Tk()
    gra = ProstaGraPKN(root)
    root.mainloop()