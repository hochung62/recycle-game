import pygame
import random
import sys

pygame.init()

# 1. 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("재활용 분리배출 게임")

# 2. 색상 및 한글 지원 폰트 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ⚠️ 한글 폰트 경로 설정
try:
    font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 28)  # 윈도우 한글 폰트
except FileNotFoundError:
    print("malgun.ttf 폰트를 찾을 수 없습니다. 다른 폰트를 설정하세요.")
    pygame.quit()
    sys.exit()

# 3. 쓰레기 종류 및 이미지 로딩
waste_types = ["플라스틱", "종이", "비닐", "유리", "일반"]

waste_images = {
    "플라스틱": pygame.image.load("assets/plastic.png"),
    "종이": pygame.image.load("assets/paper.png"),
    "비닐": pygame.image.load("assets/vinyl.png"),
    "유리": pygame.image.load("assets/glass.png"),
    "일반": pygame.image.load("assets/general.png"),
}

bin_image = pygame.transform.scale(pygame.image.load("assets/bin.png"), (100, 80))
trash_bin_positions = {
    name: pygame.Rect(50 + i * 140, 500, 100, 80) for i, name in enumerate(waste_types)
}

# 4. 쓰레기 클래스
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

# 5. 게임 루프
def main():
    score = 0
    clock = pygame.time.Clock()
    time_limit = 60
    start_ticks = pygame.time.get_ticks()

    current_trash = Trash(random.choice(waste_types))
    offset_x, offset_y = 0, 0
    running = True

    while running:
        screen.fill(WHITE)
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        if seconds > time_limit:
            screen.fill(WHITE)
            end_text = font.render(f"게임 종료! 점수: {score}", True, BLACK)
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
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
                                score = max(0, score - 1)
                            current_trash = Trash(random.choice(waste_types))
                            break

            elif event.type == pygame.MOUSEMOTION:
                if current_trash.dragging:
                    mouse_x, mouse_y = event.pos
                    current_trash.rect.x = mouse_x + offset_x
                    current_trash.rect.y = mouse_y + offset_y

        # 쓰레기통 표시
        for category, bin_rect in trash_bin_positions.items():
            screen.blit(bin_image, bin_rect)
            label = font.render(category, True, BLACK)
            screen.blit(label, (bin_rect.x + 10, bin_rect.y - 30))

        # 쓰레기 아이템 표시
        current_trash.draw(screen)

        # 점수 및 시간 표시
        score_text = font.render(f"점수: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        timer_text = font.render(f"남은 시간: {int(time_limit - seconds)}초", True, BLACK)
        screen.blit(timer_text, (600, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
