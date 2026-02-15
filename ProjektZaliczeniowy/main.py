"""
HUGO - Gra
==========

Wymagania:
- Python 3.x
- Pygame (pip install pygame)

Jak uruchomić:
    python main.py
"""
import pygame
import sys
from game.game import Game


def main():
    """Główna funkcja - uruchamia grę."""
    
    # Zainicjuj Pygame
    pygame.init()
    
    # Utwórz grę
    game = Game()
    
    # Uruchom główną pętlę
    game.run()
    
    # Sprzątanie po zakończeniu
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
