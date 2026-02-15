"""
HUGO - Klasa Liny
=================
Lina po której wspina się gracz.
Liny wyglądają jakby się przesuwały w dół - to tworzy iluzję wspinaczki.
"""
import pygame
from .config import *


class Rope:
    """
    Pojedyncza lina w grze.
    
    Lina ma animowaną teksturę która scrolluje (przesuwa się),
    co tworzy efekt ruchu/wspinaczki.
    """

    def __init__(self, x, sprite_manager):
        """
        Tworzy linę.
        
        Parametry:
            x - pozycja pozioma liny
            sprite_manager - obiekt do pobierania grafik
        """
        self.x = x  # Pozycja X (nie zmienia się)
        self.scroll_offset = 0  # Przesunięcie tekstury (animacja)
        self.sprite_manager = sprite_manager

    def update(self, scroll_speed):
        """
        Aktualizuje animację liny.
        
        Parametry:
            scroll_speed - prędkość scrollowania gry
        """
        # Przesuń teksturę
        self.scroll_offset += scroll_speed
        
        # Zapętl (tekstura ma 100px wysokości)
        if self.scroll_offset > 100:
            self.scroll_offset -= 100

    def draw(self, screen):
        """Rysuje linę na ekranie."""
        rope_sprite = self.sprite_manager.get_sprite('rope')
        
        # Rysuj teksturę liny wielokrotnie (od góry do dołu ekranu)
        # Zaczynamy od -200 żeby nie było "dziury" na górze
        y = -200
        while y < SCREEN_HEIGHT + 200:
            draw_y = y + int(self.scroll_offset)
            screen.blit(rope_sprite, (self.x, draw_y))
            y += 100  # Tekstura ma 100px wysokości
