"""
HUGO - Główna Logika Gry
========================
Główna klasa Game zarządzająca całą grą.

Stany gry:
- 'menu' - ekran startowy
- 'playing' - aktywna rozgrywka
- 'game_over' - ekran końcowy
"""
import pygame
import random
from .config import *
from .player import Player
from .rope import Rope
from .collectibles import Coin, PowerUp
from .obstacles import ObstacleManager
from .enemy import Enemy, Projectile, EnemyManager
from .sprites import SpriteManager


class Game:
    """
    Główna klasa gry.
    Zarządza wszystkim - od menu po rozgrywkę.
    """

    def __init__(self):
        """Inicjalizacja gry."""
        # Okno i zegar
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hugo - Wspinaczka po Linach")
        self.clock = pygame.time.Clock()

        # Czcionki
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)

        # Sprite manager
        self.sprite_manager = SpriteManager()

        # Stan gry
        self.game_state = 'menu'

        # Inicjalizacja obiektów
        self.reset_game()

    def reset_game(self):
        """Resetuje grę do stanu początkowego."""
        # Liny (3 sztuki równomiernie rozmieszczone)
        rope_spacing = SCREEN_WIDTH // (NUM_ROPES + 1)
        self.ropes = [
            Rope(rope_spacing * (i + 1) - ROPE_WIDTH // 2, self.sprite_manager)
            for i in range(NUM_ROPES)
        ]

        # Gracz (na środkowej linie)
        middle_rope = self.ropes[1]
        start_x = middle_rope.x + ROPE_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player = Player(start_x, PLAYER_Y_POSITION, self.sprite_manager)

        # Listy obiektów
        self.coins = []
        self.powerups = []

        # Managery
        self.obstacle_manager = ObstacleManager()
        self.enemy_manager = EnemyManager()

        # Stan gry
        self.score = 0
        self.distance = 0
        self.scroll_speed = SCROLL_SPEED

        # Powerup podwójnych punktów
        self.double_points = False
        self.double_points_timer = 0

        # Liczniki spawnu
        self.last_coin_distance = 0
        self.last_powerup_distance = 0
        self.last_enemy_distance = 0

        # Tło
        self.background_y = 0
        self.background_scroll_speed = 1

    def spawn_objects(self):
        """Spawnuje nowe obiekty (monety, przeszkody, powerupy, przeciwników)."""
        # MONETY - co 100 pikseli dystansu
        if self.distance - self.last_coin_distance > 100:
            if len(self.coins) < 5:
                rope_index = random.randint(0, NUM_ROPES - 1)
                self.coins.append(Coin(rope_index, -COIN_SIZE, self.sprite_manager))
            self.last_coin_distance = self.distance

        # PRZESZKODY - system patternów
        self.obstacle_manager.spawn_pattern_if_ready(self.distance, self.sprite_manager)

        # POWERUPY - co 400 pikseli, 40% szansy
        if self.distance - self.last_powerup_distance > 400:
            if random.random() < 0.4:
                rope_index = random.randint(0, NUM_ROPES - 1)
                pu_type = random.choice(['invincible', 'double_points'])
                self.powerups.append(
                    PowerUp(rope_index, -POWERUP_SIZE, pu_type, self.sprite_manager)
                )
            self.last_powerup_distance = self.distance

        # PRZECIWNICY - co 350 pikseli
        if self.distance - self.last_enemy_distance > ENEMY_SPAWN_DISTANCE:
            if self.enemy_manager.can_spawn_enemy():
                from_bottom = random.random() < ENEMY_SPAWN_FROM_BOTTOM_CHANCE

                if from_bottom:
                    self.enemy_manager.add_enemy(
                        Enemy(SCREEN_HEIGHT + ENEMY_HEIGHT, None, 
                              self.sprite_manager, from_bottom=True)
                    )
                else:
                    side = random.choice(['left', 'right'])
                    y = random.randint(100, 400)
                    self.enemy_manager.add_enemy(
                        Enemy(y, side, self.sprite_manager)
                    )
            self.last_enemy_distance = self.distance

    def update(self):
        """Główna pętla logiki - wywoływana co klatkę."""
        if self.game_state != 'playing':
            return

        # Sterowanie gracza
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.ropes)
        self.player.update()

        # Update lin
        for rope in self.ropes:
            rope.update(self.scroll_speed, SCREEN_HEIGHT)

        # Scrolling tła
        self.background_y += self.background_scroll_speed
        if self.background_y >= BACKGROUND_HEIGHT:
            self.background_y = 0

        # Dystans
        self.distance += self.scroll_speed

        # Update obiektów
        for coin in self.coins:
            coin.update(self.scroll_speed)
        for powerup in self.powerups:
            powerup.update(self.scroll_speed)
        self.obstacle_manager.update_all(self.scroll_speed)
        self.enemy_manager.update_all(self.scroll_speed)

        # Strzały przeciwników
        for enemy in self.enemy_manager.enemies:
            if enemy.can_shoot():
                if hasattr(enemy, 'actual_side'):
                    direction = 1 if enemy.actual_side == 'left' else -1
                    proj_x = enemy.x + (ENEMY_WIDTH if enemy.actual_side == 'left' else 0)
                else:
                    direction = 1 if enemy.side == 'left' else -1
                    proj_x = enemy.x + (ENEMY_WIDTH if enemy.side == 'left' else 0)
                proj_y = enemy.y + ENEMY_HEIGHT // 2
                self.enemy_manager.projectiles.append(Projectile(proj_x, proj_y, direction))

        # Spawning
        self.spawn_objects()

        # Czyszczenie obiektów poza ekranem
        self.coins = [c for c in self.coins if not c.is_off_screen()]
        self.powerups = [p for p in self.powerups if not p.is_off_screen()]

        # Kolizje z monetami
        for coin in self.coins[:]:
            if coin.check_collision(self.player.hitbox, self.ropes):
                points = COIN_POINTS * 2 if self.double_points else COIN_POINTS
                self.score += points
                self.coins.remove(coin)

        # Kolizje z przeszkodami (jeśli nie nieśmiertelny)
        if not self.player.invincible:
            if self.obstacle_manager.check_collisions(self.player.hitbox, self.ropes):
                self.game_state = 'game_over'
                return
            if self.enemy_manager.check_projectile_collisions(self.player.hitbox):
                self.game_state = 'game_over'
                return

        # Kolizje z powerupami
        for powerup in self.powerups[:]:
            if powerup.check_collision(self.player.hitbox, self.ropes):
                if powerup.type == 'invincible':
                    self.player.activate_invincibility()
                elif powerup.type == 'double_points':
                    self.double_points = True
                    self.double_points_timer = 300
                self.powerups.remove(powerup)

        # Timer podwójnych punktów
        if self.double_points:
            self.double_points_timer -= 1
            if self.double_points_timer <= 0:
                self.double_points = False

        # Punkty za dystans
        self.score += DISTANCE_POINTS_MULTIPLIER * self.scroll_speed

        # Zwiększanie trudności
        if self.distance > 1000:
            self.scroll_speed = min(
                SCROLL_SPEED + (self.distance // 2000) * 0.3,
                6
            )
            self.background_scroll_speed = self.scroll_speed * 0.8

    def draw(self):
        """Rysuje odpowiedni ekran w zależności od stanu gry."""
        if self.game_state == 'menu':
            self.draw_menu()
        elif self.game_state == 'playing':
            self.draw_game()
        elif self.game_state == 'game_over':
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        """
        Rysuje PROSTE menu główne.
        Bez efektów specjalnych, gradientów czy animacji.
        """
        # Tło
        bg_sprite = self.sprite_manager.get_sprite('background')
        if bg_sprite:
            self.screen.blit(bg_sprite, (0, 0))
        else:
            self.screen.fill(SKY_BLUE)

        # Przyciemnienie tła
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Panel główny (prosty prostokąt)
        panel_w, panel_h = 700, 600
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_h // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, DARK_GRAY, panel_rect)
        pygame.draw.rect(self.screen, YELLOW, panel_rect, 4)

        # Tytuł
        title = self.title_font.render("HUGO", True, YELLOW)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, panel_y + 30))

        # Podtytuł
        subtitle = self.font.render("Wspinaczka po Linach", True, WHITE)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        self.screen.blit(subtitle, (subtitle_x, panel_y + 100))

        # Linia oddzielająca
        pygame.draw.line(self.screen, YELLOW, 
                        (panel_x + 50, panel_y + 150),
                        (panel_x + panel_w - 50, panel_y + 150), 2)

        # Sterowanie
        y = panel_y + 180
        
        header = self.font.render("STEROWANIE", True, YELLOW)
        self.screen.blit(header, (panel_x + 50, y))
        y += 40

        controls = [
            "Strzalki / WASD - Ruch",
            "Lewo/Prawo - Zmiana liny",
            "Gora/Dol - Ruch pionowy",
        ]
        for text in controls:
            rendered = self.small_font.render(text, True, WHITE)
            self.screen.blit(rendered, (panel_x + 70, y))
            y += 30

        # Cel gry
        y += 20
        header = self.font.render("CEL GRY", True, YELLOW)
        self.screen.blit(header, (panel_x + 50, y))
        y += 40

        goals = [
            "Wspinaj sie jak najwyzej",
            "Zbieraj monety",
            "Unikaj przeszkod i pociskow",
        ]
        for text in goals:
            rendered = self.small_font.render(text, True, WHITE)
            self.screen.blit(rendered, (panel_x + 70, y))
            y += 30

        # Powerupy
        y += 20
        header = self.font.render("POWERUPY", True, YELLOW)
        self.screen.blit(header, (panel_x + 50, y))
        y += 40

        # Fioletowy - nieśmiertelność
        pygame.draw.rect(self.screen, PURPLE, (panel_x + 70, y, 30, 30))
        pygame.draw.rect(self.screen, WHITE, (panel_x + 70, y, 30, 30), 2)
        text = self.small_font.render("- Niesmiertelnosc (3s)", True, WHITE)
        self.screen.blit(text, (panel_x + 110, y + 5))
        y += 40

        # Zielony - podwójne punkty
        pygame.draw.rect(self.screen, GREEN, (panel_x + 70, y, 30, 30))
        pygame.draw.rect(self.screen, WHITE, (panel_x + 70, y, 30, 30), 2)
        text = self.small_font.render("- Podwojne punkty (5s)", True, WHITE)
        self.screen.blit(text, (panel_x + 110, y + 5))

        # Przycisk START (prosty, bez animacji)
        start_text = self.font.render("Nacisnij SPACJE aby zaczac", True, BLACK)
        btn_w = start_text.get_width() + 40
        btn_h = start_text.get_height() + 20
        btn_x = SCREEN_WIDTH // 2 - btn_w // 2
        btn_y = panel_y + panel_h - 70

        pygame.draw.rect(self.screen, YELLOW, (btn_x, btn_y, btn_w, btn_h))
        pygame.draw.rect(self.screen, WHITE, (btn_x, btn_y, btn_w, btn_h), 3)
        self.screen.blit(start_text, (btn_x + 20, btn_y + 10))

        # ESC info
        esc_text = self.small_font.render("ESC - Wyjscie z gry", True, (150, 150, 150))
        esc_x = SCREEN_WIDTH // 2 - esc_text.get_width() // 2
        self.screen.blit(esc_text, (esc_x, panel_y + panel_h - 25))

    def draw_game(self):
        """Rysuje ekran gry."""
        # Tło
        bg_sprite = self.sprite_manager.get_sprite('background')
        if bg_sprite:
            self.screen.blit(bg_sprite, (0, self.background_y))
            self.screen.blit(bg_sprite, (0, self.background_y - BACKGROUND_HEIGHT))
        else:
            self.screen.fill(SKY_BLUE)

        # Liny
        for rope in self.ropes:
            rope.draw(self.screen)

        # Monety
        for coin in self.coins:
            coin.draw(self.screen, self.ropes)

        # Powerupy
        for powerup in self.powerups:
            powerup.draw(self.screen, self.ropes)

        # Przeszkody
        self.obstacle_manager.draw_all(self.screen, self.ropes)

        # Przeciwnicy i pociski
        self.enemy_manager.draw_all(self.screen)

        # Gracz
        self.player.draw(self.screen)

        # UI
        self._draw_ui()

    def _draw_ui(self):
        """Rysuje interfejs użytkownika (punkty, dystans, powerupy)."""
        # Punkty
        score_text = self.font.render(f"Punkty: {int(self.score)}", True, WHITE)
        score_bg = pygame.Rect(5, 5, score_text.get_width() + 10, score_text.get_height() + 5)
        pygame.draw.rect(self.screen, BLACK, score_bg)
        pygame.draw.rect(self.screen, WHITE, score_bg, 2)
        self.screen.blit(score_text, (10, 10))

        # Dystans
        dist_text = self.small_font.render(f"Dystans: {int(self.distance * 0.0075)}m", True, WHITE)
        dist_bg = pygame.Rect(5, 48, dist_text.get_width() + 10, dist_text.get_height() + 5)
        pygame.draw.rect(self.screen, BLACK, dist_bg)
        pygame.draw.rect(self.screen, WHITE, dist_bg, 2)
        self.screen.blit(dist_text, (10, 50))

        # Aktywne powerupy
        y = 85
        if self.player.invincible:
            inv_text = self.small_font.render("NIESMIERTELNOSC!", True, WHITE)
            inv_bg = pygame.Rect(5, y - 2, inv_text.get_width() + 10, inv_text.get_height() + 5)
            pygame.draw.rect(self.screen, PURPLE, inv_bg)
            pygame.draw.rect(self.screen, WHITE, inv_bg, 2)
            self.screen.blit(inv_text, (10, y))
            y += 30

        if self.double_points:
            dp_text = self.small_font.render("PODWOJNE PUNKTY!", True, WHITE)
            dp_bg = pygame.Rect(5, y - 2, dp_text.get_width() + 10, dp_text.get_height() + 5)
            pygame.draw.rect(self.screen, GREEN, dp_bg)
            pygame.draw.rect(self.screen, WHITE, dp_bg, 2)
            self.screen.blit(dp_text, (10, y))

    def draw_game_over(self):
        """Rysuje ekran Game Over."""
        # Narysuj grę w tle (zamrożoną)
        self.draw_game()

        # Przyciemnienie
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Teksty
        texts = [
            ("GAME OVER", RED, self.title_font, -100),
            (f"Wynik: {int(self.score)}", WHITE, self.font, -20),
            (f"Dystans: {int(self.distance * 0.0075)}m", WHITE, self.small_font, 20),
            ("SPACJA - Graj ponownie", YELLOW, self.font, 80),
            ("ESC - Menu glowne", YELLOW, self.small_font, 120),
        ]

        for text, color, font, y_offset in texts:
            rendered = font.render(text, True, color)
            x = SCREEN_WIDTH // 2 - rendered.get_width() // 2
            y = SCREEN_HEIGHT // 2 + y_offset
            self.screen.blit(rendered, (x, y))

    def handle_events(self):
        """Obsługuje eventy (klawiatura, zamknięcie okna)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.game_state == 'menu':
                    if event.key == pygame.K_SPACE:
                        self.game_state = 'playing'
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False

                elif self.game_state == 'playing':
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = 'menu'

                elif self.game_state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.game_state = 'playing'
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = 'menu'

        return True

    def run(self):
        """Główna pętla gry."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
