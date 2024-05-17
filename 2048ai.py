import cv2
# mängu kontrollimiseks 
import pyautogui
import time
# AI Vision
from vision import GameVision
# AI
from search import ai
import logging
from config import Config

def move(direction:str) -> None:
    directions = {
        "up": lambda:pyautogui.press('up'),
        "down":lambda:pyautogui.press('down'),
        "left":lambda:pyautogui.press('left'),
        "right":lambda:pyautogui.press('right')
    }

    directions[direction]()



if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - [%(levelname)s] - %(message)s", level=Config.logging_level, datefmt="%H:%M:%S")
    vision:GameVision = GameVision()
    debug = logging.getLogger().isEnabledFor(logging.DEBUG)
    moves_made = 0
    game_not_found = 0
    prev_board = []

    while True:
        vision.take_screenshot()
        # hetkel screenshot.png faili susteemis
        board = vision.get_board()

        if game_not_found == Config.game_not_found_max:
            logging.error("The game was not found")
            logging.error("Make sure that screen.png in the code folder represents your screen correctly")
            logging.error(f"Current screen resolution is set to {Config.screen_width}x{Config.screen_height}")
            logging.error("The resolution can be changed in config.py")
            logging.error("Also, make sure that you grant the necessary access to the screen capture.")
            break
        
        if board is not None:
            new_board = vision.create_4x4_board(board)
            logging.debug(new_board)
            if debug:
                cv2.imwrite(f"{Config.boards_loc}/{moves_made}.png", board)
            game_not_found = 0
        else:
            logging.warning("Board not found, please open webpage with game")
            time.sleep(Config.board_not_found_waiting_time)
            game_not_found += 1
            continue

        if prev_board == new_board:
            logging.error("Game controls do not work. It looks like your system requires permission access")
            break

        if not vision.is_game:
            logging.info("Game finished")
            break

        # Mängu aju    
        next_move = ai(new_board)

        if next_move:
            logging.debug(f"Next move: {next_move}")
            move(next_move)
        else:
            break
        # testimiseks
        moves_made += 1
        prev_board = new_board
        # animatsiooni parast
        time.sleep(Config.animation_delay)
