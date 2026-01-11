"""
HUGO - Konfiguracja gry
=======================
Wszystkie stałe i parametry gry w jednym miejscu.
Dzięki temu łatwo zmieniać ustawienia bez szukania po całym kodzie.
"""

# =============================================================================
# OKNO GRY
# =============================================================================
SCREEN_WIDTH = 1000      # Szerokość okna w pikselach
SCREEN_HEIGHT = 1000     # Wysokość okna w pikselach
FPS = 60                 # Klatki na sekundę (płynność gry)

# =============================================================================
# KOLORY (format RGB)
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
DARK_GRAY = (50, 50, 50)

# =============================================================================
# GRACZ
# =============================================================================
PLAYER_WIDTH = 128       # Szerokość sprite'a gracza
PLAYER_HEIGHT = 128      # Wysokość sprite'a gracza
PLAYER_VERTICAL_SPEED = 4    # Prędkość ruchu góra/dół

# Pozycja gracza na ekranie
PLAYER_Y_POSITION = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2  # Środek ekranu
PLAYER_MIN_Y = 50                                # Górna granica
PLAYER_MAX_Y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100   # Dolna granica

# Animacja wspinaczki (7 klatek)
PLAYER_CLIMB_FRAMES = 7
PLAYER_FRAME_WIDTH = 100
PLAYER_ANIMATION_SPEED = 8   # Co ile klatek zmienia się animacja

# Animacja skoku (4 klatki)
PLAYER_JUMP_FRAMES = 4
PLAYER_JUMP_FRAME_WIDTH = 100

# Hitbox gracza - 70% rozmiaru sprite'a (żeby kolizje były fair)
PLAYER_HITBOX_SCALE = 0.7

# =============================================================================
# PRZESZKODY (NIETOPERZE)
# =============================================================================
OBSTACLE_SIZE = 140          # Rozmiar sprite'a nietoperza
OBSTACLE_HITBOX_SCALE = 0.7  # Hitbox 70% rozmiaru

# Animacja nietoperzy (3 klatki machania skrzydłami)
BAT_ANIMATION_FRAMES = 3
BAT_FRAME_SIZE = 140

# Wzorce rozmieszczenia przeszkód
# Format: (zajęte_liny, wolne_liny, nazwa)
# Zawsze musi być przynajmniej jedna wolna lina!
PATTERNS = [
    # Łatwe - jeden nietoperz
    ([0], [1, 2], "pojedyncza_lewa"),
    ([1], [0, 2], "pojedyncza_srodek"),
    ([2], [0, 1], "pojedyncza_prawa"),
    # Trudne - dwa nietoperze
    ([0, 1], [2], "podwojna_lewe"),
    ([0, 2], [1], "podwojna_boki"),
    ([1, 2], [0], "podwojna_prawe"),
]

# Spawning przeszkód
PATTERN_SPAWN_DISTANCE = 220     # Początkowa odległość między patternami
MIN_PATTERN_DISTANCE = 300       # Minimalna odległość
MAX_PATTERN_DISTANCE = 600       # Maksymalna odległość
PATTERN_VERTICAL_VARIATION = 30  # Randomizacja wysokości (±30px)

# =============================================================================
# PRZECIWNICY (ENEMY)
# =============================================================================
ENEMY_WIDTH = 128
ENEMY_HEIGHT = 128
ENEMY_SHOOT_COOLDOWN = 90        # Klatki między strzałami (1.5s przy 60 FPS)
ENEMY_SHOOT_CHANCE = 0.03        # Szansa na strzał co klatkę (3%)
ENEMY_MAX_ON_SCREEN = 2          # Maksymalnie 2 na ekranie
ENEMY_SPAWN_DISTANCE = 350       # Co ile pikseli pojawia się nowy
ENEMY_SPAWN_FROM_BOTTOM_CHANCE = 0.3  # 30% szansy że pojawi się od dołu

# Animacja enemy
ENEMY_ANIMATION_FRAMES = 2
ENEMY_ANIMATION_SPEED = 30

# =============================================================================
# LINY I SCROLLING
# =============================================================================
SCROLL_SPEED = 3         # Bazowa prędkość scrollingu (zwiększa się z czasem)
ROPE_WIDTH = 30          # Szerokość liny
NUM_ROPES = 3            # Liczba lin (lewa, środek, prawa)

# =============================================================================
# PRZEDMIOTY DO ZBIERANIA
# =============================================================================
COIN_SIZE = 50           # Rozmiar monety
POWERUP_SIZE = 50        # Rozmiar powerupa

# =============================================================================
# PUNKTACJA
# =============================================================================
COIN_POINTS = 10                    # Punkty za monetę
DISTANCE_POINTS_MULTIPLIER = 0.005  # Punkty za dystans co klatkę

# =============================================================================
# GRAFIKI
# =============================================================================
SPRITES_DIR = "sprites/"
BACKGROUND_HEIGHT = 1000  # Wysokość tła (do scrollingu)

# Nazwy plików graficznych
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
