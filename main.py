import pygame

import glm
# file import
import map as chessmap
import pieces
import resource_loader
from glm import ivec2

pygame.init()

# window param
width, height = 1400, 700
screen_size = ivec2(width, height)
background_color = 255, 255, 255

clock = pygame.time.Clock()

#
screen = pygame.display.set_mode(tuple(screen_size))

resource_loader.load_resource()

def runGame():
    running = True

    font_size = 45
    font = pygame.font.SysFont(None, font_size)

    tile_size = 60
    map = chessmap.Map(screen, screen_size, tile_size, "brown", "test")

    # text = font.render(map.getMap(), True, (0, 0, 0))
    # text_rect = text.get_rect(
    #     center=(
    #         size[0]*0.5,
    #         size[1] - font_size*0.5
    #     )
    # )

    routes = None
    select_piece_pos = None; select_piece = pieces.Piece.Non

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            map.poll_evnets(event)

        screen.fill(background_color)

        map.update()

        # if map.updated():
        #     print("test")
        #     text = font.render(map.getMap(), True, (0, 0, 0))
        #     text_rect = text.get_rect(
        #         center=(
        #             size[0]*0.5,
        #             size[1] - font_size*0.5
        #         )
        #     )

        # screen.blit(text, text_rect)

        pygame.display.flip()  # 더블버퍼 스왑
        clock.tick(60)  # FPS 60 고정as

runGame()
pygame.quit()
