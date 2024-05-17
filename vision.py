import cv2
import numpy as np
import os
# numbrite tuvastamine
import easyocr

# screenshot
from mss import mss
from PIL import Image

# types
from typing import Union, List
import logging

from config import Config

class GameVision():
    __debug:bool = False
    is_game:bool = True
    cur_mistake = 0

    # numbrituvastuse mudel
    reader = easyocr.Reader(['en'])

    def __init__(self) -> None:
        self.__debug = logging.getLogger().isEnabledFor(logging.DEBUG)
        if self.__debug:
            self.create_debug_folders()
        logging.info(f"Screen parameters set to width:{Config.screen_width}, height:{Config.screen_height}")            
        logging.info(f"Vision AI is working")
        

        
    def get_board(self, src:str=Config.screenshot_name) -> Union[None, np.ndarray]:

        img = cv2.imread(src)
        # pildi eeltöötlus
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (13,13), 0)
        edges = cv2.Canny(gray, 1, 8)
        kernel = np.ones((1,1), np.uint8)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(closed, cv2.RECURS_FILTER, cv2.CHAIN_APPROX_SIMPLE)
        
        board = None
        for contour in contours:
            # pindala, ei ole ideaalne lahendus, aga töötab
            if cv2.contourArea(contour) > Config.board_area:
                board = contour
                break
        
        # boardi ja debugi pärast on vajalik        
        if board is None:
            return None

        x, y, w, h = cv2.boundingRect(board)
        # loome lauda pildi
        board_image = img[y:y+h, x:x+w]

        height, width = board_image.shape[:2]

        if abs(height - width) >= 5:
            logging.debug(f"Found an object that matches area, but it is not a square. Height: {height} width:{width}")
            return None
        
        if self.__debug:
            cv2.imwrite(Config.debug_processed_img_loc, closed)
            cv2.imwrite(Config.debug_board_img_loc, board_image)
            cv2.drawContours(img, [board], -1, (0, 255, 0), 3)
            cv2.imwrite(Config.debug_contours_img_loc, img)

        return board_image
    
    def extract_board_cells(self, board:np.ndarray) -> List[np.ndarray]:

        # pildi pikkus ja laius
        board_height, board_width, _ = board.shape

        # meie laua dimensioon
        rows = 4
        cols = 4

        # ühe ruudu pikkus ja laius
        cell_height = board_height // rows
        cell_width = board_width // cols
        cell_height

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
                cell = cv2.resize(cell, (200, 200), interpolation=cv2.INTER_LINEAR)
                cells_imgs.append(cell)

                if self.__debug:
                    cell_filename = os.path.join(Config.debug_cell_folder, f'cell_{row}_{col}.jpg')
                    cv2.imwrite(cell_filename, cell) 
        return cells_imgs
    
    def get_cell_number(self, img:np.ndarray) -> int:
        # Using EasyOCR to detect text on the image
        # allowlist [0-9], et mudel kontrolliks ainult numbreid
        result = self.reader.readtext(img,  allowlist ='0123456789')
        if result and self.is_result_numeric(result):
            num = int(result[0][1])

            self.validate_num(num)
            self.is_max()
            
            return num
        return 0

    def create_4x4_board(self, board:np.ndarray) -> List[List[int]]:
        self.reset_cur_mistakes()
        board_values = [self.get_cell_number(img) for img in self.extract_board_cells(board) ]
        board_state = [
            board_values[0:4], #rida1 
            board_values[4:8], 
            board_values[8:12],
            board_values[12:16] #rida2
        ]
        return board_state


    def take_screenshot(self) -> np.ndarray:
        # https://stackoverflow.com/questions/35097837/capture-video-data-from-screen-in-python
        mon = {'left': 0, 'top': 0, 'width': Config.screen_width , 'height': Config.screen_height}
        with mss() as sct:
            screenShot = sct.grab(mon)
            img = Image.frombytes(
                'RGB', 
                (screenShot.width, screenShot.height), 
                screenShot.rgb, 
            )
            open_cv_image = np.array(img)
            # Convert RGB to BGR, kuna cv2 on BGR
            # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            cv2.imwrite(Config.screenshot_name, open_cv_image)
            return open_cv_image
        
    def create_debug_folders(self) -> None:
      
        if self.__debug:
            os.makedirs(Config.debug_folder, exist_ok=True)
            os.makedirs(Config.debug_cell_folder, exist_ok=True)

    def validate_num(self, num:int) -> None:
         if num % 2 != 0:
            self.cur_mistake += 1

    def is_max(self) -> None:
        if self.cur_mistake == Config.vision_max_mistake:
            self.is_game = False

    def is_result_numeric(self, result)->bool:
        if not result[0][1].isnumeric():
            self.cur_mistake += 1
            self.is_max()
            return False
        return True


    def reset_cur_mistakes(self) -> None:
        self.cur_mistake = 0
