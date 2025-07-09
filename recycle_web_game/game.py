
import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("재활용 분리배출 게임")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 28)

waste_types = ["플라스틱", "종이", "비닐", "유리", "일반"]
waste_images = {
    "플라스틱": pygame.image.load("assets/plastic.png"),
    "종이": pygame.image.load("assets/paper.png"),
    "비닐": pygame.image.load("assets/vinyl.png"),
    "유리": pygame.image.load("assets/glass.png"),
    "일반": pygame.image.load("assets/general.png"),
}
bin_image = pygame.transform.scale(pygame.image.load("assets/bin.png"), (100, 80))
trash_bin_positions = {name: pygame.Rect(50 + i * 140, 500, 100, 80) for i, name in enumerate(waste_types)}

class Trash:
    def __init__(self, name):
        self.name = name
        self.image = pygame.transform.scale(waste_images[name], (100, 50))
        self.rect = self.image.get_rect(topleft=(random.randint(100, 600), 50))
        self.dragging = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        label = font.render(self.name, True, BLACK)
        screen.blit(label, (self.rect.x + 5, self.rect.y + 55))

current_trash = Trash(random.choice(waste_types))
score = 0
clock = pygame.time.Clock()
time_limit = 60
start_ticks = pygame.time.get_ticks()

running = True
while running:
    screen.fill(WHITE)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds > time_limit:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_trash.rect.collidepoint(event.pos):
                current_trash.dragging = True
                offset_x = current_trash.rect.x - event.pos[0]
                offset_y = current_trash.rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            if current_trash.dragging:
                current_trash.dragging = False
                for category, bin_rect in trash_bin_positions.items():
                    if bin_rect.collidepoint(current_trash.rect.center):
                        if category == current_trash.name:
                            score += 1
                        else:
                            score -= 1
                        current_trash = Trash(random.choice(waste_types))

        elif event.type == pygame.MOUSEMOTION:
            if current_trash.dragging:
                mouse_x, mouse_y = event.pos
                current_trash.rect.x = mouse_x + offset_x
                current_trash.rect.y = mouse_y + offset_y

    for category, bin_rect in trash_bin_positions.items():
        screen.blit(bin_image, bin_rect)
        label = font.render(category, True, BLACK)
        screen.blit(label, (bin_rect.x + 10, bin_rect.y - 40))

    current_trash.draw(screen)
    score_text = font.render(f"점수: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    timer_text = font.render(f"남은 시간: {int(time_limit - seconds)}초", True, BLACK)
    screen.blit(timer_text, (600, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
