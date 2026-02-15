# 🎮 HUGO - Wspinaczka po Linach

Prosta gra platformowa w Pygame gdzie wspinasz się po linach i zbierasz monety!

## 🚀 Jak uruchomić

```bash
# Zainstaluj Pygame
pip install pygame

# Uruchom grę
python main.py
```

## 🎮 Sterowanie

| Klawisz | Akcja |
|---------|-------|
| ↑ / W | Ruch w górę |
| ↓ / S | Ruch w dół |
| ← / A | Skok na lewą linę |
| → / D | Skok na prawą linę |
| SPACJA | Start / Restart |
| ESC | Menu / Wyjście |

## 🎯 Cel gry

- Wspinaj się jak najwyżej
- Zbieraj monety (+10 punktów)
- Unikaj nietoperzy i pocisków
- Im dalej zajdziesz, tym więcej punktów!

## ⭐ Powerupy

| Kolor | Efekt | Czas |
|-------|-------|------|
| 🟣 Fioletowy | Nieśmiertelność | 3 sek |
| 🟢 Zielony | Podwójne punkty | 5 sek |

## 📊 Punktacja

- **Moneta** = 10 punktów (20 z powerupem)
- **Dystans** = 1 punkt za każdy metr

## 📁 Struktura projektu

```
hugo_game/
├── main.py              # Uruchom to!
├── README.md            # Ten plik
├── game/
│   ├── __init__.py
│   ├── config.py        # Ustawienia gry
│   ├── game.py          # Główna logika
│   ├── menu.py          # Menu gry
│   ├── player.py        # Klasa gracza
│   ├── rope.py          # Klasy lin
│   ├── obstacles.py     # Nietoperze
│   ├── enemy.py         # Przeciwnicy
│   ├── collectibles.py  # Monety i powerupy
│   └── sprites.py       # Ładowanie grafik
└── sprites/             # Folder z grafikami
```

## 🎮 Mechaniki

### Trudność
Gra zaczyna się łatwo i stopniowo przyspiesza:
- Przez pierwsze ~400 metrów - normalna prędkość
- Potem co ~400 metrów - lekkie przyspieszenie
- Maksymalna prędkość jest ograniczona

### Przeszkody
Nietoperze pojawiają się według wzorców - **zawsze jest przynajmniej jedna wolna lina** do ucieczki!

### Kolizje
Hitboxy (obszary kolizji) są mniejsze niż obrazki - dzięki temu gra jest sprawiedliwa i możesz "otrzeć się" o przeszkodę.

---

