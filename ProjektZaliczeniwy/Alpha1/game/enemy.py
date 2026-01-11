"""
HUGO - System Przeciwników
==========================
Przeciwnicy pojawiający się z boku lub od dołu i strzelający pociskami.
"""
import pygame
import random
from .config import *


class Enemy:
    """
    Przeciwnik strzelający pociskami.
    Może pojawić się z boku (lewo/prawo) lub od dołu ekranu.
    """

    def __init__(self, y, side, sprite_manager, from_bottom=False):
        """
        Tworzy przeciwnika.
        
        Parametry:
            y - pozycja Y (dla bocznych) lub ignorowane (dla dolnych)
            side - 'left' lub 'right' (dla bocznych) lub None (dla dolnych)
            sprite_manager - manager sprite'ów
            from_bottom - True jeśli pojawia się od dołu
        """
        self.side = side
        self.y = y
        self.sprite_manager = sprite_manager
        self.from_bottom = from_bottom
        
        self.shoot_cooldown = 0      # Timer między strzałami
        self.has_entered = False     # Czy dotarł na pozycję
        self.time_on_screen = 0      # Czas na ekranie
        self.anim_counter = 0

        if from_bottom:
            # Enemy od dołu
            self.side = 'bottom'
            self.y = SCREEN_HEIGHT + ENEMY_HEIGHT
            self.target_y = SCREEN_HEIGHT - ENEMY_HEIGHT - 100
            self.x = 50 if random.random() < 0.5 else SCREEN_WIDTH - ENEMY_WIDTH - 50
            self.actual_side = 'left' if self.x < SCREEN_WIDTH // 2 else 'right'
            self.enter_speed_y = -5
        elif side == 'left':
            # Enemy z lewej
            self.x = -ENEMY_WIDTH
            self.target_x = 50
            self.actual_side = 'left'
        else:
            # Enemy z prawej
            self.x = SCREEN_WIDTH
            self.target_x = SCREEN_WIDTH - ENEMY_WIDTH - 50
            self.actual_side = 'right'

        self.rect = pygame.Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.enter_speed = 5

    def update(self, scroll_speed):
        """Aktualizuje pozycję i stan."""
        # Faza wjazdu
        if not self.has_entered:
            if self.from_bottom:
                self.y = max(self.y + self.enter_speed_y, self.target_y)
                if self.y <= self.target_y:
                    self.has_entered = True
            elif self.side == 'left':
                self.x = min(self.x + self.enter_speed, self.target_x)
                if self.x >= self.target_x:
                    self.has_entered = True
            else:
                self.x = max(self.x - self.enter_speed, self.target_x)
                if self.x <= self.target_x:
                    self.has_entered = True
        else:
            # Scrolluj z grą (tylko boczni)
            if not self.from_bottom:
                self.y += scroll_speed

        # Aktualizuj rect
        self.rect.x = self.x
        self.rect.y = self.y

        # Timery
        if self.has_entered:
            self.time_on_screen += 1
        self.anim_counter += 1
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def can_shoot(self):
        """Sprawdza czy może strzelić i ewentualnie strzela."""
        if self.has_entered and self.shoot_cooldown <= 0:
            base_chance = ENEMY_SHOOT_CHANCE
            time_bonus = min(self.time_on_screen / 300, 0.02)
            
            if random.random() < (base_chance + time_bonus):
                self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
                return True
        return False

    def draw(self, screen):
        """Rysuje przeciwnika."""
        display_side = self.actual_side if hasattr(self, 'actual_side') else self.side
        sprite = self.sprite_manager.get_enemy_frame(self.anim_counter, display_side)

        if sprite:
            screen.blit(sprite, self.rect)
        else:
            # Fallback
            if self.from_bottom:
                color = (50, 200, 50)
            else:
                color = (200, 50, 50) if display_side == 'left' else (50, 50, 200)
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 3)

    def is_off_screen(self):
        """Sprawdza czy wyszedł poza ekran."""
        return self.y > SCREEN_HEIGHT + 100


class Projectile:
    """
    Pocisk wystrzeliwany przez przeciwnika.
    Leci poziomo (w lewo lub prawo).
    """

    def __init__(self, x, y, direction):
        """
        Tworzy pocisk.
        
        Parametry:
            x, y - pozycja startowa
            direction - 1 (w prawo) lub -1 (w lewo)
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 7
        self.radius = 10
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)

    def update(self):
        """Aktualizuje pozycję."""
        self.x += self.speed * self.direction
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        """Rysuje pocisk (pomarańczowa kula)."""
        center_x = int(self.x)
        center_y = int(self.y)
        
        # Główna kula
        pygame.draw.circle(screen, ORANGE, (center_x, center_y), self.radius)
        # Świecenie w środku
        pygame.draw.circle(screen, (255, 200, 100), (center_x, center_y), self.radius - 2)
        # Obramowanie
        pygame.draw.circle(screen, RED, (center_x, center_y), self.radius, 1)

    def is_off_screen(self):
        """Sprawdza czy wyszedł poza ekran."""
        if self.direction == 1:
            return self.x > SCREEN_WIDTH + 50
        else:
            return self.x < -50

    def check_collision(self, player_rect):
        """Sprawdza kolizję z graczem."""
        return self.rect.colliderect(player_rect)


class EnemyManager:
    """
    Główny manager przeciwników i pocisków.
    """

    def __init__(self):
        self.enemies = []
        self.projectiles = []

    def add_enemy(self, enemy):
        """Dodaje nowego przeciwnika."""
        self.enemies.append(enemy)

    def update_all(self, scroll_speed):
        """Aktualizuje wszystkich przeciwników i pociski."""
        for enemy in self.enemies:
            enemy.update(scroll_speed)
        for projectile in self.projectiles:
            projectile.update()

        # Usuń te poza ekranem
        self.enemies = [e for e in self.enemies if not e.is_off_screen()]
        self.projectiles = [p for p in self.projectiles if not p.is_off_screen()]

    def draw_all(self, screen):
        """Rysuje wszystkich przeciwników i pociski."""
        for enemy in self.enemies:
            enemy.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)

    def check_projectile_collisions(self, player_rect):
        """Sprawdza kolizje pocisków z graczem."""
        for projectile in self.projectiles:
            if projectile.check_collision(player_rect):
                return True
        return False

    def can_spawn_enemy(self):
        """Sprawdza czy można dodać nowego enemy (max 2)."""
        return len(self.enemies) < ENEMY_MAX_ON_SCREEN
