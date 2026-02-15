"""
HUGO - Manager Sprite'ów (grafik)
=================================
Ta klasa ładuje wszystkie obrazki z folderu sprites/
i udostępnia je innym częściom gry.
"""
import pygame
import os
from .config import *


class SpriteManager:
    """
    Zarządza wszystkimi grafikami w grze.
    
    Jak działa:
    1. Przy tworzeniu ładuje wszystkie obrazki z dysku
    2. Dzieli duże obrazki (sprite sheets) na mniejsze klatki
    3. Inne klasy pobierają grafiki przez metody get_*()
    """

    def __init__(self):
        # Słownik przechowujący wszystkie grafiki
        # Klucz = nazwa, Wartość = obrazek lub lista obrazków
        self.sprites = {}
        
        # Załaduj wszystkie grafiki
        self._load_all_sprites()

    def _load_all_sprites(self):
        """Ładuje wszystkie grafiki z folderu sprites/"""
        
        # Prosta funkcja pomocnicza do ładowania pliku
        def load_image(filename):
            path = os.path.join(SPRITES_DIR, filename)
            image = pygame.image.load(path)
            return image.convert_alpha()  # convert_alpha() przyspiesza rysowanie

        # -------------------------------------------
        # GRACZ - animacja wspinaczki (7 klatek)
        # -------------------------------------------
        # Obrazek player_climb.png zawiera 7 klatek obok siebie
        # Musimy go pociąć na pojedyncze klatki
        climb_sheet = load_image(SPRITE_FILES['player_climb'])
        
        self.sprites['player_climb'] = []
        for i in range(PLAYER_CLIMB_FRAMES):
            # Wycinamy prostokąt: (x, y, szerokość, wysokość)
            x = i * PLAYER_FRAME_WIDTH
            frame = climb_sheet.subsurface((x, 0, PLAYER_FRAME_WIDTH, PLAYER_HEIGHT))
            self.sprites['player_climb'].append(frame)

        # -------------------------------------------
        # GRACZ - animacja skoku w lewo (4 klatki)
        # -------------------------------------------
        jump_left_sheet = load_image(SPRITE_FILES['player_jump_left'])
        
        self.sprites['player_jump_left'] = []
        for i in range(PLAYER_JUMP_FRAMES):
            x = i * PLAYER_JUMP_FRAME_WIDTH
            frame = jump_left_sheet.subsurface((x, 0, PLAYER_JUMP_FRAME_WIDTH, PLAYER_HEIGHT))
            self.sprites['player_jump_left'].append(frame)

        # -------------------------------------------
        # GRACZ - animacja skoku w prawo (4 klatki)
        # -------------------------------------------
        jump_right_sheet = load_image(SPRITE_FILES['player_jump_right'])
        
        self.sprites['player_jump_right'] = []
        for i in range(PLAYER_JUMP_FRAMES):
            x = i * PLAYER_JUMP_FRAME_WIDTH
            frame = jump_right_sheet.subsurface((x, 0, PLAYER_JUMP_FRAME_WIDTH, PLAYER_HEIGHT))
            self.sprites['player_jump_right'].append(frame)

        # -------------------------------------------
        # TŁO I LINY - pojedyncze obrazki
        # -------------------------------------------
        self.sprites['background'] = load_image(SPRITE_FILES['background'])
        self.sprites['rope'] = load_image(SPRITE_FILES['rope'])

        # -------------------------------------------
        # MONETA - pojedynczy obrazek
        # -------------------------------------------
        self.sprites['coin'] = load_image(SPRITE_FILES['coin'])

        # -------------------------------------------
        # NIETOPERZE - animacja 3 klatek (każdy typ)
        # -------------------------------------------
        # Nietoperz typu 1 (czerwony)
        bat1_sheet = load_image(SPRITE_FILES['bat_1'])
        self.sprites['bat_1'] = []
        for i in range(BAT_ANIMATION_FRAMES):
            x = i * BAT_FRAME_SIZE
            frame = bat1_sheet.subsurface((x, 0, BAT_FRAME_SIZE, BAT_FRAME_SIZE))
            self.sprites['bat_1'].append(frame)

        # Nietoperz typu 2 (fioletowy)
        bat2_sheet = load_image(SPRITE_FILES['bat_2'])
        self.sprites['bat_2'] = []
        for i in range(BAT_ANIMATION_FRAMES):
            x = i * BAT_FRAME_SIZE
            frame = bat2_sheet.subsurface((x, 0, BAT_FRAME_SIZE, BAT_FRAME_SIZE))
            self.sprites['bat_2'].append(frame)

        # -------------------------------------------
        # POWERUPY - pojedyncze obrazki
        # -------------------------------------------
        self.sprites['powerup_shield'] = load_image(SPRITE_FILES['powerup_shield'])
        self.sprites['powerup_star'] = load_image(SPRITE_FILES['powerup_star'])

        # -------------------------------------------
        # PRZECIWNIK (ENEMY) - 2 klatki + odbicie lustrzane
        # -------------------------------------------
        enemy_sheet = load_image(SPRITE_FILES['enemy'])
        
        # Wersja patrząca w lewo (oryginał)
        self.sprites['enemy_left'] = []
        for i in range(ENEMY_ANIMATION_FRAMES):
            x = i * ENEMY_WIDTH
            frame = enemy_sheet.subsurface((x, 0, ENEMY_WIDTH, ENEMY_HEIGHT))
            self.sprites['enemy_left'].append(frame)
        
        # Wersja patrząca w prawo (odbicie lustrzane)
        self.sprites['enemy_right'] = []
        for frame in self.sprites['enemy_left']:
            # flip(obrazek, odbij_poziomo, odbij_pionowo)
            flipped = pygame.transform.flip(frame, True, False)
            self.sprites['enemy_right'].append(flipped)

        print("[SPRITES] Wszystkie grafiki załadowane!")

    # =========================================================================
    # METODY DO POBIERANIA GRAFIK
    # =========================================================================

    def get_player_frame(self, animation_counter, is_jumping, jump_direction, jump_progress):
        """
        Zwraca odpowiednią klatkę animacji gracza.
        
        Parametry:
            animation_counter - licznik do animacji (rośnie co klatkę)
            is_jumping - czy gracz skacze między linami
            jump_direction - 'left' lub 'right'
            jump_progress - jak daleko jest w skoku (0-20)
        """
        # Jeśli gracz skacze - użyj animacji skoku
        if is_jumping and jump_direction:
            # Oblicz która klatka skoku (0, 1, 2 lub 3)
            frame_number = int((jump_progress / 20.0) * PLAYER_JUMP_FRAMES)
            frame_number = min(frame_number, PLAYER_JUMP_FRAMES - 1)  # Nie przekrocz maksimum
            
            if jump_direction == 'left':
                return self.sprites['player_jump_left'][frame_number]
            else:
                return self.sprites['player_jump_right'][frame_number]

        # Normalnie - animacja wspinaczki
        # Zmieniamy klatkę co PLAYER_ANIMATION_SPEED klatek gry
        frame_number = (animation_counter // PLAYER_ANIMATION_SPEED) % PLAYER_CLIMB_FRAMES
        return self.sprites['player_climb'][frame_number]

    def get_bat_frame(self, animation_counter, bat_type):
        """
        Zwraca klatkę animacji nietoperza.
        
        Parametry:
            animation_counter - licznik animacji
            bat_type - 'bat_1' lub 'bat_2'
        """
        # Zmieniamy klatkę co 10 klatek gry
        frame_number = (animation_counter // 10) % BAT_ANIMATION_FRAMES
        return self.sprites[bat_type][frame_number]

    def get_enemy_frame(self, animation_counter, direction):
        """
        Zwraca klatkę animacji przeciwnika.
        
        Parametry:
            animation_counter - licznik animacji
            direction - 'left' lub 'right'
        """
        frame_number = (animation_counter // ENEMY_ANIMATION_SPEED) % ENEMY_ANIMATION_FRAMES
        
        if direction == 'left':
            return self.sprites['enemy_left'][frame_number]
        else:
            return self.sprites['enemy_right'][frame_number]

    def get_sprite(self, name):
        """
        Zwraca pojedynczy sprite (nie animację).
        Używane dla: tło, lina, moneta, powerupy.
        """
        return self.sprites.get(name)
