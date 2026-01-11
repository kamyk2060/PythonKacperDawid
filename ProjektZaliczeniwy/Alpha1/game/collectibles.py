"""
HUGO - Przedmioty do zbierania
==============================
Monety i powerupy które gracz może zebrać.
"""
import pygame
from .config import *


class Coin:
    """
    Moneta do zbierania.
    Daje 10 punktów (lub 20 z powerupem podwójnych punktów).
    """

    def __init__(self, rope_index, y, sprite_manager):
        """
        Tworzy monetę na podanej linie.
        
        Parametry:
            rope_index - numer liny (0, 1, 2)
            y - pozycja Y (zwykle ujemna - powyżej ekranu)
            sprite_manager - manager sprite'ów
        """
        self.rope_index = rope_index
        self.y = y
        self.collected = False
        self.sprite_manager = sprite_manager
        self.rotation = 0  # Kąt obrotu dla animacji

    def get_rect(self, ropes):
        """Zwraca prostokąt monety (do kolizji i rysowania)."""
        x = ropes[self.rope_index].x + ROPE_WIDTH // 2 - COIN_SIZE // 2
        return pygame.Rect(x, self.y, COIN_SIZE, COIN_SIZE)

    def update(self, scroll_speed):
        """Aktualizuje pozycję i animację."""
        self.y += scroll_speed        # Scrolluj w dół
        self.rotation = (self.rotation + 3) % 360  # Obracaj

    def draw(self, screen, ropes):
        """Rysuje monetę na ekranie."""
        if self.collected:
            return
            
        rect = self.get_rect(ropes)
        coin_sprite = self.sprite_manager.get_sprite('coin')

        if coin_sprite:
            # Obróć sprite
            rotated = pygame.transform.rotate(coin_sprite, self.rotation)
            new_rect = rotated.get_rect(center=rect.center)
            screen.blit(rotated, new_rect)
        else:
            # Fallback - żółte kółko
            pygame.draw.circle(screen, YELLOW, rect.center, COIN_SIZE // 2)
            pygame.draw.circle(screen, ORANGE, rect.center, COIN_SIZE // 2, 3)

    def is_off_screen(self):
        """Sprawdza czy moneta wyszła poza ekran."""
        return self.y > SCREEN_HEIGHT

    def check_collision(self, player_hitbox, ropes):
        """Sprawdza kolizję z graczem."""
        if not self.collected:
            if self.get_rect(ropes).colliderect(player_hitbox):
                self.collected = True
                return True
        return False


class PowerUp:
    """
    Powerup - daje specjalny efekt.
    
    Typy:
    - 'invincible' - nieśmiertelność na 3 sekundy
    - 'double_points' - podwójne punkty na 5 sekund
    """

    def __init__(self, rope_index, y, powerup_type, sprite_manager):
        """
        Tworzy powerup na podanej linie.
        
        Parametry:
            rope_index - numer liny
            y - pozycja Y
            powerup_type - 'invincible' lub 'double_points'
            sprite_manager - manager sprite'ów
        """
        self.rope_index = rope_index
        self.y = y
        self.type = powerup_type
        self.collected = False
        self.sprite_manager = sprite_manager
        self.float_offset = 0  # Offset dla efektu unoszenia

    def get_rect(self, ropes):
        """Zwraca prostokąt powerupa."""
        x = ropes[self.rope_index].x + ROPE_WIDTH // 2 - POWERUP_SIZE // 2
        return pygame.Rect(x, self.y, POWERUP_SIZE, POWERUP_SIZE)

    def update(self, scroll_speed):
        """Aktualizuje pozycję i animację."""
        self.y += scroll_speed
        
        # Efekt unoszenia (sinus)
        self.float_offset = 10 * abs(
            pygame.math.Vector2(0, 1).rotate(pygame.time.get_ticks() * 0.003).y
        )

    def draw(self, screen, ropes):
        """Rysuje powerup na ekranie."""
        if self.collected:
            return
            
        rect = self.get_rect(ropes)
        # Dodaj offset unoszenia
        draw_rect = pygame.Rect(rect.x, rect.y - self.float_offset, 
                               rect.width, rect.height)

        if self.type == 'invincible':
            sprite = self.sprite_manager.get_sprite('powerup_shield')
            if sprite:
                screen.blit(sprite, draw_rect)
            else:
                pygame.draw.rect(screen, PURPLE, draw_rect)
                pygame.draw.rect(screen, WHITE, draw_rect, 3)
                
        elif self.type == 'double_points':
            sprite = self.sprite_manager.get_sprite('powerup_star')
            if sprite:
                screen.blit(sprite, draw_rect)
            else:
                pygame.draw.rect(screen, GREEN, draw_rect)
                pygame.draw.rect(screen, WHITE, draw_rect, 3)
                font = pygame.font.Font(None, 28)
                text = font.render("x2", True, WHITE)
                screen.blit(text, (draw_rect.centerx - 12, draw_rect.centery - 10))

    def is_off_screen(self):
        """Sprawdza czy powerup wyszedł poza ekran."""
        return self.y > SCREEN_HEIGHT

    def check_collision(self, player_hitbox, ropes):
        """Sprawdza kolizję z graczem."""
        if not self.collected:
            if self.get_rect(ropes).colliderect(player_hitbox):
                self.collected = True
                return True
        return False
