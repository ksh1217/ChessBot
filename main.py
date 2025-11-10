import pygame

# file import
import map as Map
import pieces

pygame.init()

# window param
size = width, height = 1400, 700
background_color = 255, 255, 255

clock = pygame.time.Clock()

#
screen = pygame.display.set_mode(size)

def runGame():
    running = True

    map = Map.Renderer("brown")
    map.setChessMap('test')

    map_size = 600

    routes = None
    select_piece_pos = None; select_piece = pieces.Piece.Non
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                select_piece_pos, select_piece = map.selectPiece(event.pos, size, map_size)
                routes = pieces.availableRoutes(select_piece_pos, select_piece, map.getNumMap())
                print(select_piece_pos, select_piece)

        screen.fill(background_color)

        map.draw(screen, size, map_size, select_piece_pos, select_piece, routes)

        pygame.display.flip()  # 더블버퍼 스왑
        clock.tick(60)  # FPS 60 고정as

runGame()
pygame.quit()
