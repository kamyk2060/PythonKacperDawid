"""
HUGO - Główna Logika Gry
========================
To jest okno gry - tutaj wszystko się łączy.

Stany gry:
- 'menu' - ekran startowy
- 'playing' - gramy
- 'game_over' - koniec gry
"""
import pygame
import random
from .config import *
from .sprites import SpriteManager
from .player import Player
from .rope import Rope
from .collectibles import Coin, PowerUp
from .obstacles import ObstacleManager
from .enemy import EnemyManager
from .menu import Menu


class Game:
    """
    Główna klasa gry - zarządza wszystkim.
    """

    def __init__(self):
        """Inicjalizacja gry."""
        # -----------------------------------------
        # OKNO I ZEGAR
        # -----------------------------------------
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hugo - Wspinaczka po Linach")
        self.clock = pygame.time.Clock()
        
        # -----------------------------------------
        # CZCIONKI DO UI W GRZE
        # -----------------------------------------
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 26)
        
        # -----------------------------------------
        # ZAŁADUJ GRAFIKI
        # -----------------------------------------
        self.sprite_manager = SpriteManager()
        
        # -----------------------------------------
        # MENU
        # -----------------------------------------
        self.menu = Menu(self.screen, self.sprite_manager)
        
        # -----------------------------------------
        # STAN GRY
        # -----------------------------------------
        self.game_state = 'menu'  # 'menu', 'playing', 'game_over'
        
        # Zainicjuj grę
        self.reset_game()

    def reset_game(self):
        """Resetuje grę do stanu początkowego."""
        # -----------------------------------------
        # LINY
        # -----------------------------------------
        # Rozmieść 3 liny równomiernie
        rope_spacing = SCREEN_WIDTH // (NUM_ROPES + 1)
        
        self.ropes = []
        for i in range(NUM_ROPES):
            x = rope_spacing * (i + 1) - ROPE_WIDTH // 2
            rope = Rope(x, self.sprite_manager)
            self.ropes.append(rope)
        
        # -----------------------------------------
        # GRACZ
        # -----------------------------------------
        # Startuje na środkowej linie
        middle_rope = self.ropes[1]
        player_x = middle_rope.x + ROPE_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player = Player(player_x, PLAYER_START_Y, self.sprite_manager)
        
        # -----------------------------------------
        # PRZEDMIOTY
        # -----------------------------------------
        self.coins = []
        self.powerups = []
        
        # -----------------------------------------
        # PRZESZKODY I PRZECIWNICY
        # -----------------------------------------
        self.obstacle_manager = ObstacleManager()
        self.enemy_manager = EnemyManager()
        
        # -----------------------------------------
        # PUNKTACJA I STATYSTYKI
        # -----------------------------------------
        self.score = 0
        self.distance_pixels = 0  # Dystans w pikselach
        
        # -----------------------------------------
        # POWERUP PODWÓJNYCH PUNKTÓW
        # -----------------------------------------
        self.double_points_active = False
        self.double_points_timer = 0
        
        # -----------------------------------------
        # TRUDNOŚĆ
        # -----------------------------------------
        self.scroll_speed = SCROLL_SPEED
        
        # -----------------------------------------
        # SPAWNING (kiedy ostatnio co się pojawiło)
        # -----------------------------------------
        self.last_coin_distance = 0
        self.last_powerup_distance = 0
        
        # -----------------------------------------
        # TŁO (animacja scrollingu)
        # -----------------------------------------
        self.background_y = 0

    def spawn_objects(self):
        """Tworzy nowe obiekty (monety, przeszkody, etc.)."""
        # -----------------------------------------
        # MONETY
        # -----------------------------------------
        if self.distance_pixels - self.last_coin_distance > COIN_SPAWN_DISTANCE:
            # Nie za dużo monet na raz
            if len(self.coins) < MAX_COINS_ON_SCREEN:
                # Losowa lina
                rope_index = random.randint(0, NUM_ROPES - 1)
                
                # Utwórz monetę nad ekranem
                coin = Coin(rope_index, -COIN_SIZE, self.sprite_manager)
                self.coins.append(coin)
            
            self.last_coin_distance = self.distance_pixels
        
        # -----------------------------------------
        # POWERUPY
        # -----------------------------------------
        if self.distance_pixels - self.last_powerup_distance > POWERUP_SPAWN_DISTANCE:
            # Losowa szansa
            if random.random() < POWERUP_SPAWN_CHANCE:
                rope_index = random.randint(0, NUM_ROPES - 1)
                
                # Losowy typ
                powerup_type = random.choice(['invincible', 'double_points'])
                
                powerup = PowerUp(rope_index, -POWERUP_SIZE, powerup_type, self.sprite_manager)
                self.powerups.append(powerup)
            
            self.last_powerup_distance = self.distance_pixels
        
        # -----------------------------------------
        # PRZESZKODY
        # -----------------------------------------
        self.obstacle_manager.try_spawn(self.distance_pixels, self.sprite_manager)
        
        # -----------------------------------------
        # PRZECIWNICY
        # -----------------------------------------
        self.enemy_manager.try_spawn(self.distance_pixels, self.sprite_manager)

    def update(self):
        """Główna pętla logiki - wywoływana co klatkę."""
        # Tylko w stanie 'playing'
        if self.game_state != 'playing':
            return
        
        # -----------------------------------------
        # STEROWANIE GRACZA
        # -----------------------------------------
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, self.ropes)
        self.player.update()
        
        # -----------------------------------------
        # AKTUALIZUJ LINY
        # -----------------------------------------
        for rope in self.ropes:
            rope.update(self.scroll_speed)
        
        # -----------------------------------------
        # SCROLLUJ TŁO
        # -----------------------------------------
        self.background_y += self.scroll_speed * 0.5  # Tło wolniej (efekt głębi)
        if self.background_y >= BACKGROUND_HEIGHT:
            self.background_y = 0
        
        # -----------------------------------------
        # ZWIĘKSZ DYSTANS
        # -----------------------------------------
        self.distance_pixels += self.scroll_speed
        
        # -----------------------------------------
        # AKTUALIZUJ OBIEKTY
        # -----------------------------------------
        for coin in self.coins:
            coin.update(self.scroll_speed)
        
        for powerup in self.powerups:
            powerup.update(self.scroll_speed)
        
        self.obstacle_manager.update(self.scroll_speed)
        self.enemy_manager.update(self.scroll_speed)
        
        # -----------------------------------------
        # SPAWNUJ NOWE OBIEKTY
        # -----------------------------------------
        self.spawn_objects()
        
        # -----------------------------------------
        # USUŃ OBIEKTY POZA EKRANEM
        # -----------------------------------------
        self.coins = [c for c in self.coins if not c.is_off_screen()]
        self.powerups = [p for p in self.powerups if not p.is_off_screen()]
        
        # -----------------------------------------
        # KOLIZJE Z MONETAMI
        # -----------------------------------------
        for coin in self.coins:
            if coin.check_collision(self.player.hitbox, self.ropes):
                # Dodaj punkty
                points = POINTS_PER_COIN
                if self.double_points_active:
                    points *= 2
                self.score += points
        
        # -----------------------------------------
        # KOLIZJE Z POWERUPAMI
        # -----------------------------------------
        for powerup in self.powerups:
            if powerup.check_collision(self.player.hitbox, self.ropes):
                if powerup.type == 'invincible':
                    self.player.activate_invincibility()
                elif powerup.type == 'double_points':
                    self.double_points_active = True
                    self.double_points_timer = 300  # 5 sekund
        
        # -----------------------------------------
        # KOLIZJE Z PRZESZKODAMI
        # -----------------------------------------
        if not self.player.invincible:
            # Sprawdź nietoperze
            if self.obstacle_manager.check_collisions(self.player.hitbox, self.ropes):
                self.game_state = 'game_over'
                return
            
            # Sprawdź pociski
            if self.enemy_manager.check_projectile_collisions(self.player.hitbox):
                self.game_state = 'game_over'
                return
        
        # -----------------------------------------
        # TIMER PODWÓJNYCH PUNKTÓW
        # -----------------------------------------
        if self.double_points_active:
            self.double_points_timer -= 1
            if self.double_points_timer <= 0:
                self.double_points_active = False
        
        # -----------------------------------------
        # PUNKTY ZA DYSTANS
        # -----------------------------------------
        # Co 100 pikseli = 1 metr = 1 punkt
        meters = int(self.distance_pixels / PIXELS_PER_METER)
        distance_points = meters * POINTS_PER_METER
        
        # Score to punkty za monety + dystans
        # (ale punkty za dystans dodajemy na podstawie aktualnego dystansu)
        
        # -----------------------------------------
        # ZWIĘKSZANIE TRUDNOŚCI
        # -----------------------------------------
        if self.distance_pixels > DIFFICULTY_START_DISTANCE:
            # Ile razy przekroczyliśmy próg
            difficulty_level = (self.distance_pixels - DIFFICULTY_START_DISTANCE) // DIFFICULTY_INCREASE_INTERVAL
            
            # Nowa prędkość
            new_speed = SCROLL_SPEED + (difficulty_level * DIFFICULTY_SPEED_INCREASE)
            
            # Nie przekraczaj maksimum
            self.scroll_speed = min(new_speed, MAX_SCROLL_SPEED)

    def draw(self):
        """Rysuje odpowiedni ekran."""
        if self.game_state == 'menu':
            self.menu.draw_main_menu()
        
        elif self.game_state == 'playing':
            self.draw_game()
        
        elif self.game_state == 'game_over':
            self.draw_game()  # Rysuj grę w tle
            
            # Oblicz dystans i wynik końcowy
            distance_meters = int(self.distance_pixels / PIXELS_PER_METER)
            final_score = self.score + (distance_meters * POINTS_PER_METER)
            
            self.menu.draw_game_over(final_score, distance_meters)
        
        # Pokaż na ekranie
        pygame.display.flip()

    def draw_game(self):
        """Rysuje ekran gry."""
        # -----------------------------------------
        # TŁO
        # -----------------------------------------
        background = self.sprite_manager.get_sprite('background')
        self.screen.blit(background, (0, self.background_y))
        self.screen.blit(background, (0, self.background_y - BACKGROUND_HEIGHT))
        
        # -----------------------------------------
        # LINY
        # -----------------------------------------
        for rope in self.ropes:
            rope.draw(self.screen)
        
        # -----------------------------------------
        # MONETY
        # -----------------------------------------
        for coin in self.coins:
            coin.draw(self.screen, self.ropes)
        
        # -----------------------------------------
        # POWERUPY
        # -----------------------------------------
        for powerup in self.powerups:
            powerup.draw(self.screen, self.ropes)
        
        # -----------------------------------------
        # PRZESZKODY
        # -----------------------------------------
        self.obstacle_manager.draw(self.screen, self.ropes)
        
        # -----------------------------------------
        # PRZECIWNICY I POCISKI
        # -----------------------------------------
        self.enemy_manager.draw(self.screen)
        
        # -----------------------------------------
        # GRACZ
        # -----------------------------------------
        self.player.draw(self.screen)
        
        # -----------------------------------------
        # INTERFEJS (UI)
        # -----------------------------------------
        self.draw_ui()

    def draw_ui(self):
        """Rysuje interfejs użytkownika (punkty, dystans, powerupy)."""
        # Oblicz aktualne wartości
        distance_meters = int(self.distance_pixels / PIXELS_PER_METER)
        total_score = self.score + (distance_meters * POINTS_PER_METER)
        
        # -----------------------------------------
        # PUNKTY
        # -----------------------------------------
        score_text = self.font.render(f"Punkty: {total_score}", True, WHITE)
        
        # Tło dla tekstu (żeby było czytelne)
        bg_rect = pygame.Rect(5, 5, score_text.get_width() + 10, score_text.get_height() + 5)
        pygame.draw.rect(self.screen, BLACK, bg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        
        self.screen.blit(score_text, (10, 10))
        
        # -----------------------------------------
        # DYSTANS
        # -----------------------------------------
        dist_text = self.small_font.render(f"Dystans: {distance_meters} m", True, WHITE)
        
        bg_rect = pygame.Rect(5, 45, dist_text.get_width() + 10, dist_text.get_height() + 5)
        pygame.draw.rect(self.screen, BLACK, bg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        
        self.screen.blit(dist_text, (10, 48))
        
        # -----------------------------------------
        # AKTYWNE POWERUPY
        # -----------------------------------------
        y = 85
        
        # Nieśmiertelność
        if self.player.invincible:
            text = self.small_font.render("NIESMIERTELNOSC!", True, WHITE)
            
            bg_rect = pygame.Rect(5, y - 2, text.get_width() + 10, text.get_height() + 5)
            pygame.draw.rect(self.screen, PURPLE, bg_rect)
            pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
            
            self.screen.blit(text, (10, y))
            y += 30
        
        # Podwójne punkty
        if self.double_points_active:
            text = self.small_font.render("PODWOJNE PUNKTY!", True, WHITE)
            
            bg_rect = pygame.Rect(5, y - 2, text.get_width() + 10, text.get_height() + 5)
            pygame.draw.rect(self.screen, GREEN, bg_rect)
            pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
            
            self.screen.blit(text, (10, y))

    def handle_events(self):
        """
        Obsługuje eventy (klawiatura, zamknięcie okna).
        Zwraca False jeśli gra ma się zakończyć.
        """
        for event in pygame.event.get():
            # Zamknięcie okna
            if event.type == pygame.QUIT:
                return False
            
            # Naciśnięcie klawisza
            if event.type == pygame.KEYDOWN:
                
                # W MENU
                if self.game_state == 'menu':
                    if event.key == pygame.K_SPACE:
                        self.game_state = 'playing'
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Wyjście z gry
                
                # W GRZE
                elif self.game_state == 'playing':
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = 'menu'
                
                # GAME OVER
                elif self.game_state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.game_state = 'playing'
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = 'menu'
        
        return True

    def run(self):
        """Główna pętla gry - uruchamia wszystko."""
        running = True
        
        while running:
            # Obsłuż eventy
            running = self.handle_events()
            
            # Aktualizuj logikę
            self.update()
            
            # Narysuj wszystko
            self.draw()
            
            # Ogranicz do 60 FPS
            self.clock.tick(FPS)
