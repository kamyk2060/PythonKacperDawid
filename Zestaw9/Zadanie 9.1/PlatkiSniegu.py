import pygame
import random
import sys

# Inicjalizacja Pygame
pygame.init()

# Stałe
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
RED = (255, 50, 50)

# Ustawienia gry
SNOWFLAKE_SIZE = 20
SNOWFLAKE_SPEED = 2
SPAWN_RATE = 30  # Co ile klatek pojawia się nowy płatek


class Snowflake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = SNOWFLAKE_SIZE
        self.speed = SNOWFLAKE_SPEED + random.uniform(-0.5, 0.5)
        self.radius = self.size // 2

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        # Rysowanie płatka śniegu (gwiazdka)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def is_clicked(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return dx * dx + dy * dy <= self.radius * self.radius

    def reached_bottom(self):
        return self.y - self.radius >= HEIGHT


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Padający Śnieg - Kliknij, aby stopić płatki!")
        self.clock = pygame.time.Clock()
        self.snowflakes = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def spawn_snowflake(self):
        x = random.randint(SNOWFLAKE_SIZE, WIDTH - SNOWFLAKE_SIZE)
        self.snowflakes.append(Snowflake(x, -SNOWFLAKE_SIZE))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                pos = pygame.mouse.get_pos()
                # Sprawdzenie kliknięcia na płatek
                for snowflake in self.snowflakes[:]:
                    if snowflake.is_clicked(pos):
                        self.snowflakes.remove(snowflake)
                        self.score += 1
                        break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()  # Restart gry
                if event.key == pygame.K_ESCAPE:
                    return False

        return True

    def update(self):
        if self.game_over:
            return

        self.frame_count += 1

        # Tworzenie nowych płatków
        if self.frame_count % SPAWN_RATE == 0:
            self.spawn_snowflake()

        # Aktualizacja płatków
        for snowflake in self.snowflakes[:]:
            snowflake.update()

            # Sprawdzenie czy płatek dotarł na dół
            if snowflake.reached_bottom():
                self.game_over = True

    def draw(self):
        # Tło
        self.screen.fill(BLUE)

        # Płatki śniegu
        for snowflake in self.snowflakes:
            snowflake.draw(self.screen)

        # Wynik
        score_text = self.font.render(f"Stopione płatki: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        # Instrukcje
        instruction_text = self.small_font.render("Klikaj na płatki, aby je stopić!", True, BLACK)
        self.screen.blit(instruction_text, (10, HEIGHT - 30))

        # Game Over
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("PRZEGRAŁEŚ!", True, RED)
            final_score_text = self.font.render(f"Stopiłeś {self.score} płatków", True, WHITE)
            restart_text = self.small_font.render("Naciśnij R, aby zagrać ponownie", True, WHITE)
            exit_text = self.small_font.render("Naciśnij ESC, aby wyjść", True, WHITE)

            self.screen.blit(game_over_text,
                             (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
            self.screen.blit(final_score_text,
                             (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 20))
            self.screen.blit(restart_text,
                             (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
            self.screen.blit(exit_text,
                             (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 80))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()