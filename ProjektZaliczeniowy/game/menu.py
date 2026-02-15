"""
HUGO - Menu Gry
===============
Ekran startowy i ekran Game Over.
Proste i czytelne menu.
"""
import pygame
from .config import *


class Menu:
    """
    Obsługuje menu gry.
    """

    def __init__(self, screen, sprite_manager):
        """
        Tworzy menu.
        
        Parametry:
            screen - ekran pygame
            sprite_manager - do pobierania tła
        """
        self.screen = screen
        self.sprite_manager = sprite_manager
        
        # Czcionki
        self.title_font = pygame.font.Font(None, 80)
        self.header_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)

    def draw_main_menu(self):
        """Rysuje główne menu."""
        # -----------------------------------------
        # TŁO
        # -----------------------------------------
        background = self.sprite_manager.get_sprite('background')
        self.screen.blit(background, (0, 0))
        
        # Przyciemnienie żeby tekst był czytelny
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dark_overlay.fill(BLACK)
        dark_overlay.set_alpha(180)  # Przezroczystość
        self.screen.blit(dark_overlay, (0, 0))
        
        # -----------------------------------------
        # TYTUŁ
        # -----------------------------------------
        title = self.title_font.render("HUGO", True, YELLOW)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, 80))
        
        subtitle = self.header_font.render("Wspinaczka po Linach", True, WHITE)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        self.screen.blit(subtitle, (subtitle_x, 160))
        
        # Linia dekoracyjna
        pygame.draw.line(self.screen, YELLOW, (200, 210), (800, 210), 2)
        
        # -----------------------------------------
        # STEROWANIE
        # -----------------------------------------
        y = 260
        
        header = self.header_font.render("STEROWANIE", True, YELLOW)
        self.screen.blit(header, (150, y))
        y += 45
        
        controls = [
            "Strzalki / WASD  -  Ruch",
            "Lewo / Prawo  -  Zmiana liny",
            "Gora / Dol  -  Ruch pionowy",
        ]
        for text in controls:
            rendered = self.text_font.render(text, True, WHITE)
            self.screen.blit(rendered, (170, y))
            y += 35
        
        # -----------------------------------------
        # CEL GRY
        # -----------------------------------------
        y += 30
        
        header = self.header_font.render("CEL GRY", True, YELLOW)
        self.screen.blit(header, (150, y))
        y += 45
        
        goals = [
            "Wspinaj sie jak najwyzej",
            "Zbieraj monety (+10 pkt)",
            "Unikaj przeszkod i pociskow",
        ]
        for text in goals:
            rendered = self.text_font.render(text, True, WHITE)
            self.screen.blit(rendered, (170, y))
            y += 35
        
        # -----------------------------------------
        # POWERUPY
        # -----------------------------------------
        y += 30
        
        header = self.header_font.render("POWERUPY", True, YELLOW)
        self.screen.blit(header, (150, y))
        y += 50
        
        # Fioletowy - nieśmiertelność
        pygame.draw.rect(self.screen, PURPLE, (170, y, 35, 35))
        pygame.draw.rect(self.screen, WHITE, (170, y, 35, 35), 2)
        text = self.text_font.render("Niesmiertelnosc (3 sek)", True, WHITE)
        self.screen.blit(text, (220, y + 5))
        y += 50
        
        # Zielony - podwójne punkty
        pygame.draw.rect(self.screen, GREEN, (170, y, 35, 35))
        pygame.draw.rect(self.screen, WHITE, (170, y, 35, 35), 2)
        text = self.text_font.render("Podwojne punkty (5 sek)", True, WHITE)
        self.screen.blit(text, (220, y + 5))
        
        # -----------------------------------------
        # PRZYCISK START
        # -----------------------------------------
        button_text = self.header_font.render("Nacisnij SPACJE aby grac", True, BLACK)
        button_width = button_text.get_width() + 60
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = 800
        
        pygame.draw.rect(self.screen, YELLOW, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.screen, WHITE, (button_x, button_y, button_width, button_height), 3)
        
        self.screen.blit(button_text, (button_x + 30, button_y + 12))
        
        # Info o ESC
        esc_text = self.text_font.render("ESC - Wyjscie", True, (150, 150, 150))
        esc_x = SCREEN_WIDTH // 2 - esc_text.get_width() // 2
        self.screen.blit(esc_text, (esc_x, 870))

    def draw_game_over(self, score, distance_meters):
        """
        Rysuje ekran Game Over.
        
        Parametry:
            score - wynik gracza
            distance_meters - przebyty dystans w metrach
        """
        # Przyciemnienie
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dark_overlay.fill(BLACK)
        dark_overlay.set_alpha(200)
        self.screen.blit(dark_overlay, (0, 0))
        
        # GAME OVER
        title = self.title_font.render("GAME OVER", True, RED)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, SCREEN_HEIGHT // 2 - 120))
        
        # Wynik
        score_text = self.header_font.render(f"Wynik: {score} pkt", True, WHITE)
        score_x = SCREEN_WIDTH // 2 - score_text.get_width() // 2
        self.screen.blit(score_text, (score_x, SCREEN_HEIGHT // 2 - 30))
        
        # Dystans
        dist_text = self.text_font.render(f"Dystans: {distance_meters} m", True, WHITE)
        dist_x = SCREEN_WIDTH // 2 - dist_text.get_width() // 2
        self.screen.blit(dist_text, (dist_x, SCREEN_HEIGHT // 2 + 20))
        
        # Opcje
        restart_text = self.header_font.render("SPACJA - Zagraj ponownie", True, YELLOW)
        restart_x = SCREEN_WIDTH // 2 - restart_text.get_width() // 2
        self.screen.blit(restart_text, (restart_x, SCREEN_HEIGHT // 2 + 90))
        
        menu_text = self.text_font.render("ESC - Menu glowne", True, YELLOW)
        menu_x = SCREEN_WIDTH // 2 - menu_text.get_width() // 2
        self.screen.blit(menu_text, (menu_x, SCREEN_HEIGHT // 2 + 140))
