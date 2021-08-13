# 집게까지 라인 선 긋기

import os
import pygame

class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position
    
    def update(self):
        rect_center = self.position + self.offset
        self.rect = self.image.get_rect(center = rect_center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)
        # 직선 그리기 
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
# 게임 관련변수
default_offset_x_claw = 40 
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