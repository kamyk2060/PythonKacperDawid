"""
HUGO - System Przeszkód (Nietoperze)
====================================
Nietoperze pojawiają się według WZORCÓW (patterns).
Dzięki temu zawsze jest przynajmniej jedna wolna lina do ucieczki!
"""
import pygame
import random
from .config import *


class Obstacle:
    """
    Pojedynczy nietoperz.
    """

    def __init__(self, rope_index, y, bat_type, sprite_manager):
        """
        Tworzy nietoperza.
        
        Parametry:
            rope_index - na której linie (0, 1, 2)
            y - pozycja Y
            bat_type - 'bat_1' lub 'bat_2' (różne kolory)
            sprite_manager - do pobierania grafiki
        """
        self.rope_index = rope_index
        self.y = y
        self.bat_type = bat_type
        self.sprite_manager = sprite_manager
        
        # Losowy start animacji (żeby nietoperze nie machały synchronicznie)
        self.animation_counter = random.randint(0, 30)

    def get_rect(self, ropes):
        """Zwraca prostokąt do RYSOWANIA (pełny rozmiar)."""
        x = ropes[self.rope_index].x + ROPE_WIDTH // 2 - OBSTACLE_SIZE // 2
        return pygame.Rect(x, self.y, OBSTACLE_SIZE, OBSTACLE_SIZE)

    def get_hitbox(self, ropes):
        """Zwraca prostokąt do KOLIZJI (mniejszy - fair gameplay)."""
        sprite_rect = self.get_rect(ropes)
        
        # Hitbox jest mniejszy niż sprite
        hitbox_size = int(OBSTACLE_SIZE * OBSTACLE_HITBOX_SCALE)
        offset = (OBSTACLE_SIZE - hitbox_size) // 2
        
        return pygame.Rect(
            sprite_rect.x + offset,
            sprite_rect.y + offset,
            hitbox_size,
            hitbox_size
        )

    def update(self, scroll_speed):
        """Aktualizuje nietoperza (ruch + animacja)."""
        self.y += scroll_speed
        self.animation_counter += 1

    def draw(self, screen, ropes):
        """Rysuje nietoperza."""
        rect = self.get_rect(ropes)
        sprite = self.sprite_manager.get_bat_frame(self.animation_counter, self.bat_type)
        screen.blit(sprite, rect)

    def is_off_screen(self):
        """Sprawdza czy wyleciał poza ekran."""
        return self.y > SCREEN_HEIGHT

    def check_collision(self, player_hitbox, ropes):
        """Sprawdza kolizję z graczem."""
        my_hitbox = self.get_hitbox(ropes)
        return my_hitbox.colliderect(player_hitbox)


class ObstacleManager:
    """
    Zarządza wszystkimi przeszkodami.
    
    Używa systemu WZORCÓW - nietoperze pojawiają się w określonych
    konfiguracjach, żeby zawsze była droga ucieczki.
    """

    def __init__(self):
        # Lista aktywnych przeszkód
        self.obstacles = []
        
        # Kiedy ostatnio pojawiła się przeszkoda
        self.last_spawn_distance = 0
        
        # Jaki będzie następny odstęp
        self.next_spawn_distance = MIN_OBSTACLE_DISTANCE
        
        # Historia wzorców (żeby nie powtarzać)
        self.pattern_history = []

    def try_spawn(self, current_distance, sprite_manager):
        """
        Próbuje utworzyć nową grupę przeszkód.
        
        Parametry:
            current_distance - aktualny przebyty dystans
            sprite_manager - do tworzenia przeszkód
        """
        # Sprawdź czy czas na nowe przeszkody
        distance_since_last = current_distance - self.last_spawn_distance
        
        if distance_since_last < self.next_spawn_distance:
            return  # Za wcześnie
        
        # -----------------------------------------
        # WYBIERZ WZORZEC
        # -----------------------------------------
        # Unikamy powtórzenia ostatniego wzorca
        available_patterns = OBSTACLE_PATTERNS.copy()
        
        if self.pattern_history:
            last_pattern = self.pattern_history[-1]
            # Usuń ostatni wzorzec z dostępnych
            available_patterns = [p for p in available_patterns if p[2] != last_pattern]
        
        # Wybierz losowy wzorzec
        if available_patterns:
            pattern = random.choice(available_patterns)
        else:
            pattern = random.choice(OBSTACLE_PATTERNS)
        
        # Zapisz w historii
        self.pattern_history.append(pattern[2])  # Zapisz nazwę
        if len(self.pattern_history) > 3:
            self.pattern_history.pop(0)  # Usuń najstarszy
        
        # -----------------------------------------
        # UTWÓRZ NIETOPERZE
        # -----------------------------------------
        occupied_lanes = pattern[0]  # Które liny są zajęte
        
        for lane in occupied_lanes:
            # Losowy typ nietoperza
            bat_type = random.choice(['bat_1', 'bat_2'])
            
            # Losowe przesunięcie Y (żeby nie były idealnie w linii)
            y_offset = random.randint(-OBSTACLE_Y_VARIATION, OBSTACLE_Y_VARIATION)
            
            # Pozycja startowa - nad ekranem
            spawn_y = -OBSTACLE_SIZE - 50 + y_offset
            
            # Utwórz nietoperza
            obstacle = Obstacle(lane, spawn_y, bat_type, sprite_manager)
            self.obstacles.append(obstacle)
        
        # -----------------------------------------
        # USTAW NASTĘPNY SPAWN
        # -----------------------------------------
        self.last_spawn_distance = current_distance
        self.next_spawn_distance = random.randint(MIN_OBSTACLE_DISTANCE, MAX_OBSTACLE_DISTANCE)

    def update(self, scroll_speed):
        """Aktualizuje wszystkie przeszkody."""
        # Aktualizuj każdą przeszkodę
        for obstacle in self.obstacles:
            obstacle.update(scroll_speed)
        
        # Usuń te które wyleciały poza ekran
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

    def draw(self, screen, ropes):
        """Rysuje wszystkie przeszkody."""
        for obstacle in self.obstacles:
            obstacle.draw(screen, ropes)

    def check_collisions(self, player_hitbox, ropes):
        """
        Sprawdza czy gracz zderzył się z jakąkolwiek przeszkodą.
        Zwraca True jeśli tak (game over!).
        """
        for obstacle in self.obstacles:
            if obstacle.check_collision(player_hitbox, ropes):
                return True
        return False
