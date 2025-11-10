from typing import Tuple

import pygame
from enum import IntFlag

'''
00/000
color/type
'''
class Piece(IntFlag):
    Non = 0
    King = 1    # 001
    Pawn = 2    # 010
    Knight = 3  # 011
    Bishop = 4  # 100
    Rook = 5    # 101
    Queen = 6   # 110

    White = 8   # 01000
    Black = 16  # 10000
    ColorFilter = 7 # 00111

def getPos2Index(index):
    return index // 8, index % 8
def getIndex2Pos(pos):
    return int(pos[1] * 8 + pos[0])

def getPieceByChar(char):
    piece = Piece.Non

    if char.islower():
        piece = piece | Piece.White
    elif char.isupper():
        piece = piece | Piece.Black

    return piece | {
        'k': Piece.King,
        'p': Piece.Pawn,
        'n': Piece.Knight,
        'b': Piece.Bishop,
        'r': Piece.Rook,
        'q': Piece.Queen,
    }[char.lower()]


def availableRoutes(pos, piece, map):
    if piece == None: return []
    if piece == Piece.Non: return []
    # routes 객체를 재사용하도록 외부에서 넘길 수 있게
    routes = PieceRoutes(map)

    kind = piece & Piece.ColorFilter  # 타입만 추출

    dispatch = {
        Piece.King: routes.king_routes,
        Piece.Pawn: routes.pawn_routes,
        Piece.Knight: routes.knight_routes,
        Piece.Bishop: routes.bishop_routes,
        Piece.Rook: routes.rook_routes,
        Piece.Queen: routes.queen_routes,
    }

    try:
        return dispatch[kind](pos)
    except KeyError:
        return []

def piece_color(p: Piece):
    if p & Piece.White: return Piece.White
    if p & Piece.Black: return Piece.Black
    return None

#
class PieceRoutes:
    Coord = Tuple[int, int]

    def __init__(self, map):
        self.map = map

    def in_board(slef, x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

    def _empty(self, pos) -> bool:
        index = getIndex2Pos(pos)
        return self.map[index] == Piece.Non

    def _ally(self, pos, my_color) -> bool:
        index = getIndex2Pos(pos)
        p = self.map[index]
        return p != Piece.Non and piece_color(p) == my_color

    def _enemy(self, pos, my_color) -> bool:
        index = getIndex2Pos(pos)
        p = self.map[index]
        c = piece_color(p)
        return p != Piece.Non and (c is not None) and c != my_color

    def _ray(self, pos, dirs, my_color):
        x0, y0 = pos
        out = []
        for dx, dy in dirs:
            x, y = x0 + dx, y0 + dy
            while self.in_board(x, y):
                if self._ally((x, y), my_color):
                    break
                out.append((x, y))
                if not self._empty((x, y)):  # 적군이면 그 칸 추가 후 중단
                    break
                x += dx
                y += dy
        return out

    def king_routes(self, pos):
        x, y = pos
        me = self.map[getIndex2Pos(pos)]
        my_color = piece_color(me)
        moves = []
        for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            nx, ny = x + dx, y + dy
            if not self.in_board(nx, ny): continue
            if not self._ally((nx, ny), my_color):
                moves.append((nx, ny))
        return moves

    def queen_routes(self, pos):
        me = self.map[getIndex2Pos(pos)]
        my_color = piece_color(me)
        rook_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        bishop_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._ray(pos, rook_dirs + bishop_dirs, my_color)

    def rook_routes(self, pos):
        me = self.map[getIndex2Pos(pos)]
        my_color = piece_color(me)
        rook_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._ray(pos, rook_dirs, my_color)

    def bishop_routes(self, pos):
        me = self.map[getIndex2Pos(pos)]
        my_color = piece_color(me)
        bishop_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._ray(pos, bishop_dirs, my_color)

    def knight_routes(self, pos):
        x, y = pos
        me = self.map[getIndex2Pos(pos)]
        my_color = piece_color(me)
        moves = []
        for dx, dy in ((-2, -1), (-2, 1), (2, -1), (2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2)):
            nx, ny = x + dx, y + dy
            if not self.in_board(nx, ny): continue
            if not self._ally((nx, ny), my_color):
                moves.append((nx, ny))
        return moves

    def pawn_routes(self, pos):
        out = []
        me = self.map[getIndex2Pos(pos)]
        my_color = piece_color(me)
        if my_color == Piece.Black: out.append((pos[0], pos[1] - 1))
        if my_color == Piece.White: out.append((pos[0], pos[1] + 1))
        print('pawn', pos, me, my_color)
        return out
