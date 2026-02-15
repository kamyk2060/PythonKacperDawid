"""
HUGO - Przedmioty do zbierania
==============================
Monety i powerupy które gracz może zebrać.
"""
import pygame
from .config import *


class Coin:
    """
    Moneta - zbierz ją żeby dostać punkty!
    """

    def __init__(self, rope_index, y, sprite_manager):
        """
        Tworzy monetę.
        
        Parametry:
            rope_index - na której linie (0, 1 lub 2)
            y - pozycja Y (zwykle ujemna - powyżej ekranu)
            sprite_manager - do pobierania grafiki
        """
        self.rope_index = rope_index
        self.y = y
        self.sprite_manager = sprite_manager
        
        self.collected = False  # Czy już zebrana
        self.rotation = 0  # Kąt obrotu (animacja)

    def get_rect(self, ropes):
        """Oblicza prostokąt monety (potrzebne do rysowania i kolizji)."""
        # Środek liny minus połowa rozmiaru monety
        x = ropes[self.rope_index].x + ROPE_WIDTH // 2 - COIN_SIZE // 2
        return pygame.Rect(x, self.y, COIN_SIZE, COIN_SIZE)

    def update(self, scroll_speed):
        """Aktualizuje monetę (ruch w dół + obracanie)."""
        # Przesuń w dół (scrollowanie)
        self.y += scroll_speed
        
        # Obracaj monetę (efekt wizualny)
        self.rotation += 3
        if self.rotation >= 360:
            self.rotation = 0

    def draw(self, screen, ropes):
        """Rysuje monetę na ekranie."""
        if self.collected:
            return  # Nie rysuj zebranych monet
        
        rect = self.get_rect(ropes)
        coin_sprite = self.sprite_manager.get_sprite('coin')
        
        # Obróć sprite
        rotated = pygame.transform.rotate(coin_sprite, self.rotation)
        
        # Wyśrodkuj obrócony obrazek
        new_rect = rotated.get_rect(center=rect.center)
        screen.blit(rotated, new_rect)

    def is_off_screen(self):
        """Sprawdza czy moneta wyszła poza ekran (do usunięcia)."""
        return self.y > SCREEN_HEIGHT

    def check_collision(self, player_hitbox, ropes):
        """Sprawdza czy gracz zebrał monetę."""
        if self.collected:
            return False
        
        my_rect = self.get_rect(ropes)
        if my_rect.colliderect(player_hitbox):
            self.collected = True
            return True
        
        return False


class PowerUp:
    """
    Powerup - daje specjalną moc na chwilę.
    
    Typy:
    - 'invincible' - nieśmiertelność (3 sekundy)
    - 'double_points' - podwójne punkty (5 sekund)
    """

    def __init__(self, rope_index, y, powerup_type, sprite_manager):
        """
        Tworzy powerup.
        
        Parametry:
            rope_index - na której linie
            y - pozycja Y
            powerup_type - typ powerupa ('invincible' lub 'double_points')
            sprite_manager - do pobierania grafiki
        """
        self.rope_index = rope_index
        self.y = y
        self.type = powerup_type
        self.sprite_manager = sprite_manager
        
        self.collected = False
        self.float_offset = 0  # Do animacji "unoszenia się"

    def get_rect(self, ropes):
        """Oblicza prostokąt powerupa."""
        x = ropes[self.rope_index].x + ROPE_WIDTH // 2 - POWERUP_SIZE // 2
        return pygame.Rect(x, self.y, POWERUP_SIZE, POWERUP_SIZE)

    def update(self, scroll_speed):
        """Aktualizuje powerup (ruch w dół + unoszenie)."""
        self.y += scroll_speed
        


    def draw(self, screen, ropes):
        """Rysuje powerup na ekranie."""
        if self.collected:
            return
        
        rect = self.get_rect(ropes)
        
        # Dodaj efekt unoszenia
        draw_y = rect.y - self.float_offset
        draw_rect = pygame.Rect(rect.x, draw_y, rect.width, rect.height)
        
        # Wybierz odpowiedni sprite
        if self.type == 'invincible':
            sprite = self.sprite_manager.get_sprite('powerup_shield')
        else:
            sprite = self.sprite_manager.get_sprite('powerup_star')
        
        screen.blit(sprite, draw_rect)

    def is_off_screen(self):
        """Sprawdza czy powerup wyszedł poza ekran."""
        return self.y > SCREEN_HEIGHT

    def check_collision(self, player_hitbox, ropes):
        """Sprawdza czy gracz zebrał powerup."""
        if self.collected:
            return False
        
        my_rect = self.get_rect(ropes)
        if my_rect.colliderect(player_hitbox):
            self.collected = True
            return True
        
        return False
