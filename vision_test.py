from vision import GameVision
import os
import cv2

if __name__ == "__main__":
    vision = GameVision()
    # test dirs
    boards_1_path = "test_imgs/boards"
    webpages_with_board_path = "test_imgs/webpages/board"
    webpages_without_board_path = "test_imgs/webpages/other"

    # get_board
    webpages_with_board_imgs_paths = os.listdir(webpages_with_board_path) 
    webpages_without_board_imgs_paths = os.listdir(webpages_without_board_path) 
    boards_1_imgs_paths = os.listdir(boards_1_path) 

    for file in webpages_with_board_imgs_paths:
        assert vision.get_board(webpages_with_board_path+"/"+file) is not None

    for file in webpages_without_board_imgs_paths:
        assert vision.get_board(webpages_without_board_path+"/"+file) is None
        
    # extract_board_cells


    board_1_expected = {
        "0.png":[[8, 2,8,4], [4,128,32,8], [2,4,2,4], [2,32,0,0]],
        "2.png":[[8, 2,8,4], [4,128,32,8], [2,4,2,4], [0,2,2,32]],
        "4.png":[[8, 2,8,4], [4,128,32,8], [0,2,4,8], [2,0,4,32]],
        "5.png":[[8, 2,8,4], [4,128,32,8], [2,4,8,0], [2,4,32,2]],
        "6.png":[[8, 2,8,4], [4,128,32,8], [2,2,4,8], [2,4,32,2]],
        "7.png":[[0, 2,8,2], [8,128,32,4], [4,2,4,16], [4,4,32,2]],
        "8.png":[[8, 2,8,2], [8,128,32,4], [2,2,4,16], [0,4,32,2]],
        "9.png":[[8, 2,8,2], [8,128,32,4], [0,4,4,16], [2,4,32,2]],
        "10.png":[[8, 2,8,2], [8,128,32,4], [2,0,8,16], [2,4,32,2]],
        "11.png":[[8, 2,8,2], [8,128,32,4], [2,8,16,2], [2,4,32,2]],
        "12.png":[[0, 2,8,2], [0,128,32,2], [16,8,16,4], [4,4,32,4]],
        "13.png":[[2, 2,8,2], [0,128,32,2], [16,8,16,4], [0,8,32,4]],
        "15.png":[[2, 4,8,2], [128,32,2,2], [16,8,16,4], [8,32,4,0]],
        "16.png":[[2, 4,8,2], [128,32,4,0], [16,8,16,4], [8,32,4,2]],
        "17.png":[[2, 4,8,2], [128,32,4,4], [16,8,16,2], [8,32,4,2]],
    }

    for file in boards_1_imgs_paths:
        board = cv2.imread(boards_1_path+"/"+file)
        new_board = vision.create_4x4_board(board) 
        assert new_board == board_1_expected[file]

    # img with big number
    board = cv2.imread("test_imgs/epic_board_2.png")
    new_board = vision.create_4x4_board(board) 
    assert new_board == [[32,64,8192,16384],[16,128,4096,32768],[8,256,2048,65536],[4,512,1024,131072]]

    