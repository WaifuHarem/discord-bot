import pytesseract

from config import tesseract_path



class OCR():

    # See: https://stackoverflow.com/a/52231794/3256177
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    @staticmethod
    def detect_data(img):
        # run tesseract, returning recognized data
        custom_config = r'--psm 6'
        return pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)