import cv2
import numpy as np
import os

# numbrite tuvastamine
import easyocr

# mängu kontrollimiseks 
import pyautogui

from mss import mss
from PIL import Image

# types
from typing import Union, List

import random
import time

# AI
from search import ai

reader = easyocr.Reader(['en'])

def get_board(src:str="screen.png", debug:bool=False) -> Union[None, np.ndarray]:

    img = cv2.imread(src)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (13,13), 0)
    edges = cv2.Canny(gray, 1, 8)
    kernel = np.ones((1,1), np.uint8)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closed, cv2.RECURS_FILTER, cv2.CHAIN_APPROX_SIMPLE)
    
    board = None
    for contour in contours:
        # pindala, ei ole ideaalne lahendus, aga töötab
        if cv2.contourArea(contour) > 200000:
            board = contour
            break

    if board is None:
        return None

    x, y, w, h = cv2.boundingRect(board)
    # loome lauda pildi
    board_image = img[y:y+h, x:x+w]
    
    if debug:
        cv2.imwrite("test.jpg", closed)
        cv2.imwrite("board.jpg", board_image)
        cv2.drawContours(img, [board], -1, (0, 255, 0), 3)
        cv2.imwrite("testb.jpg", img)

    return board_image

def extract_board_cells(board:np.ndarray, debug:bool=True) -> List[np.ndarray]:

    # pildi pikkus ja laius
    board_height, board_width, _ = board.shape

    # meie laua dimensioon
    rows = 4
    cols = 4

    # ühe ruudu pikkus ja laius
    cell_height = board_height // rows
    cell_width = board_width // cols

    if debug:
        output_dir = 'cell_images'
        os.makedirs(output_dir, exist_ok=True)

    cells_imgs = []
    for row in range(rows):
        for col in range(cols):
            # Kõrgem matemaatika 
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = (col + 1) * cell_width
            y2 = (row + 1) * cell_height
            
            # salvestame ruudu massiivi
            cell = board[y1:y2, x1:x2]
            cells_imgs.append(cell)
            
    return cells_imgs

def get_cell_number(img:np.ndarray) -> int:

    # Using EasyOCR to detect text on the image
    # allowlist [0-9], et mudel kontrolliks ainult numbreid
    result = reader.readtext(img,  allowlist ='0123456789')
    return int(result[0][1]) if result else 0

def create_4x4_board(board:np.ndarray) -> List[List[int]]:
    board_values = [get_cell_number(img) for img in extract_board_cells(board) ]
    board_state = [
        board_values[0:4], #rida1 
        board_values[4:8], 
        board_values[8:12],
        board_values[12:16] #rida2
    ]
    return board_state


def take_screen_shot() -> np.ndarray:
    mon = {'left': 0, 'top': 0, 'width': 2560, 'height': 1440}
    with mss() as sct:
        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB', 
            (screenShot.width, screenShot.height), 
            screenShot.rgb, 
        )
        open_cv_image = np.array(img)
        # Convert RGB to BGR, kuna cv2 on BGR
        # kuskilt stackoverfloavist võtsin seda
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        cv2.imwrite("screen.png", open_cv_image)
        return open_cv_image

def move(direction:str) -> None:
    directions = {
        "up": lambda:pyautogui.press('up'),
        "down":lambda:pyautogui.press('down'),
        "left":lambda:pyautogui.press('left'),
        "right":lambda:pyautogui.press('right')
    }

    directions[direction]()



if __name__ == "__main__":
    moves_made = 0
    boards_loc = "boards2/"
    while True:
        take_screen_shot()
        # hetkel screenshot.png faili susteemis
        board = get_board(debug=False)
        
        if board is not None:
            new_board = create_4x4_board(board)
            print(new_board)
            cv2.imwrite(f"{boards_loc}/{moves_made}.png", board)
        else:
            print("board not found")
            time.sleep(3)
            continue


        # Mängu aju    
        next_move = ai(new_board)

        if next_move:
            move(next_move)
        else:
            break
        # testimiseks
        moves_made += 1
        # animatsiooni parast
        time.sleep(0.2)
