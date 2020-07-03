import numpy as np
import cv2
import re

from ocr import OCR


class Ffr():

    # Crop dimensions expressed as % of width and height
    crop_info = {
        'date_info'   : [ 0.03, 0.07, 0.75, 1.00 ],
        'player_info' : [ 0.03, 0.07, 0.03, 0.35 ],
        'map_title'   : [ 0.12, 0.17, 0.20, 0.90 ],
        'map_info'    : [ 0.16, 0.23, 0.20, 0.90 ],
        'amazing'     : [ 0.24, 0.30, 0.05, 0.25 ],
        'perfect'     : [ 0.29, 0.35, 0.05, 0.25 ],
        'good'        : [ 0.36, 0.40, 0.05, 0.25 ],
        'average'     : [ 0.42, 0.47, 0.05, 0.25 ],
        'miss'        : [ 0.48, 0.52, 0.05, 0.25 ],
        'boo'         : [ 0.54, 0.58, 0.05, 0.25 ],
        'aaa_equiv'   : [ 0.25, 0.30, 0.35, 0.60 ],
        'raw_goods'   : [ 0.30, 0.35, 0.40, 0.65 ]
    }

    # The game area w:h ratio
    ratio = 1.6254901960784313725490196078431

    # Constants to access rgb channels
    red   = 0
    green = 1
    blue  = 2

    # Regexes for detecting stuff in strings
    regex_num = r'\s*(\d+((,\d{3})*)?(\.\d+)?)'
    
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
            new_width = Ffr.ratio*height
            black_bar_width = (width - new_width)/2

            # If statement guard against window title bar
            if black_bar_width > 0:
                img = img[:, int(black_bar_width) : int(width - black_bar_width)]
        else:
            new_height = width/Ffr.ratio
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
            new_height = width/Ffr.ratio
            title_bar_height = height - new_height
            img = img[int(title_bar_height):, :]

        # height, width, number of channels in image
        self.height   = img.shape[0]
        self.width    = img.shape[1]
        self.channels = img.shape[2]

        # Filter out unwanted background color
        r_treshold = (0 <= img[:, :, Ffr.red]) & (img[:, :, Ffr.red] <= 60)
        g_treshold = (0 <= img[:, :, Ffr.green]) & (img[:, :, Ffr.green] <= 60)
        b_treshold = (0 <= img[:, :, Ffr.blue])  & (img[:, :, Ffr.blue] <= 60)
        img[r_treshold & g_treshold & b_treshold] = 0

        self.img = img


    def get_date_info_img(self): return self.__get_info_img('date_info')
    def get_player_info_img(self): return self.__get_info_img('player_info')
    def get_map_title_img(self): return self.__get_info_img('map_title')
    def get_map_info_img(self): return self.__get_info_img('map_info')
    def get_amazing_img(self): return self.__get_info_img('amazing')
    def get_perfect_img(self): return self.__get_info_img('perfect')
    def get_good_img(self): return self.__get_info_img('good')
    def get_average_img(self): return self.__get_info_img('average')
    def get_miss_img(self): return self.__get_info_img('miss')
    def get_boo_img(self): return self.__get_info_img('boo')
    def get_aaa_equiv_img(self): return self.__get_info_img('aaa_equiv')
    def get_raw_goods_img(self): return self.__get_info_img('raw_goods')


    @staticmethod
    def draw_boundary(img, data):
        new_img = img 

        # draw the bounding boxes on the image
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 10:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                new_img = cv2.rectangle(new_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return new_img


    def process_image(self):
        img_data = {
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

        img = self.get_date_info_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"(\d+):(\d+):(\d+)(am|pm)\D*(\d+)/(\d+)/(\d+)", ' '.join(data['text']))
        if match: 
            img_data['text']['hour']   = match.group(1)
            img_data['text']['minute'] = match.group(2)
            img_data['text']['second'] = match.group(3)
            img_data['text']['ampm']   = match.group(4)
            img_data['text']['month']  = match.group(5)
            img_data['text']['day']    = match.group(6)
            img_data['text']['year']   = match.group(7)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_player_info_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"\[Lv\.\d+\]\s*(.*):", ' '.join(data['text']))
        if match: img_data['text']['player'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_map_title_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"[\s]*[\S]*[\s]*(.*)", ' '.join(data['text']))
        if match: img_data['text']['title'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_map_info_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Difficulty:\D*(\d+)\D*Length:\D*(\d+):(\d+)\D*Artist:([^-]+)\D*Stepfile by:([^-]+)", ' '.join(data['text']))
        if match:
            img_data['text']['difficulty'] = match.group(1)
            img_data['text']['length_min'] = match.group(2)
            img_data['text']['length_sec'] = match.group(3)
            img_data['text']['artist']     = match.group(4)
            img_data['text']['creator']    = match.group(5)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_amazing_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Amazing:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['amazing_score'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_perfect_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Perfect:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['perfect_score'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_good_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Good:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['good_score'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_average_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Average:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['average_score'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_miss_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Miss:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['miss_score'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_boo_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Boo:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['miss_score'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_aaa_equiv_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"AAA Equivalency:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['AAA_equiv'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        img = self.get_raw_goods_img()
        data = OCR.detect_data(img)
        print(' '.join(data['text']))
        match = re.search(r"Raw Goods:" + Ffr.regex_num, ' '.join(data['text']))
        if match: img_data['text']['raw_goods'] = match.group(1)
        img_data['imgs'].append(Ffr.draw_boundary(img, data))

        return img_data


    def __get_info_img(self, key):
        h1 = Ffr.crop_info[key][0]
        h2 = Ffr.crop_info[key][1]
        w1 = Ffr.crop_info[key][2]
        w2 = Ffr.crop_info[key][3]

        return self.img[int(self.height*h1) : int(self.height*h2), int(self.width*w1) : int(self.width*w2)]