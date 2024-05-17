import logging

class Config:
    # Screen settings
    screen_width = 1440
    screen_height = 900

    # Logging level INFO sobilik, kui soovite naha koik logid, siis mutke INFO -> DEBUG
    logging_level = logging.INFO

    # Debug directories
    boards_loc = "boards2/"
    debug_folder:str = "debug_imgs/"
    debug_cell_folder:str = f"{debug_folder}/cell_images"
    debug_contours_img_loc = f"{debug_folder}/all_contours.jpg"
    debug_board_img_loc = f"{debug_folder}/board.jpg"
    debug_processed_img_loc = f"{debug_folder}/processed_img.jpg"

    # Screenshot name
    screenshot_name = "screen.png"

    # End the game of board was not found n times
    game_not_found_max = 10
    # If board not found wait n seconds
    board_not_found_waiting_time = 3
    # Animation constant
    animation_delay = 0.2

    # Max possible mistakes -> number not % 2 == 0
    vision_max_mistake = 2

    # Area of the board
    board_area = 200000

