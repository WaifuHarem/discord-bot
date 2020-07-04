import numpy as np
import cv2
import re

from ffr.ffr_img_processing import FfrImgProcessing
from ffr.ffr_txt_processing import FfrTxtProcessing
from ocr import OCR


class FfrCore():

    # The game area w:h ratio
    ratio = 1.6254901960784313725490196078431

    # Constants to access rgb channels
    red   = 0
    green = 1
    blue  = 2
    
    def __init__(self, filename):
        '''
        Loads and crops image to include just the game area
        '''

        # read the image and get the dimensions
        img = cv2.imread(filename)

        # height, width, number of channels in image
        height   = img.shape[0]
        width    = img.shape[1]
        channels = img.shape[2]

        # Crop to game area
        if width > height:
            new_width = FfrCore.ratio*height
            black_bar_width = (width - new_width)/2

            # If statement guard against window title bar
            if black_bar_width > 0:
                img = img[:, int(black_bar_width) : int(width - black_bar_width)]
        else:
            new_height = width/FfrCore.ratio
            black_bar_height = (height - new_height)/2

            # If statement just in case
            if black_bar_height > 0:
                img = img[int(black_bar_height) : int(height - black_bar_height), :]

        # height, width, number of channels in image
        height   = img.shape[0]
        width    = img.shape[1]
        channels = img.shape[2]

        # See if the window title bar needs to be cropped out
        if width > height:
            new_height = width/FfrCore.ratio
            title_bar_height = height - new_height
            img = img[int(title_bar_height):, :]

        # height, width, number of channels in image
        self.height   = img.shape[0]
        self.width    = img.shape[1]
        self.channels = img.shape[2]

        # Filter out unwanted background color
        r_treshold = (0 <= img[:, :, FfrCore.red]) & (img[:, :, FfrCore.red] <= 60)
        g_treshold = (0 <= img[:, :, FfrCore.green]) & (img[:, :, FfrCore.green] <= 60)
        b_treshold = (0 <= img[:, :, FfrCore.blue])  & (img[:, :, FfrCore.blue] <= 60)
        img[r_treshold & g_treshold & b_treshold] = 0

        self.img = img


    def process_image(self):
        data = {
            'text' : {
                'hour'          : None,
                'minute'        : None,
                'second'        : None,
                'ampm'          : None,
                'day'           : None,
                'month'         : None,
                'year'          : None,
                'player'        : None,
                'title'         : None,
                'difficulty'    : None,
                'length_min'    : None,
                'length_sec'    : None,
                'artist'        : None,
                'creator'       : None,
                'amazing_score' : None,
                'perfect_score' : None,
                'good_score'    : None,
                'average_score' : None,
                'miss_score'    : None,
                'boo_score'     : None,
                'AAA_equiv'     : None,
                'raw_goods'     : None
            },
            'imgs' : []
        }

        self.__process_data(data, FfrImgProcessing.get_date_info_img,   FfrTxtProcessing.get_date_info_txt)
        self.__process_data(data, FfrImgProcessing.get_player_info_img, FfrTxtProcessing.get_player_info_txt)
        self.__process_data(data, FfrImgProcessing.get_map_title_img,   FfrTxtProcessing.get_map_title_txt)
        self.__process_data(data, FfrImgProcessing.get_map_info_img,    FfrTxtProcessing.get_map_info_txt)
        self.__process_data(data, FfrImgProcessing.get_amazing_img,     FfrTxtProcessing.get_amazing_txt)
        self.__process_data(data, FfrImgProcessing.get_perfect_img,     FfrTxtProcessing.get_perfect_txt)
        self.__process_data(data, FfrImgProcessing.get_good_img,        FfrTxtProcessing.get_good_txt)
        self.__process_data(data, FfrImgProcessing.get_average_img,     FfrTxtProcessing.get_average_txt)
        self.__process_data(data, FfrImgProcessing.get_miss_img,        FfrTxtProcessing.get_miss_txt)
        self.__process_data(data, FfrImgProcessing.get_boo_img,         FfrTxtProcessing.get_boo_txt)
        self.__process_data(data, FfrImgProcessing.get_aaa_equiv_img,   FfrTxtProcessing.get_aaa_equiv_txt)
        self.__process_data(data, FfrImgProcessing.get_raw_goods_img,   FfrTxtProcessing.get_raw_goods_txt)

        return data


    def __process_data(self, data, img_func, txt_func):
        img = img_func(self.img)
        ocr_data = OCR.detect_data(img)

        txt_data = txt_func(' '.join(ocr_data['text']))
        if txt_data != None: data['text'].update(txt_data)

        data['imgs'].append(FfrImgProcessing.draw_boundary(img, ocr_data))