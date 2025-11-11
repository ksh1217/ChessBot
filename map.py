import pygame
from dask import compute

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

        self._chess_FEN = resource_loader.chess_map_list[chess_map_name]
        self._chess_map = []
        self.setChessMap(chess_map_name)

        self._update_toggle = False
        self._compute = False

        self.select_pos = None
        self.select_piece = None
        self.routes = None

        self._FEN_count = 0
        self._win_team = Piece.Non
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
        return self._chess_FEN
    def getMap(self):
        return self._chess_map
    def getPiece(self, pos):
        return self._chess_map[pos]

    def ended(self):
        return self._win_team

    def compute(self):
        self._chess_FEN = ""
        self._FEN_count = 0
        self._compute = True

    def updated(self):
        if not self._update_toggle: return False
        self._update_toggle = False
        self._compute = False
        return True

    def _compute_select_tile(self, event_pos):
        middle = self.screen_size * ivec2(0.5)
        pos = middle - (4 * self._tile_size)
        epos = ivec2(
            (event_pos[0] - pos.x) // self._tile_size,
            (event_pos[1] - pos.y) // self._tile_size
        )
        if (epos.x < 0 or 7 < epos.x
            or epos.y < 0 or 7 < epos.y
        ):
            return None
        return epos
    def _select_tile_event(self, event_pos, turn):
        select_pos = self._compute_select_tile(event_pos)
        if select_pos is None:
            return (None, None)
        piece = self.getPiece(select_pos)
        if ~Piece.ColorFilter & piece is not turn:
            return (None, None)
        return (select_pos, piece)
    def _move_piece_event(self, event_pos):
        if self.select_piece is not None and len(self.routes) > 0:
            spos = self._compute_select_tile(event_pos)
            if spos is None: return False
            for pos in self.routes[0]:
                if pos == spos:
                    self._chess_map[spos] = self.select_piece
                    self._chess_map[self.select_pos] = Piece.Non
                    self.select_piece = None
                    return True
            for pos in self.routes[1]:
                if pos == spos:
                    if self._chess_map[spos] & Piece.ColorFilter == Piece.King:
                        self._win_team = self._chess_map[spos] & ~Piece.ColorFilter
                    self._chess_map[spos] = self.select_piece
                    self._chess_map[self.select_pos] = Piece.Non
                    self.select_piece = None
                    return True
        return False

    def poll_evnets(self, event, turn):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._move_piece_event(event.pos):
                self.compute()
            else:
                self.select_pos, self.select_piece = self._select_tile_event(event.pos, turn)
                self.routes = pieces.availableRoutes(self.select_pos, self.select_piece, self._chess_map)
            # print(select_piece, select_pos)
            # if not moved:

    # render
    def update(self):
        self._update_toggle = self._compute
        for pos in ivec2.range(8, 8):
            self._draw_tile(pos)
        self._draw_routes()

    def _draw_tile(self, pos):
        tile_color = self._tilemap_color[(pos.x + pos.y) % 2]
        self._draw_map_tile(tile_color, pos)
        # if self.select_pos is not None and self.select_pos == pos: return
        self._draw_piece(pos)

    def _draw_piece(self, pos):
        piece = self.getPiece(pos)
        if self._update_toggle:
            if piece == Piece.Non:
                self._FEN_count = self._FEN_count + 1
            else:
                if self._FEN_count > 0:
                    self._chess_FEN = self._chess_FEN + str(self._FEN_count)
                    self._FEN_count = 0
                self._chess_FEN = self._chess_FEN + pieces.getCharByPiece(piece)
            if pos.x >= 7:
                # print(pos.x, pos.y)
                self._FEN_count = 0
                self._chess_FEN = self._chess_FEN + "/"

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