"""
HUGO - Klasa Gracza
===================
Obsługuje wszystko związane z postacią Hugo:
- Sterowanie (klawiatura)
- Ruch między linami
- Animacje
- Nieśmiertelność (powerup)
"""
import pygame
from .config import *


class Player:
    """
    Gracz - Hugo wspinający się po linach.
    """

    def __init__(self, x, y, sprite_manager):
        """
        Tworzy gracza.
        
        Parametry:
            x, y - pozycja startowa
            sprite_manager - obiekt do pobierania grafik
        """
        # -----------------------------------------
        # POZYCJA I ROZMIAR
        # -----------------------------------------
        # Prostokąt do rysowania (pełny rozmiar obrazka)
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Hitbox do kolizji - MNIEJSZY niż obrazek!
        # Dzięki temu gra jest sprawiedliwa - możesz "otrzeć się" o przeszkodę
        hitbox_width = int(PLAYER_WIDTH * PLAYER_HITBOX_SCALE)
        hitbox_height = int(PLAYER_HEIGHT * PLAYER_HITBOX_SCALE)
        
        # Wyśrodkuj hitbox w obrazku
        offset_x = (PLAYER_WIDTH - hitbox_width) // 2
        offset_y = (PLAYER_HEIGHT - hitbox_height) // 2
        self.hitbox = pygame.Rect(x + offset_x, y + offset_y, hitbox_width, hitbox_height)
        
        # -----------------------------------------
        # STAN GRACZA
        # -----------------------------------------
        self.current_rope = 1  # Na której linie jest gracz (0, 1, 2)
        
        # Nieśmiertelność (z powerupa)
        self.invincible = False
        self.invincible_timer = 0  # Ile klatek zostało nieśmiertelności
        
        # -----------------------------------------
        # SYSTEM RUCHU MIĘDZY LINAMI
        # -----------------------------------------
        self.is_moving = False      # Czy w trakcie przeskoku
        self.target_x = x           # Dokąd zmierzamy
        self.move_cooldown = 0      # Czas do następnego skoku
        
        # -----------------------------------------
        # ANIMACJA SKOKU
        # -----------------------------------------
        self.is_jumping = False
        self.jump_direction = None  # 'left' lub 'right'
        self.jump_progress = 0      # 0-20 (postęp animacji)
        
        # -----------------------------------------
        # ANIMACJA OGÓLNA
        # -----------------------------------------
        self.sprite_manager = sprite_manager
        self.animation_counter = 0  # Licznik do animacji

    def handle_input(self, keys, ropes):
        """
        Obsługuje sterowanie gracza.
        
        Parametry:
            keys - stan klawiszy (z pygame.key.get_pressed())
            ropes - lista lin (żeby wiedzieć gdzie się przesunąć)
        """
        # -----------------------------------------
        # RUCH GÓRA/DÓŁ
        # -----------------------------------------
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED
        
        # Nie wychodź poza ekran
        if self.rect.y < PLAYER_MIN_Y:
            self.rect.y = PLAYER_MIN_Y
        if self.rect.y > PLAYER_MAX_Y:
            self.rect.y = PLAYER_MAX_Y

        # -----------------------------------------
        # COOLDOWN SKOKU
        # -----------------------------------------
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        # -----------------------------------------
        # ZMIANA LINY (SKOK)
        # -----------------------------------------
        # Możemy skakać tylko jeśli nie jesteśmy w ruchu i cooldown = 0
        if not self.is_moving and self.move_cooldown == 0:
            
            # Skok w lewo
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.current_rope > 0:  # Nie jesteśmy na lewej skrajnej
                    self.current_rope -= 1
                    self._start_jump('left', ropes)
            
            # Skok w prawo
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.current_rope < NUM_ROPES - 1:  # Nie jesteśmy na prawej skrajnej
                    self.current_rope += 1
                    self._start_jump('right', ropes)

        # -----------------------------------------
        # PŁYNNY RUCH DO CELU
        # -----------------------------------------
        if self.is_moving:
            # Oblicz odległość do celu
            distance = abs(self.rect.x - self.target_x)
            
            if distance > 2:
                # Ruszaj się w stronę celu
                speed = min(7, distance)  # Max 7 pikseli na klatkę
                
                if self.rect.x < self.target_x:
                    self.rect.x += speed  # W prawo
                else:
                    self.rect.x -= speed  # W lewo
            else:
                # Dotarliśmy do celu
                self.rect.x = self.target_x
                self.is_moving = False

        # -----------------------------------------
        # ANIMACJA SKOKU
        # -----------------------------------------
        if self.is_jumping:
            self.jump_progress += 1
            
            if self.jump_progress > 20:
                # Koniec animacji skoku
                self.is_jumping = False
                self.jump_progress = 0

        # -----------------------------------------
        # AKTUALIZUJ POZYCJĘ HITBOXA
        # -----------------------------------------
        # Hitbox musi "podążać" za obrazkiem
        hitbox_width = int(PLAYER_WIDTH * PLAYER_HITBOX_SCALE)
        hitbox_height = int(PLAYER_HEIGHT * PLAYER_HITBOX_SCALE)
        offset_x = (PLAYER_WIDTH - hitbox_width) // 2
        offset_y = (PLAYER_HEIGHT - hitbox_height) // 2
        
        self.hitbox.x = self.rect.x + offset_x
        self.hitbox.y = self.rect.y + offset_y

    def _start_jump(self, direction, ropes):
        """Rozpoczyna skok na inną linę."""
        self.move_cooldown = 30  # Poczekaj 30 klatek przed następnym skokiem
        self.is_moving = True
        self.is_jumping = True
        self.jump_direction = direction
        self.jump_progress = 0
        
        # Oblicz gdzie mamy dolecieć (środek nowej liny)
        target_rope = ropes[self.current_rope]
        self.target_x = target_rope.x + ROPE_WIDTH // 2 - PLAYER_WIDTH // 2

    def update(self):
        """Aktualizuje stan gracza (wywoływane co klatkę)."""
        # Zwiększ licznik animacji
        self.animation_counter += 1
        if self.animation_counter > 1000:
            self.animation_counter = 0
        
        # Obsłuż timer nieśmiertelności
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def activate_invincibility(self):
        """Włącza nieśmiertelność na 3 sekundy."""
        self.invincible = True
        self.invincible_timer = 180  # 3 sekundy * 60 FPS = 180 klatek

    def draw(self, screen):
        """Rysuje gracza na ekranie."""
        # Pobierz odpowiednią klatkę animacji
        sprite = self.sprite_manager.get_player_frame(
            self.animation_counter,
            self.is_jumping,
            self.jump_direction,
            self.jump_progress
        )

        # Efekt migania podczas nieśmiertelności
        if self.invincible:
            # Migaj co 10 klatek (5 klatek widoczny, 5 niewidoczny)
            if self.invincible_timer % 10 < 5:
                return  # Nie rysuj - gracz "znika" na chwilę

        # Narysuj gracza
        screen.blit(sprite, self.rect)
