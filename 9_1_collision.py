# 충돌처리1

import os
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
    # 각 광석의 무게에 따른 스피드와 가격
    def __init__(self, image, position, price, speed):
        super().__init__() 
        self.image = image
        self.rect = image.get_rect(center=position) 
        ##
        self.price = price
        self.speed = speed
        

def setup_gemstone():
    # 각 광석의 가격과 스피드 변수
    s_g_price, s_g_speed = 100, 5
    b_g_price, b_g_speed = 300, 2
    stone_price, stone_speed = 10, 2
    dia_price, dia_speed = 600, 7
    # 추가한 변수를 집어넣음
    s_g = Gemstone(gemstone_imgs[0], (200, 380), s_g_price, s_g_speed) 
    gemstone_group.add(s_g) 
    gemstone_group.add(Gemstone(gemstone_imgs[1], (300, 500), b_g_price, b_g_speed))
    gemstone_group.add(Gemstone(gemstone_imgs[2], (300, 380), stone_price, stone_speed))
    gemstone_group.add(Gemstone(gemstone_imgs[3], (900, 400), dia_price, dia_speed))

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock() 
default_offset_x_claw = 40 

to_x = 0
# 집게로 잡은 보석
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
    pygame.image.load(os.path.join(current_path, "s_g.png")), 
    pygame.image.load(os.path.join(current_path, "b_g.png")), 
    pygame.image.load(os.path.join(current_path, "stone.png")), 
    pygame.image.load(os.path.join(current_path, "dia.png"))]

gemstone_group = pygame.sprite.Group()
setup_gemstone()

claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
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

        # 잡은 보석 제거
        if caught_gemstone:
            # update_score(caught_gemstone.price) # 점수 업데이트 처리
            # 그룹에서 잡은 보석 제외
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None

    # 잡힌 보석이 없다면 충돌체크
    if not caught_gemstone:
        for gemstone in gemstone_group:
            # 충돌 체크
            if claw.rect.colliderect(gemstone.rect):
                # 잡힌 보석
                caught_gemstone = gemstone
                # 잡은 보석에 따른 속도
                to_x = -gemstone.speed
                # 보석을 잡았기 때문에 break로 탈출
                break

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)
    claw.update(to_x)
    claw.draw(screen)

    pygame.display.update()

pygame.quit()