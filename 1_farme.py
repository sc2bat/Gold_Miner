# 기본 틀

import pygame

pygame.init() # 초기화

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock() # fps 값 고정

running = True
while running:
    clock.tick(30) # fps 30으로 고정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()