import pygame
import json

import pieces


def getPieceByPos(pos, map):
    return getPieceByIndex(pos[1] * 8 + pos[0], map)
def getPieceByIndex(index, map):
    for c in map:
        if c == '/': continue

        if index == 0:
            if not c.isdigit():
                return c
            else:
                return None

        if c.isdigit():
            index = index - int(c)
        else:
            index = index - 1


class Renderer:
    def __init__(self, tilemap_color_name='black-white', chess_map_name='default'):
        with open('tilemap_color_list.json', 'r') as f:
            self._tilemap_color_list = json.load(f)
        with open('chess_map.json', 'r') as f:
            self._chess_map_list = json.load(f)

        # default setting
        self._tilemap_color = self._tilemap_color_list[tilemap_color_name]

        self._chess_map = []
        self._chess_num_map = []
        self.setChessMap(chess_map_name)

        self.font = pygame.font.SysFont('comicsans', 30)

        self._tile_size = 60

        # 
    def setTileSize(self, size):
        self._tile_size = size

    def setTilemapColor(self, tilemap_name):
        self._tilemap_color = self._tilemap_color_list[tilemap_name]

    def setChessMap(self, chess_map_name):
        self._chess_map = self._chess_map_list[chess_map_name]

        self._chess_num_map.clear()
        for c in self._chess_map:
            if c == '/': continue

            if c.isdigit():
                self._chess_num_map = (
                        self._chess_num_map
                        + [pieces.Piece.Non for _ in range(int(c))]
                )
            else:
                self._chess_num_map.append(pieces.getPieceByChar(c))


    def getMap(self):
        return self._chess_map
    def getNumMap(self):
        return self._chess_num_map

    def selectPiece2Index(self, index):
        return getPieceByIndex(index, self._chess_map)
    def selectPiece2Pos(self, pos):
        return self.selectPiece2Index(pos[1] * 8 + pos[0])
    def selectPiece(self, event_pos, screen_size, size):
        self.setTileSize(size // 8)

        middle = mx, my = screen_size[0]/2, screen_size[1]/2
        pos = cx, cy = (
            mx - (4 * self._tile_size),
            my - (4 * self._tile_size)
        )
        if ((event_pos[0] > cx + 8 * self._tile_size
                or event_pos[1] > cy + 8 * self._tile_size) or
            (event_pos[0] < cx
                or event_pos[1] < cy)
        ):
            return 0

        select_pos = sx, sy = (
            (event_pos[0] - cx) // self._tile_size,
            (event_pos[1] - cy) // self._tile_size
        )

        piece_char = self.selectPiece2Pos(select_pos)
        if piece_char == None: return (select_pos, pieces.Piece.Non)
        return (select_pos, pieces.getPieceByChar(piece_char))

    # render
    def draw(self, screen, screen_size, size, select_pos, select_piece, routes):
        self.setTileSize(size // 8)

        for y in range(8):
            for x in range(8):
                index = y * 8 + x

                tile_color = self._tilemap_color[(x + y) % 2]

                self._draw_map_tile(
                    screen, screen_size,
                    tile_color,
                    (x, y)
                )

                self._draw_piece(screen, screen_size, index, (x, y))

        self._draw_routes(screen, screen_size, select_pos, select_piece, routes)

    def _draw_piece(self, screen, screen_size, index, pos):
        c = getPieceByIndex(index, self._chess_map)
        if c == None: return
        c = pieces.getPieceByChar(c)
        test = self.font.render(str(c), True, (255, 0, 0))

        middle = mx, my = screen_size[0] / 2, screen_size[1] / 2

        tile_pos = cx, cy = (
            mx - (4 * self._tile_size) + (pos[0] * self._tile_size),
            my - (4 * self._tile_size) + (pos[1] * self._tile_size)
        )

        screen.blit(test, tile_pos)

    def _draw_routes(self, screen, screen_size, pos, select_piece, routes):
        if select_piece == pieces.Piece.Non: return
        self._draw_map_tile(
            screen, screen_size,
            (255, 255, 0, 100),
            pos
        )
        if routes == None: return
        piece_color = pieces.piece_color(select_piece)
        for route in routes:
            route_piece = getPieceByPos(route, self._chess_map)
            if route_piece != None:
                route_piece = pieces.getPieceByChar(route_piece)
                if piece_color != pieces.piece_color(route_piece):
                    self._draw_map_tile(
                        screen, screen_size,
                        (255, 0, 0, 100),
                        route
                    )
                continue
            self._draw_map_tile(
                screen, screen_size,
                (255, 255, 0, 100),
                route,
            )

    def _draw_map_tile(self, screen, screen_size, color, pos):
        middle = mx, my = screen_size[0]/2, screen_size[1]/2

        tile_pos = cx, cy = (
            mx - (4 * self._tile_size) + (pos[0] * self._tile_size),
            my - (4 * self._tile_size) + (pos[1] * self._tile_size)
        )

        if len(color) == 3: color = color + [255]
        rect_surf = pygame.Surface(
            (self._tile_size, self._tile_size),
            pygame.SRCALPHA)
        pygame.draw.rect(
            rect_surf,
            color,
            rect_surf.get_rect()
        )
        screen.blit(rect_surf, (cx, cy))