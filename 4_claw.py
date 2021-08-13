# 보석을 집는 집게

import os
import pygame

# claw class
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
    # 클래스 객체 내에서 처리
    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

gemstone_imgs = [
    pygame.image.load(os.path.join(current_path, "s_g.png")), 
    pygame.image.load(os.path.join(current_path, "b_g.png")), 
    pygame.image.load(os.path.join(current_path, "stone.png")), 
    pygame.image.load(os.path.join(current_path, "dia.png"))]

gemstone_group = pygame.sprite.Group()
setup_gemstone()

# 집게
claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
# 화면 가로크기 기준으로 절반, 세로 위로부터 110px 위치
claw = Claw(claw_image, (screen_width // 2, 110))

    
running = True
while running:
    clock.tick(30) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)
    # 집게 그리기
    claw.draw(screen) # 각각의 sprite 로는 draw 불가 따라서 클래스 내에 별도로 처리

    pygame.display.update()

pygame.quit()