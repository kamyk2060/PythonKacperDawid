"""
HUGO - Klasa Liny
=================
Lina po której wspina się gracz.
Liny mają animowaną teksturę tworzącą iluzję ruchu.
"""
import pygame
from .config import *


class Rope:
    """
    Pojedyncza lina w grze.
    
    Lina jest statyczna (nie rusza się), ale ma animowaną teksturę
    która tworzy iluzję wspinaczki gracza.
    """

    def __init__(self, x, sprite_manager):
        """
        Tworzy linę na podanej pozycji X.
        
        Parametry:
            x - pozycja pozioma liny
            sprite_manager - manager do pobierania sprite'a
        """
        self.x = x
        self.scroll_offset = 0  # Offset animacji tekstury
        self.sprite_manager = sprite_manager

    def update(self, scroll_speed, screen_height):
        """
        Aktualizuje animację scrollingu liny.
        
        Parametry:
            scroll_speed - prędkość scrollingu gry
            screen_height - wysokość ekranu (nieużywane, zostawione dla kompatybilności)
        """
        # Zwiększ offset
        self.scroll_offset += scroll_speed
        
        # Zapętl offset (tekstura ma 100px wysokości)
        if self.scroll_offset > 100:
            self.scroll_offset -= 100
        elif self.scroll_offset < -100:
            self.scroll_offset += 100

    def draw(self, screen):
        """Rysuje linę na ekranie."""
        rope_sprite = self.sprite_manager.get_sprite('rope')

        if rope_sprite:
            # Rysuj sprite'y tile'owane (powtarzane)
            for i in range(-200, SCREEN_HEIGHT + 200, 100):
                y_pos = i + int(self.scroll_offset)
                screen.blit(rope_sprite, (self.x, y_pos))
        else:
            # Fallback - prosta linia
            for i in range(-50, SCREEN_HEIGHT + 50, 15):
                y_pos = i + int(self.scroll_offset) % 15
                pygame.draw.line(
                    screen,
                    BROWN,
                    (self.x + ROPE_WIDTH // 2, y_pos),
                    (self.x + ROPE_WIDTH // 2, y_pos + 10),
                    5
                )
