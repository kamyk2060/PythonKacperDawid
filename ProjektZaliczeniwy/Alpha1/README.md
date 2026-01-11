# 🎮 HUGO - Wspinaczka po Linach

Prosta gra platformowa gdzie Hugo wspina się po linach i unika przeszkód!

## 🚀 Jak uruchomić

```bash
# Upewnij się że masz zainstalowany Pygame
pip install pygame

# Uruchom grę
python main.py
```

## 🎮 Sterowanie

| Akcja | Klawisze |
|-------|----------|
| Ruch góra/dół | `↑↓` lub `W/S` |
| Zmiana liny | `←→` lub `A/D` |
| Start gry | `SPACJA` |
| Menu / Wyjście | `ESC` |

## 🎯 Cel gry

- Wspinaj się jak najwyżej
- Zbieraj monety (10 punktów każda)
- Unikaj nietoperzy i pocisków

## ⭐ Powerupy

| Kolor | Efekt |
|-------|-------|
| 🟣 Fioletowy | Nieśmiertelność na 3 sekundy |
| 🟢 Zielony | Podwójne punkty na 5 sekund |

## 📁 Struktura projektu

```
hugo_game/
├── main.py              # Uruchom to żeby zagrać!
├── game/
│   ├── __init__.py
│   ├── config.py        # Wszystkie ustawienia gry
│   ├── game.py          # Główna logika gry
│   ├── player.py        # Klasa gracza
│   ├── rope.py          # Klasa liny
│   ├── obstacles.py     # Nietoperze
│   ├── enemy.py         # Przeciwnicy i pociski
│   ├── collectibles.py  # Monety i powerupy
│   └── sprites.py       # Manager grafik
└── sprites/             # Folder z grafikami (opcjonalne)
```

## 🎨 Grafiki

Gra działa bez grafik - używa prostych kształtów jako fallback.

Jeśli chcesz użyć grafik, dodaj je do folderu `sprites/`:
- `player_climb.png` - animacja wspinaczki (700×128px, 7 klatek)
- `player_jump_left.png` - skok w lewo (400×128px, 4 klatki)
- `player_jump_right.png` - skok w prawo (400×128px, 4 klatki)
- `bat_1.png`, `bat_2.png` - nietoperze (420×140px, 3 klatki)
- `background.png` - tło (1000×1000px)
- `rope.png` - tekstura liny (30×100px)
- `coin.png` - moneta (50×50px)
- `powerup_shield.png`, `powerup_star.png` - powerupy (50×50px)
- `enemy.png` - przeciwnik (256×128px, 2 klatki)

## 📝 Mechaniki

### System przeszkód
Nietoperze pojawiają się według wzorców (patterns). Zawsze jest przynajmniej jedna wolna lina - gra jest zawsze możliwa do przejścia!

### System kolizji
Hitboxy są mniejsze (70%) od sprite'ów - dzięki temu kolizje są bardziej fair.

### Trudność
Gra automatycznie zwiększa prędkość scrollingu z czasem.

---

Projekt edukacyjny 🎓
