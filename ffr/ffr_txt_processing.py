import re


class FfrTxtProcessing():

    # Regexes for detecting stuff in strings
    regex_num = r'\s*(\d+((,\d{3})*)?(\.\d+)?)'
   

    @staticmethod
    def get_date_info_txt(text):
        data = {}
        print(text)

        regex = r"(\d+):(\d+):(\d+)(am|pm)\D*(\d+)/(\d+)/(\d+)"
        match = re.search(regex, text)
        if match:
            data['hour']   = match.group(1)
            data['minute'] = match.group(2)
            data['second'] = match.group(3)
            data['ampm']   = match.group(4)
            data['month']  = match.group(5)
            data['day']    = match.group(6)
            data['year']   = match.group(7)

        return data


    @staticmethod
    def get_player_info_txt(text):
        data = {}
        print(text)

        regex = r"\[Lv\.\d+\]\s*(.*):"
        match = re.search(regex, text)
        if match:
            data['player'] = match.group(1)

        return data


    @staticmethod
    def get_map_title_txt(text):
        data = {}
        print(text)

        regex = r"[\s]*[\S]*[\s]*(.*)"
        match = re.search(regex, text)
        if match:
            data['title'] = match.group(1)

        return data


    @staticmethod
    def get_map_info_txt(text):
        data = {}
        print(text)

        regex = r"Difficulty:\D*(\d+)\D*Length:\D*(\d+):(\d+)\D*Artist:([^-]+)\D*Stepfile by:([^-]+)"
        match = re.search(regex, text)
        if match:
            data['difficulty'] = match.group(1)
            data['length_min'] = match.group(2)
            data['length_sec'] = match.group(3)
            data['artist']     = match.group(4)
            data['creator']    = match.group(5)

        return data


    @staticmethod
    def get_amazing_txt(text):
        data = {}
        print(text)

        regex = r"Amazing:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['amazing_score'] = match.group(1)

        return data


    @staticmethod
    def get_perfect_txt(text):
        data = {}
        print(text)

        regex = r"Perfect:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['perfect_score'] = match.group(1)

        return data


    @staticmethod
    def get_good_txt(text):
        data = {}
        print(text)

        regex = r"Good:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['good_score'] = match.group(1)

        return data


    @staticmethod
    def get_average_txt(text):
        data = {}
        print(text)

        regex = r"Average:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['average_score'] = match.group(1)

        return data


    @staticmethod
    def get_miss_txt(text):
        data = {}
        print(text)

        regex = r"Miss:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['miss_score'] = match.group(1)

        return data


    @staticmethod
    def get_boo_txt(text):
        data = {}
        print(text)

        regex = r"Boo:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['boo_score'] = match.group(1)

        return data

    
    @staticmethod
    def get_aaa_equiv_txt(text):
        data = {}
        print(text)

        regex = r"AAA Equivalency:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['AAA_equiv'] = match.group(1)

        return data


    @staticmethod
    def get_raw_goods_txt(text):
        data = {}
        print(text)

        regex = r"Raw Goods:" + FfrTxtProcessing.regex_num
        match = re.search(regex, text)
        if match:
            data['raw_goods'] = match.group(1)

        return data