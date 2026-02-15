"""
HUGO - Przeciwnicy
==================
Przeciwnicy pojawiają się z boku lub od dołu i strzelają pociskami.
"""
import pygame
import random
from .config import *


class Enemy:
    """
    Przeciwnik strzelający pociskami.
    Może pojawić się z lewej, prawej lub od dołu ekranu.
    """

    def __init__(self, y, side, sprite_manager, from_bottom=False):
        """
        Tworzy przeciwnika.
        
        Parametry:
            y - pozycja Y (dla bocznych)
            side - 'left' lub 'right' (skąd wjeżdża)
            sprite_manager - do pobierania grafiki
            from_bottom - czy pojawia się od dołu
        """
        self.sprite_manager = sprite_manager
        self.from_bottom = from_bottom
        
        self.has_entered = False  # Czy już wjechał na ekran
        self.shoot_cooldown = 0   # Czas do następnego strzału
        self.time_on_screen = 0   # Jak długo jest na ekranie
        self.animation_counter = 0
        
        # -----------------------------------------
        # USTAW POZYCJĘ STARTOWĄ
        # -----------------------------------------
        if from_bottom:
            # Wjeżdża od dołu
            self.y = SCREEN_HEIGHT + ENEMY_HEIGHT
            self.target_y = SCREEN_HEIGHT - ENEMY_HEIGHT - 100
            
            # Losowo po lewej lub prawej stronie
            if random.random() < 0.5:
                self.x = 50
                self.direction = 'left'  # Patrzy w prawo (strzela w prawo)
            else:
                self.x = SCREEN_WIDTH - ENEMY_WIDTH - 50
                self.direction = 'right'  # Patrzy w lewo (strzela w lewo)
        else:
            # Wjeżdża z boku
            self.y = y
            
            if side == 'left':
                self.x = -ENEMY_WIDTH  # Startuje poza ekranem
                self.target_x = 50     # Docelowa pozycja
                self.direction = 'left'
            else:
                self.x = SCREEN_WIDTH
                self.target_x = SCREEN_WIDTH - ENEMY_WIDTH - 50
                self.direction = 'right'
        
        # Prostokąt do rysowania
        self.rect = pygame.Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def update(self, scroll_speed):
        """Aktualizuje przeciwnika."""
        # -----------------------------------------
        # FAZA WJAZDU
        # -----------------------------------------
        if not self.has_entered:
            if self.from_bottom:
                # Jedź do góry
                self.y -= 5
                if self.y <= self.target_y:
                    self.y = self.target_y
                    self.has_entered = True
            else:
                # Jedź w bok
                if self.direction == 'left':
                    self.x += 5
                    if self.x >= self.target_x:
                        self.x = self.target_x
                        self.has_entered = True
                else:
                    self.x -= 5
                    if self.x <= self.target_x:
                        self.x = self.target_x
                        self.has_entered = True
        else:
            # Scrolluj razem ze światem (tylko boczni)
            if not self.from_bottom:
                self.y += scroll_speed
            
            self.time_on_screen += 1
        
        # Aktualizuj rect
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Liczniki
        self.animation_counter += 1
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def can_shoot(self):
        """
        Sprawdza czy przeciwnik może strzelić.
        Zwraca True jeśli właśnie strzelił.
        """
        if not self.has_entered:
            return False
        
        if self.shoot_cooldown > 0:
            return False
        
        # Losowa szansa na strzał (większa im dłużej jest na ekranie)
        chance = ENEMY_SHOOT_CHANCE + min(self.time_on_screen / 500, 0.02)
        
        if random.random() < chance:
            self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
            return True
        
        return False

    def get_projectile_spawn_point(self):
        """Zwraca pozycję z której leci pocisk."""
        # Pocisk leci z przodu przeciwnika
        if self.direction == 'left':
            x = self.x + ENEMY_WIDTH  # Prawa strona
        else:
            x = self.x  # Lewa strona
        
        y = self.y + ENEMY_HEIGHT // 2  # Środek wysokości
        
        # Kierunek: 1 = w prawo, -1 = w lewo
        direction = 1 if self.direction == 'left' else -1
        
        return x, y, direction

    def draw(self, screen):
        """Rysuje przeciwnika."""
        sprite = self.sprite_manager.get_enemy_frame(self.animation_counter, self.direction)
        screen.blit(sprite, self.rect)

    def is_off_screen(self):
        """Sprawdza czy wyleciał poza ekran."""
        return self.y > SCREEN_HEIGHT + 100


class Projectile:
    """
    Pocisk strzelany przez przeciwnika.
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
        
        # Prostokąt do kolizji
        self.rect = pygame.Rect(
            x - self.radius,
            y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def update(self):
        """Przesuwa pocisk."""
        self.x += self.speed * self.direction
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        """Rysuje pocisk (pomarańczowa kula)."""
        center = (int(self.x), int(self.y))
        
        # Główna kula
        pygame.draw.circle(screen, ORANGE, center, self.radius)
        
        # Jaśniejszy środek
        pygame.draw.circle(screen, (255, 200, 100), center, self.radius - 3)
        
        # Obramowanie
        pygame.draw.circle(screen, RED, center, self.radius, 2)

    def is_off_screen(self):
        """Sprawdza czy wyleciał poza ekran."""
        return self.x < -50 or self.x > SCREEN_WIDTH + 50

    def check_collision(self, player_hitbox):
        """Sprawdza kolizję z graczem."""
        return self.rect.colliderect(player_hitbox)


class EnemyManager:
    """
    Zarządza wszystkimi przeciwnikami i pociskami.
    """

    def __init__(self):
        self.enemies = []
        self.projectiles = []
        self.last_spawn_distance = 0

    def try_spawn(self, current_distance, sprite_manager):
        """Próbuje utworzyć nowego przeciwnika."""
        # Sprawdź czy czas na nowego
        if current_distance - self.last_spawn_distance < ENEMY_SPAWN_DISTANCE:
            return
        
        # Sprawdź limit na ekranie
        if len(self.enemies) >= ENEMY_MAX_ON_SCREEN:
            return
        
        # Losuj typ (od dołu lub z boku)
        from_bottom = random.random() < ENEMY_FROM_BOTTOM_CHANCE
        
        if from_bottom:
            enemy = Enemy(0, None, sprite_manager, from_bottom=True)
        else:
            side = random.choice(['left', 'right'])
            y = random.randint(100, 400)
            enemy = Enemy(y, side, sprite_manager, from_bottom=False)
        
        self.enemies.append(enemy)
        self.last_spawn_distance = current_distance

    def update(self, scroll_speed):
        """Aktualizuje przeciwników i pociski."""
        # Aktualizuj przeciwników
        for enemy in self.enemies:
            enemy.update(scroll_speed)
            
            # Sprawdź czy strzelił
            if enemy.can_shoot():
                x, y, direction = enemy.get_projectile_spawn_point()
                self.projectiles.append(Projectile(x, y, direction))
        
        # Aktualizuj pociski
        for projectile in self.projectiles:
            projectile.update()
        
        # Usuń obiekty poza ekranem
        self.enemies = [e for e in self.enemies if not e.is_off_screen()]
        self.projectiles = [p for p in self.projectiles if not p.is_off_screen()]

    def draw(self, screen):
        """Rysuje przeciwników i pociski."""
        for enemy in self.enemies:
            enemy.draw(screen)
        
        for projectile in self.projectiles:
            projectile.draw(screen)

    def check_projectile_collisions(self, player_hitbox):
        """Sprawdza czy jakiś pocisk trafił gracza."""
        for projectile in self.projectiles:
            if projectile.check_collision(player_hitbox):
                return True
        return False
