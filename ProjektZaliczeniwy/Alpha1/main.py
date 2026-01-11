"""
Hugo Game - Główny plik uruchomieniowy
======================================
Uruchom ten plik żeby zagrać: python main.py
"""
import pygame
import sys
from game.game import Game


def main():
    """Uruchamia grę."""
    # Inicjalizacja Pygame
    pygame.init()
    
    # Utworzenie i uruchomienie gry
    game = Game()
    game.run()
    
    # Sprzątanie po zakończeniu
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
