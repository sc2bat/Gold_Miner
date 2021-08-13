# 게임오버
# 제한시간 부여
# 목표 점수 달성 게임 성공

import os
import math
import pygame

class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT
        self.angle_speed = 2.5
        self.angle = 10 
    
    def update(self, to_x):
        if self.direction == LEFT:
            self.angle += self.angle_speed
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x

        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)

        self.rect = self.image.get_rect(center=self.position+offset_rotated)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed):
        super().__init__() 
        self.image = image
        self.rect = image.get_rect(center=position) 
        self.price = price
        self.speed = speed
        
    def set_position(self, position, angle):
        r = self.rect.size[0] // 2
        rad_angle = math.radians(angle)
        to_x = r * math.cos(rad_angle)
        to_y = r * math.sin(rad_angle)
        self.rect.center = (position[0] + to_x, position[1] + to_y)

def setup_gemstone():
    s_g_price, s_g_speed = 100, 5
    b_g_price, b_g_speed = 300, 2
    stone_price, stone_speed = 10, 2
    dia_price, dia_speed = 600, 7
    s_g = Gemstone(gemstone_imgs[0], (200, 380), s_g_price, s_g_speed) 
    gemstone_group.add(s_g) 
    gemstone_group.add(Gemstone(gemstone_imgs[1], (300, 500), b_g_price, b_g_speed))
    gemstone_group.add(Gemstone(gemstone_imgs[2], (300, 380), stone_price, stone_speed))
    gemstone_group.add(Gemstone(gemstone_imgs[3], (900, 400), dia_price, dia_speed))

def update_score(score):
    global curr_score
    curr_score += score
    
def display_score():
    txt_curr_score = game_font.render(f"Curr Score : {curr_score:,}", True, BLACK)
    screen.blit(txt_curr_score, (50, 20))

    txt_goal_score = game_font.render(f"Goal Score : {goal_score:,}", True, BLACK)
    screen.blit(txt_goal_score, (50, 80))

# 시간
def display_time(time):
    txt_timer = game_font.render(f"TIME : {time}", True, BLACK)
    screen.blit(txt_timer, (1000, 50))

# 게임 종료
def display_game_over():
    game_font = pygame.font.SysFont("arialblack", 60)
    txt_game_over = game_font.render(game_result, True, BLACK)
    # 화면 중간에 위치
    rect_game_over = txt_game_over.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(txt_game_over, rect_game_over)


pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock() 

game_font = pygame.font.SysFont("arialblack",30)
goal_score = 1500
curr_score = 0

# game over 변수
# 게임 결과
game_result = None 
# 시간
total_time = 60
# 현재 tick (시간)을 받아옴
start_ticks = pygame.time.get_ticks()

default_offset_x_claw = 40 

to_x = 0
caught_gemstone = None 
move_speed = 12 
return_speed = 20

LEFT = -1 
RIGHT = 1
STOP = 0 

RED = (255, 0, 0)
BLACK = (0, 0, 0)

current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

gemstone_imgs = [
    pygame.image.load(os.path.join(current_path, "s_g.png")).convert_alpha(), 
    pygame.image.load(os.path.join(current_path, "b_g.png")).convert_alpha(), 
    pygame.image.load(os.path.join(current_path, "stone.png")).convert_alpha(), 
    pygame.image.load(os.path.join(current_path, "dia.png")).convert_alpha()]

gemstone_group = pygame.sprite.Group()
setup_gemstone()

claw_image = pygame.image.load(os.path.join(current_path, "claw.png")).convert_alpha()
claw = Claw(claw_image, (screen_width // 2, 110))
    
running = True
while running:
    clock.tick(30) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            claw.set_direction(STOP)
            to_x = move_speed
    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed
    if claw.offset.x < default_offset_x_claw:
        to_x = 0
        claw.set_init_state()

        if caught_gemstone:
            update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None

    if not caught_gemstone:
        for gemstone in gemstone_group:
            if pygame.sprite.collide_mask(claw, gemstone):
                caught_gemstone = gemstone
                to_x = -gemstone.speed
                break

    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)
    claw.update(to_x)
    claw.draw(screen)

    display_score()

    # 시간 계산
    # 경과 시간 ms -> s
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    # 남은 시간
    # 1234 -> 1.234 -> int -> 1
    display_time(total_time - int(elapsed_time))
    # 시간이 0이하면 게임 종료
    if total_time - int(elapsed_time) <= 0:
        running = False
        if curr_score >= goal_score:
            game_result = "Winner Winner Chicken Winner"
        else:
            game_result = "Game Over"
    # 게임 종료 표시
        display_game_over()


    pygame.display.update()

# 게임 종료 후 2초대기
pygame.time.delay(2000)

pygame.quit()