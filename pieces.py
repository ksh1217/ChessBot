from typing import Tuple

import pygame
from enum import IntFlag
from glm import ivec2

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

def getCharByPiece(piece: Piece):
    p = piece & Piece.ColorFilter
    c = {
        Piece.King: 'k',
        piece.Pawn: 'p',
        piece.Knight: 'n',
        piece.Bishop: 'b',
        piece.Rook: 'r',
        piece.Queen: 'q',
    }[p]
    if piece & Piece.Black > 0: c = c.upper()
    return c
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


def availableRoutes(pos, piece, map, enpassant):
    if piece == None or piece == Piece.Non: return []

    # routes 객체를 재사용하도록 외부에서 넘길 수 있게
    routes = PieceRoutes(map, enpassant)

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
def piece_invert_color(p: Piece):
    if p & Piece.White: return Piece.Black
    if p & Piece.Black: return Piece.White
    return None

#
class PieceRoutes:
    def __init__(self, map, enpassant):
        self.map = map
        self.enpassant = enpassant

    def in_board(slef, pos) -> bool:
        return 0 <= pos.x < 8 and 0 <= pos.y < 8

    def _empty(self, pos) -> bool:
        return self.map[pos] == Piece.Non

    def _ally(self, pos, my_color) -> bool:
        p = self.map[pos]
        return p != Piece.Non and piece_color(p) == my_color

    def _enemy(self, pos, my_color) -> bool:
        p = self.map[pos]
        c = piece_color(p)
        return p != Piece.Non and (c is not None) and c != my_color

    def _ray(self, pos, dirs, my_color):
        out = []
        out_enemy = []
        for dpos in dirs:
            npos = ivec2(pos + dpos)
            while self.in_board(npos):
                if self._ally(npos, my_color):
                    break
                if not self._empty(npos):  # 적군이면 그 칸 추가 후 중단
                    out_enemy.append(npos)
                    break
                out.append(npos)
                npos = npos + dpos
        return (out, out_enemy)

    def king_routes(self, pos):
        me = self.map[pos]
        my_color = piece_color(me)
        moves = []
        target = []
        for dpos in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            npos = ivec2(pos + dpos)
            if not self.in_board(npos): continue
            if not self._ally(npos, my_color):
                if self._ally(npos, piece_invert_color(my_color)):
                    target.append(npos)
                else:
                    moves.append(npos)
        return (moves, target)

    def queen_routes(self, pos):
        me = self.map[pos]
        my_color = piece_color(me)
        rook_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        bishop_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._ray(pos, rook_dirs + bishop_dirs, my_color)

    def rook_routes(self, pos):
        me = self.map[pos]
        my_color = piece_color(me)
        rook_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._ray(pos, rook_dirs, my_color)

    def bishop_routes(self, pos):
        me = self.map[pos]
        my_color = piece_color(me)
        bishop_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._ray(pos, bishop_dirs, my_color)

    def knight_routes(self, pos):
        me = self.map[pos]
        my_color = piece_color(me)
        moves = []
        target = []
        for dpos in ((-2, -1), (-2, 1), (2, -1), (2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2)):
            npos = pos + dpos
            if not self.in_board(npos): continue
            if not self._ally(npos, my_color):
                if self._ally(npos, piece_invert_color(my_color)):
                    target.append(npos)
                else:
                    moves.append(npos)
        return (moves, target)

    def pawn_routes(self, pos):
        x, y = pos
        me = self.map[pos]
        my_color = piece_color(me)
        enemy_color = piece_invert_color(my_color)
        moves = []
        target = []
        dir, start_rank = (-1, 6) if my_color == Piece.Black else (1, 1)
        for dx in (-1, 1):
            npos = ivec2(pos + (dx, dir))
            if self.in_board(npos):
                if self._ally(npos, enemy_color):
                    target.append(npos)
                if self.enpassant is not None and self.enpassant == npos:
                    target.append(npos)
        npos = ivec2(x, y + dir)
        if self.in_board(npos) and self._empty(npos):
            moves.append(npos)
            npos2 = ivec2(x, y + (dir * 2))
            if start_rank == y and self._empty(npos2):
                moves.append(npos2)

        return (moves, target)
