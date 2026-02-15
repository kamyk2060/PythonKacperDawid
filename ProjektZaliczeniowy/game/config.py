"""
HUGO - Konfiguracja gry
=======================
Tutaj są wszystkie ustawienia gry.
"""

# =============================================================================
# OKNO GRY
# =============================================================================
SCREEN_WIDTH = 1000   # Szerokość okna
SCREEN_HEIGHT = 1000  # Wysokość okna
FPS = 60              # Klatki na sekundę (płynność animacji)

# =============================================================================
# KOLORY
# =============================================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
DARK_GRAY = (40, 40, 40)

# =============================================================================
# GRACZ
# =============================================================================
PLAYER_WIDTH = 128    # Szerokość gracza
PLAYER_HEIGHT = 128   # Wysokość gracza
PLAYER_SPEED = 4      # Prędkość ruchu góra/dół

# Gdzie gracz może się poruszać (granice)
PLAYER_START_Y = 400              # Gdzie zaczyna (środek ekranu mniej więcej)
PLAYER_MIN_Y = 50                 # Nie może wyjść powyżej tego
PLAYER_MAX_Y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100  # Nie może wyjść poniżej

# Animacja gracza
PLAYER_CLIMB_FRAMES = 7       # Ile klatek ma animacja wspinaczki
PLAYER_FRAME_WIDTH = 100      # Szerokość jednej klatki w ustawieniu
PLAYER_ANIMATION_SPEED = 8    # Co ile klatek zmienia się obrazek

PLAYER_JUMP_FRAMES = 4        # Ile klatek ma animacja skoku
PLAYER_JUMP_FRAME_WIDTH = 100

# Hitbox - obszar kolizji gracza (mniejszy niż obrazek)
PLAYER_HITBOX_SCALE = 0.7     # 70% rozmiaru obrazka

# =============================================================================
# LINY
# =============================================================================
NUM_ROPES = 3         # Ile lin jest w grze (lewa, środkowa, prawa)
ROPE_WIDTH = 30       # Szerokość liny

# =============================================================================
# SCROLLING (przesuwanie świata)
# =============================================================================
SCROLL_SPEED = 3      # Bazowa prędkość scrollowania

# =============================================================================
# TRUDNOŚĆ
# =============================================================================
# Gra zaczyna przyspieszać dopiero po przebyciu tego dystansu
DIFFICULTY_START_DISTANCE = 3000  # Zaczynamy przyspieszać po ~400 metrach

# Co ile dystansu zwiększamy prędkość
DIFFICULTY_INCREASE_INTERVAL = 3000  # Co ~400 metrów

# O ile zwiększamy prędkość za każdym razem
DIFFICULTY_SPEED_INCREASE = 0.25

# Maksymalna prędkość (żeby nie było za szybko)
MAX_SCROLL_SPEED = 5

# =============================================================================
# PRZESZKODY (NIETOPERZE)
# =============================================================================
OBSTACLE_SIZE = 140           # Rozmiar nietoperza
OBSTACLE_HITBOX_SCALE = 0.7   # Hitbox = 70% obrazka

# Animacja nietoperzy
BAT_ANIMATION_FRAMES = 3      # 3 klatki animacji
BAT_FRAME_SIZE = 140

# Jak często pojawiają się przeszkody
MIN_OBSTACLE_DISTANCE = 400   # Minimalny odstęp między przeszkodami
MAX_OBSTACLE_DISTANCE = 700   # Maksymalny odstęp

# Losowe przesunięcie wysokości nietoperzy w grupie
OBSTACLE_Y_VARIATION = 30

# Wzorce przeszkód - (zajęte_liny, wolne_liny, nazwa)
# ZAWSZE musi być przynajmniej jedna wolna lina!
OBSTACLE_PATTERNS = [
    # Łatwe - jeden nietoperz
    ([0], [1, 2], "lewa"),
    ([1], [0, 2], "srodek"),
    ([2], [0, 1], "prawa"),
    # Trudniejsze - dwa nietoperze
    ([0, 1], [2], "lewe"),
    ([0, 2], [1], "boki"),
    ([1, 2], [0], "prawe"),
]

# =============================================================================
# PRZECIWNICY (strzelający)
# =============================================================================
ENEMY_WIDTH = 128
ENEMY_HEIGHT = 128
ENEMY_SHOOT_COOLDOWN = 90     # Czas między strzałami (w klatkach)
ENEMY_SHOOT_CHANCE = 0.03     # Szansa na strzał co klatkę (3%)
ENEMY_MAX_ON_SCREEN = 2       # Max przeciwników na raz
ENEMY_SPAWN_DISTANCE = 500    # Co ile dystansu może się pojawić
ENEMY_FROM_BOTTOM_CHANCE = 0.3  # 30% szans że pojawi się od dołu

# Animacja
ENEMY_ANIMATION_FRAMES = 2
ENEMY_ANIMATION_SPEED = 30

# =============================================================================
# PRZEDMIOTY DO ZBIERANIA
# =============================================================================
COIN_SIZE = 50        # Rozmiar monety
POWERUP_SIZE = 50     # Rozmiar powerupa

COIN_SPAWN_DISTANCE = 150     # Co ile dystansu pojawia się moneta
MAX_COINS_ON_SCREEN = 5       # Max monet na ekranie

POWERUP_SPAWN_DISTANCE = 600  # Co ile dystansu może pojawić się powerup
POWERUP_SPAWN_CHANCE = 0.4    # 40% szansy na pojawienie się

# =============================================================================
# PUNKTACJA
# =============================================================================
POINTS_PER_COIN = 10         # Punkty za monetę
POINTS_PER_METER = 1          # Punkty za każdy metr dystansu

# Przelicznik dystansu na metry (piksele -> metry)
# 100 pikseli = 1 metr
PIXELS_PER_METER = 100

# =============================================================================
# GRAFIKI
# =============================================================================
SPRITES_DIR = "sprites/"
BACKGROUND_HEIGHT = 1000

SPRITE_FILES = {
    'player_climb': 'player_climb.png',
    'player_jump_left': 'player_jump_left.png',
    'player_jump_right': 'player_jump_right.png',
    'background': 'background.png',
    'rope': 'rope.png',
    'coin': 'coin.png',
    'bat_1': 'bat_1.png',
    'bat_2': 'bat_2.png',
    'powerup_shield': 'powerup_shield.png',
    'powerup_star': 'powerup_star.png',
    'enemy': 'enemy.png',
}
