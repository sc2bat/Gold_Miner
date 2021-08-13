# 보석
import os
import pygame

# 보석 클래스
# pygame 이 제공하는 sprite 를 상속받아서 새로운 클래스를 정의하고
# 이미지와 렉트 정보 반드시 정의
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__() 
        self.image = image
        self.rect = image.get_rect(center=position) # x, y 좌표

def setup_gemstone():
    # position 튜플로 감싸고 좌표는 임의로 작성
    s_g = Gemstone(gemstone_imgs[0], (200, 380)) 
    gemstone_group.add(s_g) # 그룹에 추가
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

# 4개의 보석 이미지 불러오기
gemstone_imgs = [
    pygame.image.load(os.path.join(current_path, "s_g.png")), # small gold
    pygame.image.load(os.path.join(current_path, "b_g.png")), # big gold
    pygame.image.load(os.path.join(current_path, "stone.png")), 
    pygame.image.load(os.path.join(current_path, "dia.png"))]

# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone()

    
running = True
while running:
    clock.tick(30) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    # 보석 그룹 내 모든 sprite 그림
    gemstone_group.draw(screen)

    pygame.display.update()

pygame.quit()