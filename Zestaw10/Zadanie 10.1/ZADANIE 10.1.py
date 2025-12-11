import tkinter as tk
import random

okno = tk.Tk()
okno.title("Kostka")
okno.geometry("250x350")

# Znaki kostek Unicode
kostki = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

def rzuc():
    wynik = random.randint(0, 5)
    etykieta.config(text=kostki[wynik])
    liczba.config(text=f"{wynik + 1}")

etykieta = tk.Label(okno, text="⚀", font=("Arial", 100))
etykieta.pack(pady=20)

liczba = tk.Label(okno, text="1", font=("Arial", 20))
liczba.pack()

tk.Button(okno, text="Rzuć", command=rzuc, font=("Arial", 14)).pack(pady=20)

okno.mainloop()