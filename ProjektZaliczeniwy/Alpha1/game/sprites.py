"""
HUGO - Manager Sprite'ów
========================
Ładuje i zarządza wszystkimi grafikami w grze.
Jeśli grafiki nie istnieją, gra używa prostych kształtów jako fallback.
"""
import pygame
import os
from .config import *


class SpriteManager:
    """
    Zarządza wszystkimi sprite'ami (grafikami) w grze.
    
    Główne zadania:
    - Ładowanie grafik z dysku
    - Dzielenie sprite sheets na pojedyncze klatki
    - Udostępnianie sprite'ów innym modułom
    """

    def __init__(self):
        # Słownik przechowujący wszystkie sprite'y
        # Klucz = nazwa, Wartość = Surface lub lista Surface'ów (dla animacji)
        self.sprites = {}
        
        # Flaga - czy używamy grafik czy fallbacków
        self.use_sprites = True
        
        # Próbujemy załadować grafiki
        self.load_sprites()

    def load_sprites(self):
        """
        Ładuje wszystkie sprite'y z katalogu sprites/
        Jeśli coś pójdzie nie tak, ustawia use_sprites = False
        i gra będzie używać prostych kształtów.
        """
        try:
            # Sprawdź czy katalog istnieje
            if not os.path.exists(SPRITES_DIR):
                print(f"[SPRITES] Brak katalogu '{SPRITES_DIR}' - używam fallbacków")
                self.use_sprites = False
                return

            # Pomocnicza funkcja do ładowania pliku
            def load(filename):
                path = os.path.join(SPRITES_DIR, filename)
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Brak pliku: {filename}")
                return pygame.image.load(path).convert_alpha()

            # ===============================================
            # GRACZ - animacja wspinaczki (7 klatek)
            # ===============================================
            climb_sheet = load(SPRITE_FILES['player_climb'])
            self.sprites['player_climb'] = [
                climb_sheet.subsurface((i * PLAYER_FRAME_WIDTH, 0, 
                                       PLAYER_FRAME_WIDTH, PLAYER_HEIGHT))
                for i in range(PLAYER_CLIMB_FRAMES)
            ]

            # ===============================================
            # GRACZ - animacja skoku (4 klatki w każdą stronę)
            # ===============================================
            jump_left = load(SPRITE_FILES['player_jump_left'])
            self.sprites['player_jump_left'] = [
                jump_left.subsurface((i * PLAYER_JUMP_FRAME_WIDTH, 0,
                                     PLAYER_JUMP_FRAME_WIDTH, PLAYER_HEIGHT))
                for i in range(PLAYER_JUMP_FRAMES)
            ]

            jump_right = load(SPRITE_FILES['player_jump_right'])
            self.sprites['player_jump_right'] = [
                jump_right.subsurface((i * PLAYER_JUMP_FRAME_WIDTH, 0,
                                      PLAYER_JUMP_FRAME_WIDTH, PLAYER_HEIGHT))
                for i in range(PLAYER_JUMP_FRAMES)
            ]

            # ===============================================
            # TŁO I LINY
            # ===============================================
            self.sprites['background'] = load(SPRITE_FILES['background'])
            self.sprites['rope'] = load(SPRITE_FILES['rope'])

            # ===============================================
            # MONETA
            # ===============================================
            self.sprites['coin'] = load(SPRITE_FILES['coin'])

            # ===============================================
            # NIETOPERZE (3 klatki animacji każdy)
            # ===============================================
            bat1_sheet = load(SPRITE_FILES['bat_1'])
            self.sprites['bat_1'] = [
                bat1_sheet.subsurface((i * BAT_FRAME_SIZE, 0, 
                                      BAT_FRAME_SIZE, BAT_FRAME_SIZE))
                for i in range(BAT_ANIMATION_FRAMES)
            ]

            bat2_sheet = load(SPRITE_FILES['bat_2'])
            self.sprites['bat_2'] = [
                bat2_sheet.subsurface((i * BAT_FRAME_SIZE, 0, 
                                      BAT_FRAME_SIZE, BAT_FRAME_SIZE))
                for i in range(BAT_ANIMATION_FRAMES)
            ]

            # ===============================================
            # POWERUPY
            # ===============================================
            self.sprites['powerup_shield'] = load(SPRITE_FILES['powerup_shield'])
            self.sprites['powerup_star'] = load(SPRITE_FILES['powerup_star'])

            # ===============================================
            # ENEMY (2 klatki + odbicie lustrzane)
            # ===============================================
            enemy_sheet = load(SPRITE_FILES['enemy'])
            
            # Enemy patrzący w lewo (oryginał)
            self.sprites['enemy_left'] = [
                enemy_sheet.subsurface((i * ENEMY_WIDTH, 0, ENEMY_WIDTH, ENEMY_HEIGHT))
                for i in range(ENEMY_ANIMATION_FRAMES)
            ]
            
            # Enemy patrzący w prawo (odbicie lustrzane)
            self.sprites['enemy_right'] = [
                pygame.transform.flip(frame, True, False)
                for frame in self.sprites['enemy_left']
            ]

            print("[SPRITES] Wszystkie grafiki załadowane!")

        except Exception as e:
            print(f"[SPRITES] Błąd ładowania: {e}")
            print("[SPRITES] Używam prostych kształtów jako fallback")
            self.use_sprites = False

    # =========================================================================
    # METODY POBIERANIA SPRITE'ÓW
    # =========================================================================

    def get_player_frame(self, anim_frame, is_jumping, jump_direction, jump_progress=0):
        """
        Zwraca odpowiednią klatkę animacji gracza.
        
        Parametry:
            anim_frame - globalny licznik animacji
            is_jumping - czy gracz skacze
            jump_direction - 'left' lub 'right'
            jump_progress - postęp skoku (0-20)
        """
        if not self.use_sprites:
            return None

        # Jeśli skacze - użyj animacji skoku
        if is_jumping and jump_direction:
            # Przelicz postęp skoku na numer klatki (0-3)
            frame = min(int((jump_progress / 20.0) * PLAYER_JUMP_FRAMES), 
                       PLAYER_JUMP_FRAMES - 1)
            
            if jump_direction == 'left':
                return self.sprites['player_jump_left'][frame]
            else:
                return self.sprites['player_jump_right'][frame]

        # Normalnie - animacja wspinaczki
        frame = (anim_frame // PLAYER_ANIMATION_SPEED) % PLAYER_CLIMB_FRAMES
        return self.sprites['player_climb'][frame]

    def get_bat_frame(self, anim_counter, bat_type):
        """
        Zwraca klatkę animacji nietoperza.
        
        Parametry:
            anim_counter - licznik animacji
            bat_type - 'bat_1' lub 'bat_2'
        """
        if not self.use_sprites:
            return None
            
        frame = (anim_counter // 10) % BAT_ANIMATION_FRAMES
        return self.sprites[bat_type][frame]

    def get_enemy_frame(self, anim_counter, side):
        """
        Zwraca klatkę animacji enemy.
        
        Parametry:
            anim_counter - licznik animacji  
            side - 'left' lub 'right'
        """
        if not self.use_sprites:
            return None
            
        frame = (anim_counter // ENEMY_ANIMATION_SPEED) % ENEMY_ANIMATION_FRAMES
        
        if side == 'left':
            return self.sprites['enemy_left'][frame]
        else:
            return self.sprites['enemy_right'][frame]

    def get_sprite(self, name):
        """
        Zwraca pojedynczy sprite (nie animację).
        Używane dla: tło, lina, moneta, powerupy.
        """
        if not self.use_sprites:
            return None
        return self.sprites.get(name)
