import numpy as np
import cv2


class FfrImgProcessing():

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
        'raw_goods'   : [ 0.30, 0.35, 0.40, 0.65 ],
        'combo'       : [ 0.48, 0.53, 0.39, 0.64 ]
    }


    @staticmethod
    def get_date_info_img(img): 
        return FfrImgProcessing.__crop_img(img, 'date_info')


    @staticmethod
    def get_player_info_img(img):
        return FfrImgProcessing.__crop_img(img, 'player_info')


    @staticmethod
    def get_map_title_img(img):
        return FfrImgProcessing.__crop_img(img, 'map_title')


    @staticmethod
    def get_map_info_img(img):
        return FfrImgProcessing.__crop_img(img, 'map_info')


    @staticmethod
    def get_amazing_img(img):
        return FfrImgProcessing.__crop_img(img, 'amazing')


    @staticmethod
    def get_perfect_img(img):
        return FfrImgProcessing.__crop_img(img, 'perfect')


    @staticmethod
    def get_good_img(img):
        return FfrImgProcessing.__crop_img(img, 'good')


    @staticmethod
    def get_average_img(img):
        return FfrImgProcessing.__crop_img(img, 'average')


    @staticmethod
    def get_miss_img(img):
        return FfrImgProcessing.__crop_img(img, 'miss')


    @staticmethod
    def get_boo_img(img):
        target_width = 312
        target_height = 38

        img = FfrImgProcessing.__crop_img(img, 'boo')

        # height, width, number of channels in image
        height   = img.shape[0]
        width    = img.shape[1]

        # Enlarge image
        img = cv2.resize(img, (0,0), fx=target_width/width, fy=target_height/height, interpolation=cv2.INTER_NEAREST)
        return img


    @staticmethod
    def get_aaa_equiv_img(img):
        return FfrImgProcessing.__crop_img(img, 'aaa_equiv')


    @staticmethod
    def get_raw_goods_img(img):
        target_width = 312
        target_height = 38

        img = FfrImgProcessing.__crop_img(img, 'raw_goods')

        # height, width, number of channels in image
        height   = img.shape[0]
        width    = img.shape[1]

        # Enlarge image
        img = cv2.resize(img, (0,0), fx=target_width/width, fy=target_height/height, interpolation=cv2.INTER_NEAREST)
        return img


    @staticmethod
    def get_combo_img(img):
        target_width = 312
        target_height = 38

        img = FfrImgProcessing.__crop_img(img, 'combo')

        # height, width, number of channels in image
        height   = img.shape[0]
        width    = img.shape[1]

        # Enlarge image
        img = cv2.resize(img, (0,0), fx=target_width/width, fy=target_height/height, interpolation=cv2.INTER_NEAREST)
        return img


    @staticmethod
    def __crop_img(img, key):
        h1 = FfrImgProcessing.crop_info[key][0]
        h2 = FfrImgProcessing.crop_info[key][1]
        w1 = FfrImgProcessing.crop_info[key][2]
        w2 = FfrImgProcessing.crop_info[key][3]

        height = img.shape[0]
        width  = img.shape[1]

        return img[int(height*h1) : int(height*h2), int(width*w1) : int(width*w2)]


    @staticmethod
    def draw_boundary(img, data):
        new_img = img 

        # draw the bounding boxes on the image
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 10:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                new_img = cv2.rectangle(new_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return new_img