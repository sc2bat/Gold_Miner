# 집게를 어느지점 (pivot 중심점)으로부터 떨어트려서 배치
# self.rect 를 업데이트해야함

import os
import pygame

class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
    # 띄워주기위해 offset
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position
    
    def update(self):
        rect_center = self.position + self.offset
        self.rect = self.image.get_rect(center = rect_center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # 중심점 확인
        pygame.draw.circle(screen, RED, self.position, 3)

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
# 게임 관련변수
# 중심점으로부터 집게까지의 기본 x 간격
default_offset_x_claw = 40 
# 색변수
RED = (255, 0, 0)

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
    # 업데이트
    claw.update()
    claw.draw(screen)

    pygame.display.update()

pygame.quit()