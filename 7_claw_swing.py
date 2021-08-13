# 집게 좌우로 이동

import os
import pygame

class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        # 
        self.original_image = image
        self.rect = image.get_rect(center=position)
        # 백터2 rotate 를 제공함
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        # 방향변수
        # 집게의 이동방향
        self.direction = LEFT
        # 집게의 각도 변경 폭
        self.angle_speed = 2.5
        # 최초 각도 정의
        self.angle = 10 
    
    def update(self):
        # 왼쪽으로 이동한다면 속도만큼 각도 증가
        if self.direction == LEFT:
            self.angle += self.angle_speed
        # 오른쪽으로 이동한다면 속도만큼 각도 증가
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed
        # 허용 각도 범위를 벗어나면?
        if self.angle > 170:
            self.angle = 170
            self.direction = RIGHT
        elif self.angle < 10:
            self.angle = 10
            self.direction = LEFT
        # 확인
        # print(self.angle, self.direction) 
              
        # rect_center = self.position + self.offset
        # self.rect = self.image.get_rect(center = rect_center)
        self.rotate()

    # 회전하는이미지
    def rotate(self):
        # pygame.transform.rotate() # 같은 매락이지만 화면상 매끄럽지 못한 부분이 있다고 함
        # 회전 시킬 이미지
        # 음수 이유 시계방향으로 각도를 계산하므로 
        # 1 이미지 크기 변동 없음
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        # 새롭게 이동된 옵셋 값을 가져옴
        offset_rotated = self.offset.rotate(self.angle)
        # print(offset_rotated)

        self.rect = self.image.get_rect(center=self.position+offset_rotated)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)

class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__() 
        self.image = image
        self.rect = image.get_rect(center=position) 
        

def setup_gemstone():
    s_g = Gemstone(gemstone_imgs[0], (200, 380)) 
    gemstone_group.add(s_g) 
    gemstone_group.add(Gemstone(gemstone_imgs[1], (300, 500)))
    gemstone_group.add(Gemstone(gemstone_imgs[2], (300, 380)))
    gemstone_group.add(Gemstone(gemstone_imgs[3], (900, 400)))

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock() 
default_offset_x_claw = 40 
# 방향
LEFT = -1 
RIGHT = 1 

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

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)
    claw.update()
    claw.draw(screen)

    pygame.display.update()

pygame.quit()