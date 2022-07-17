import pygame as pg
from gravity import GravityObject
import time
import random
def main():
    screen = pg.display.set_mode((600, 600))
    running = True
    pg.display.set_caption('A game')
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    clock = pg.time.Clock()
    blocks = []
    interval = 1
    prev = time.time()
    sinking = False
    sinkSpeed = 0.02
    prevSpawn = 1000
    p = GravityObject(300, 590, 10, 600)
    score = 0
    pg.font.init()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        font = pg.font.SysFont('Arial', 20)
        text_surface = font.render("Score: "+str(score), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(300, 10))
        screen.blit(text_surface, text_rect)
        currentFloor = 600
        for block in blocks:
            if block.x < p.x < block.x + 30 and block.y > p.y:
                if block.y < currentFloor:
                    currentFloor = block.y
        p.floor = currentFloor
        if time.time() - prev >= interval:
            spot = random.randint(-25, 595)
            if spot < prevSpawn + 30 and spot + 30 > prevSpawn:
                if spot + 60 > 570:
                    spot -= 60
                else:
                    spot += 60
            prevSpawn = spot
            floor = 600
            for i in range(len(blocks)):
                if spot - 30 < blocks[i].x < spot + 30:
                    if blocks[i].y < floor and blocks[i].fallSpeed == 1:
                        floor = blocks[i].y
            newBlock = GravityObject(spot, 20, 30, floor)
            newBlock.acceleration = 0.2
            blocks.append(newBlock)
            prev = time.time()
            if interval > 0.1:
                interval -= 0.05
            if sinkSpeed <= 0.4:
                sinkSpeed += 0.03
            if len(blocks) == 5:
                sinking = True
        newBlocks = []
        for i in range(len(blocks)):
            blocks[i].gravity()
            if blocks[i].y > 600:
                score += 1
            else:
                newBlocks.append(blocks[i])
            if blocks[i].y < p.y - 10 < blocks[i].y + 30 and blocks[i].x - 10 < p.x < blocks[i].x + 40 and blocks[i].fallSpeed != 1:
                running = False
            if blocks[i].y - 10 < p.y < blocks[i].y + 40 and blocks[i].x - 10 < p.x < blocks[i].x + 40 and blocks[i].fallSpeed == 1:
                if p.x > blocks[i].x + 36:
                    p.x = blocks[i].x + 40
                if p.x < blocks[i].x - 6:
                    p.x = blocks[i].x - 10
            pg.draw.rect(screen, 'gray', (blocks[i].x, blocks[i].y, 30, 30))
            if sinking:
                blocks[i].y += sinkSpeed
                blocks[i].floor += sinkSpeed
        blocks = newBlocks.copy()
        if pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_a]:
            p.x -= 4
            if p.x < 10:
                p.x = 10
        elif pg.key.get_pressed()[pg.K_RIGHT] or pg.key.get_pressed()[pg.K_d]:
            p.x += 4
            if p.x > 590:
                p.x = 590
        for block in blocks:
            if block.x - 10 < p.x < block.x + 40 and block.y - 10 < p.y < block.y + 40:
                if block.x > p.x-10:
                    p.x = block.x - 10
                if block.x + 30 < p.x + 10:
                    p.x = block.x + 30 + 10
                if block.y > p.y - 10:
                    p.jumping = False
                    p.y = block.y - 10
                if block.y + 30 < p.y - 10:
                    p.y = block.y + 40
        pg.draw.circle(screen, 'green', (p.x,p.y), 10)
        p.gravity()
        pg.display.update()
        clock.tick(60)
        screen.fill('white')
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KeyboardInterrupt
        font = pg.font.SysFont('Arial', 50)
        text_surface = font.render("Your final score was: " + str(score), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(300, 150))
        screen.blit(text_surface, text_rect)
        font = pg.font.SysFont('Arial', 50)
        text_surface = font.render("Press r to restart", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(300, 450))
        screen.blit(text_surface, text_rect)
        if pg.key.get_pressed()[pg.K_r]:
            main()
        pg.display.update()
        clock.tick(60)
        screen.fill('white')

main()
