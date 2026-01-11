"""
HUGO - System Przeszkód (Nietoperze)
====================================
Nietoperze pojawiają się według wzorców (patterns) żeby gra była fair.
Zawsze jest przynajmniej jedna wolna lina do ucieczki!
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
        Tworzy nietoperza na podanej linie.
        
        Parametry:
            rope_index - numer liny (0, 1, 2)
            y - pozycja Y
            bat_type - 'bat_1' lub 'bat_2' (różne kolory)
            sprite_manager - manager sprite'ów
        """
        self.rope_index = rope_index
        self.y = y
        self.type = bat_type
        self.sprite_manager = sprite_manager
        
        # Losowy start animacji (żeby nietoperze nie były zsynchronizowane)
        self.anim_counter = random.randint(0, 30)

    def get_rect(self, ropes):
        """Zwraca prostokąt sprite'a (do rysowania)."""
        x = ropes[self.rope_index].x + ROPE_WIDTH // 2 - OBSTACLE_SIZE // 2
        return pygame.Rect(x, self.y, OBSTACLE_SIZE, OBSTACLE_SIZE)

    def get_hitbox(self, ropes):
        """Zwraca hitbox (mniejszy niż sprite - fair gameplay)."""
        sprite_rect = self.get_rect(ropes)
        hitbox_size = int(OBSTACLE_SIZE * OBSTACLE_HITBOX_SCALE)
        offset = (OBSTACLE_SIZE - hitbox_size) // 2
        return pygame.Rect(
            sprite_rect.x + offset,
            sprite_rect.y + offset,
            hitbox_size,
            hitbox_size
        )

    def update(self, scroll_speed):
        """Aktualizuje pozycję i animację."""
        self.y += scroll_speed
        self.anim_counter += 1

    def draw(self, screen, ropes):
        """Rysuje nietoperza na ekranie."""
        sprite_rect = self.get_rect(ropes)
        bat_sprite = self.sprite_manager.get_bat_frame(self.anim_counter, self.type)

        if bat_sprite:
            screen.blit(bat_sprite, sprite_rect)
        else:
            # Fallback - kolorowe kółko
            color = RED if self.type == 'bat_1' else PURPLE
            pygame.draw.circle(screen, color, sprite_rect.center, OBSTACLE_SIZE // 2)

    def is_off_screen(self):
        """Sprawdza czy wyszedł poza ekran."""
        return self.y > SCREEN_HEIGHT

    def check_collision(self, player_hitbox, ropes):
        """Sprawdza kolizję z graczem."""
        return self.get_hitbox(ropes).colliderect(player_hitbox)


class Pattern:
    """
    Wzór rozmieszczenia nietoperzy.
    Definiuje które liny są zajęte, a które wolne.
    """

    def __init__(self, occupied_lanes, free_lanes, name):
        self.occupied_lanes = occupied_lanes
        self.free_lanes = free_lanes
        self.name = name
        self.difficulty = len(occupied_lanes)

    def spawn_obstacles(self, base_y, sprite_manager):
        """Tworzy nietoperze dla tego wzorca."""
        obstacles = []
        for lane in self.occupied_lanes:
            bat_type = random.choice(['bat_1', 'bat_2'])
            y_offset = random.randint(-PATTERN_VERTICAL_VARIATION, 
                                     PATTERN_VERTICAL_VARIATION)
            obstacles.append(Obstacle(lane, base_y + y_offset, bat_type, sprite_manager))
        return obstacles


class PatternManager:
    """
    Zarządza wyborem wzorców.
    Unika powtórzeń i zapewnia że gra jest możliwa do przejścia.
    """

    def __init__(self):
        # Stwórz obiekty Pattern z konfiguracji
        self.patterns = [Pattern(o, f, n) for o, f, n in PATTERNS]
        
        self.last_pattern_distance = 0
        self.next_pattern_distance = PATTERN_SPAWN_DISTANCE
        self.pattern_history = []

    def get_available_patterns(self):
        """Zwraca listę wzorców dostępnych do wyboru (unikając powtórzeń)."""
        available = self.patterns.copy()

        if self.pattern_history:
            last = self.pattern_history[-1]
            
            # Unikaj blokowania tej samej liny 2x pod rząd
            if last.difficulty == 1:
                last_lane = last.occupied_lanes[0]
                available = [p for p in available if last_lane not in p.occupied_lanes]

            # Unikaj tego samego wzorca 3x pod rząd
            if len(self.pattern_history) >= 2:
                if self.pattern_history[-2].name == last.name:
                    available = [p for p in available if p.name != last.name]

        return available or self.patterns

    def can_spawn_pattern(self, current_distance):
        """Sprawdza czy czas na nowy wzorzec."""
        return current_distance - self.last_pattern_distance >= self.next_pattern_distance

    def spawn_next_pattern(self, base_y, sprite_manager, current_distance):
        """Spawnuje następny wzorzec."""
        # Losuj odstęp do następnego
        self.next_pattern_distance = random.randint(MIN_PATTERN_DISTANCE, MAX_PATTERN_DISTANCE)
        
        # Wybierz wzorzec
        available = self.get_available_patterns()
        chosen = random.choice(available)
        
        # Stwórz nietoperze
        obstacles = chosen.spawn_obstacles(base_y, sprite_manager)
        
        # Zapisz w historii
        self.pattern_history.append(chosen)
        if len(self.pattern_history) > 3:
            self.pattern_history.pop(0)
        
        self.last_pattern_distance = current_distance
        return obstacles, chosen


class ObstacleManager:
    """
    Główny manager przeszkód.
    Używany przez game.py do zarządzania wszystkimi nietoperzami.
    """

    def __init__(self):
        self.obstacles = []
        self.pattern_manager = PatternManager()

    def spawn_pattern_if_ready(self, current_distance, sprite_manager):
        """Spawnuje wzorzec jeśli nadszedł czas."""
        spawn_y = -OBSTACLE_SIZE - 50

        if self.pattern_manager.can_spawn_pattern(current_distance):
            new_obstacles, pattern = self.pattern_manager.spawn_next_pattern(
                spawn_y, sprite_manager, current_distance
            )
            self.obstacles.extend(new_obstacles)
            return new_obstacles, pattern
        return [], None

    def update_all(self, scroll_speed):
        """Aktualizuje wszystkie nietoperze."""
        for obs in self.obstacles:
            obs.update(scroll_speed)
        # Usuń te poza ekranem
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

    def draw_all(self, screen, ropes):
        """Rysuje wszystkie nietoperze."""
        for obs in self.obstacles:
            obs.draw(screen, ropes)

    def check_collisions(self, player_hitbox, ropes):
        """Sprawdza kolizje z graczem. Zwraca True jeśli trafiony."""
        for obs in self.obstacles:
            if obs.check_collision(player_hitbox, ropes):
                return True
        return False
