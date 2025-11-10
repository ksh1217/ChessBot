import pygame
import json

from pieces import Piece

tilemap_color_list = None
chess_map_list = None
images = None

def load_resource():
    global tilemap_color_list
    global chess_map_list
    global images

    with open('Assets/map/tilemap_color_list.json', 'r') as f:
        tilemap_color_list = json.load(f)
    with open('Assets/map/chess_map.json', 'r') as f:
        chess_map_list = json.load(f)

    images = {
        Piece.King | Piece.White: pygame.image.load("Assets/image/king.png"),
        Piece.Queen | Piece.White: pygame.image.load("Assets/image/queen.png"),
        Piece.Rook | Piece.White: pygame.image.load("Assets/image/rook.png"),
        Piece.Knight | Piece.White: pygame.image.load("Assets/image/knight.png"),
        Piece.Bishop | Piece.White: pygame.image.load("Assets/image/bishop.png"),
        Piece.Pawn | Piece.White: pygame.image.load("Assets/image/pawn.png"),

        Piece.King | Piece.Black: _invert_rgb("Assets/image/king.png"),
        Piece.Queen | Piece.Black: _invert_rgb("Assets/image/queen.png"),
        Piece.Rook | Piece.Black: _invert_rgb("Assets/image/rook.png"),
        Piece.Knight | Piece.Black: _invert_rgb("Assets/image/knight.png"),
        Piece.Bishop | Piece.Black: _invert_rgb("Assets/image/bishop.png"),
        Piece.Pawn | Piece.Black: _invert_rgb("Assets/image/pawn.png"),

        "move_circle": pygame.image.load("Assets/image/move_circle.png").convert_alpha(),
        "target_circle": pygame.image.load("Assets/image/target_circle.png").convert_alpha(),
    }
    return True

def _invert_rgb(file_path) -> pygame.Surface:
    img = pygame.image.load(file_path)
    inv = img.copy()
    rgb = pygame.surfarray.pixels3d(inv)  # (W,H,3) 뷰
    rgb[:] = 255 - rgb  # RGB 반전
    del rgb  # 잠금 해제!
    return inv