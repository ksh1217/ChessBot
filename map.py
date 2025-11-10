import pygame

import pieces
from pieces import Piece
from glm import ivec2
import resource_loader

class Map:
    def __init__(self, screen, screen_size, tile_size, tilemap_color_name='black-white', chess_map_name='default'):
        self.screen = screen
        self.screen_size = screen_size
        self._tile_size = tile_size

        # default setting
        self._tilemap_color = resource_loader.tilemap_color_list[tilemap_color_name]

        self._chess_map = []
        self.setChessMap(chess_map_name)

        self._update_toggle = False

        self.select_pos = None
        self.select_piece = None
        self.routes = None

    #
    def setTileSize(self, size):
        self._tile_size = size
    def setTilemapColor(self, tilemap_name):
        self._tilemap_color = resource_loader.tilemap_color_list[tilemap_name]
    def setChessMap(self, chess_map_name):
        self._chess_map.clear()
        for c in resource_loader.chess_map_list[chess_map_name]:
            if c == '/': continue

            if c.isdigit():
                self._chess_map = (
                        self._chess_map
                        + [Piece.Non for _ in range(int(c))]
                )
            else:
                self._chess_map.append(pieces.getPieceByChar(c))

    def getFEN(self):
        pass
    def getMap(self):
        return self._chess_map
    def getPiece(self, pos):
        return self._chess_map[pos]

    # def click_tile_event(self, event_pos, screen_size, size):
    #     self.setTileSize(size // 8)
    #
    #     middle = mx, my = screen_size[0]/2, screen_size[1]/2
    #     pos = cx, cy = (
    #         mx - (4 * self._tile_size),
    #         my - (4 * self._tile_size)
    #     )
    #     if ((event_pos[0] > cx + 8 * self._tile_size
    #             or event_pos[1] > cy + 8 * self._tile_size) or
    #         (event_pos[0] < cx
    #             or event_pos[1] < cy)
    #     ):
    #         return 0
    #
    #     select_pos = ivec2(
    #         (event_pos[0] - cx) // self._tile_size,
    #         (event_pos[1] - cy) // self._tile_size
    #     )
    #
    #     self.getPiece(select_pos)


    def compute(self):

        self._update_toggle = True

    def updated(self):
        if not self._update_toggle: return False
        self._update_toggle = False

    def _select_tile_event(self, event_pos):
        middle = self.screen_size * ivec2(0.5)
        pos = middle - (4 * self._tile_size)
        if ((event_pos[0] > pos.x + 8 * self._tile_size
             or event_pos[1] > pos.y + 8 * self._tile_size) or
                (event_pos[0] < pos.x
                 or event_pos[1] < pos.y)
        ):
            return 0
        select_pos = ivec2(
            (event_pos[0] - pos.x) // self._tile_size,
            (event_pos[1] - pos.y) // self._tile_size
        )
        return (select_pos, self.getPiece(select_pos))

    def poll_evnets(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.select_pos, self.select_piece = self._select_tile_event(event.pos)
            # print(select_piece, select_pos)
            self.routes = pieces.availableRoutes(self.select_pos, self.select_piece, self._chess_map)

    # render
    def update(self):
        for pos in ivec2.range(8, 8):
            self._draw_tile(pos)

    def _draw_tile(self, pos):
        tile_color = self._tilemap_color[(pos.x + pos.y) % 2]
        self._draw_map_tile(tile_color, pos)
        self._draw_piece(pos)

        self._draw_routes()

    def _draw_piece(self, pos):
        piece = self.getPiece(pos)
        if piece == Piece.Non: return
        self._draw_image_tile(
            piece,
            pos,
            self._tile_size
        )

    def _draw_routes(self):
        if self.select_piece == None or self.select_piece == Piece.Non: return
        self._draw_map_tile(
            (0, 150, 0, 100),
            self.select_pos
        )
        self._draw_piece(self.select_pos)
        if self.routes == None: return
        piece_color = pieces.piece_color(self.select_piece)
        for route in self.routes[0]:
            self._draw_image_tile(
                "move_circle",
                route,
                self._tile_size * 0.3,
                128
            )
        for route in self.routes[1]:
            self._draw_image_tile(
                "target_circle",
                route,
                self._tile_size,
                128
            )

    def _draw_image_tile(self, image, pos, size, alpha = 255):
        middle = mx, my = self.screen_size[0] * 0.5, self.screen_size[1] * 0.5

        tile_pos = cx, cy = (
            mx - (4 * self._tile_size) + (pos[0] * self._tile_size) + ((self._tile_size - size) * 0.5),
            my - (4 * self._tile_size) + (pos[1] * self._tile_size) + ((self._tile_size - size) * 0.5)
        )

        img = pygame.transform.smoothscale(resource_loader.images[image], (size, size))
        img.set_alpha(alpha)
        self.screen.blit(img, tile_pos)

    def _draw_map_tile(self, color, pos):
        mx, my = self.screen_size[0] * 0.5, self.screen_size[1] * 0.5
        cx, cy = (
            mx - (4 * self._tile_size) + (pos.x * self._tile_size),
            my - (4 * self._tile_size) + (pos.y * self._tile_size)
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
        self.screen.blit(rect_surf, (cx, cy))