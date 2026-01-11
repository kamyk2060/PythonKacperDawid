"""
HUGO - Klasa Gracza
===================
Obsługuje postać Hugo - ruch, animacje, kolizje, powerupy.
"""
import pygame
from .config import *


class Player:
    """
    Gracz - Hugo wspinający się po linach.
    
    Główne funkcje:
    - Ruch pionowy (góra/dół)
    - Zmiana liny (lewo/prawo) z płynną animacją
    - Nieśmiertelność (powerup)
    """

    def __init__(self, x, y, sprite_manager):
        """
        Tworzy gracza na podanej pozycji.
        
        Parametry:
            x, y - pozycja startowa
            sprite_manager - manager do pobierania sprite'ów
        """
        # Prostokąt do rysowania (pełny rozmiar sprite'a)
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Hitbox do kolizji (mniejszy niż sprite - bardziej fair)
        hitbox_w = int(PLAYER_WIDTH * PLAYER_HITBOX_SCALE)
        hitbox_h = int(PLAYER_HEIGHT * PLAYER_HITBOX_SCALE)
        offset_x = (PLAYER_WIDTH - hitbox_w) // 2
        offset_y = (PLAYER_HEIGHT - hitbox_h) // 2
        self.hitbox = pygame.Rect(x + offset_x, y + offset_y, hitbox_w, hitbox_h)
        
        # Na której linie jest gracz (0, 1, 2)
        self.current_rope = 1  # Start na środkowej
        
        # Powerup nieśmiertelności
        self.invincible = False
        self.invincible_timer = 0
        
        # System ruchu między linami
        self.move_cooldown = 0     # Cooldown przed kolejnym skokiem
        self.is_moving = False     # Czy w trakcie ruchu
        self.target_x = x          # Docelowa pozycja X
        
        # System animacji skoku
        self.is_jumping = False
        self.jump_direction = None  # 'left' lub 'right'
        self.jump_progress = 0      # 0-20
        
        # Animacja
        self.sprite_manager = sprite_manager
        self.anim_frame = 0

    def move(self, keys, ropes):
        """
        Obsługuje sterowanie gracza.
        
        Parametry:
            keys - stan klawiszy (pygame.key.get_pressed())
            ropes - lista lin
        """
        # =============================================
        # RUCH PIONOWY (góra/dół)
        # =============================================
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= PLAYER_VERTICAL_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_VERTICAL_SPEED
        
        # Ogranicz do granic ekranu
        self.rect.y = max(PLAYER_MIN_Y, min(self.rect.y, PLAYER_MAX_Y))

        # =============================================
        # COOLDOWN
        # =============================================
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        # =============================================
        # RUCH POZIOMY (zmiana liny)
        # =============================================
        if not self.is_moving and self.move_cooldown == 0:
            # Skok w lewo
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.current_rope > 0:
                self.current_rope -= 1
                self._start_jump('left', ropes)
            
            # Skok w prawo
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.current_rope < NUM_ROPES - 1:
                self.current_rope += 1
                self._start_jump('right', ropes)

        # =============================================
        # PŁYNNY RUCH DO CELU
        # =============================================
        if self.is_moving:
            distance = abs(self.rect.x - self.target_x)
            if distance > 2:
                step = min(7, distance)
                if self.rect.x < self.target_x:
                    self.rect.x += step
                else:
                    self.rect.x -= step
            else:
                self.rect.x = self.target_x
                self.is_moving = False

        # =============================================
        # POSTĘP ANIMACJI SKOKU
        # =============================================
        if self.is_jumping:
            self.jump_progress += 1
            if self.jump_progress > 20:
                self.is_jumping = False
                self.jump_progress = 0

        # =============================================
        # AKTUALIZACJA HITBOXA
        # =============================================
        hitbox_w = int(PLAYER_WIDTH * PLAYER_HITBOX_SCALE)
        hitbox_h = int(PLAYER_HEIGHT * PLAYER_HITBOX_SCALE)
        offset_x = (PLAYER_WIDTH - hitbox_w) // 2
        offset_y = (PLAYER_HEIGHT - hitbox_h) // 2
        self.hitbox.x = self.rect.x + offset_x
        self.hitbox.y = self.rect.y + offset_y

    def _start_jump(self, direction, ropes):
        """Rozpoczyna skok na inną linę."""
        self.move_cooldown = 30  # Cooldown 0.5 sekundy
        self.is_moving = True
        self.is_jumping = True
        self.jump_direction = direction
        self.jump_progress = 0
        
        # Oblicz pozycję docelową (środek nowej liny)
        target_rope = ropes[self.current_rope]
        self.target_x = target_rope.x + ROPE_WIDTH // 2 - PLAYER_WIDTH // 2

    def update(self):
        """Aktualizuje timery i animacje."""
        # Licznik animacji
        self.anim_frame = (self.anim_frame + 1) % 1000
        
        # Timer nieśmiertelności
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def activate_invincibility(self):
        """Włącza nieśmiertelność na 3 sekundy."""
        self.invincible = True
        self.invincible_timer = 180  # 3 sekundy przy 60 FPS

    def draw(self, screen):
        """Rysuje gracza na ekranie."""
        # Pobierz odpowiedni sprite
        sprite = self.sprite_manager.get_player_frame(
            self.anim_frame,
            self.is_jumping,
            self.jump_direction,
            self.jump_progress
        )

        # Efekt migania podczas nieśmiertelności
        if self.invincible and self.invincible_timer % 10 < 5:
            return  # Nie rysuj (miga)

        if sprite:
            screen.blit(sprite, self.rect)
        else:
            # Fallback - prostokąt
            color = YELLOW if self.invincible else RED
            pygame.draw.rect(screen, color, self.rect)
