import cv2
from paddleocr import PaddleOCR
import numpy as np
import unicodedata as ud


class OcrLicense:
    def __init__(self) -> None:
        self.paddleocr_jp = PaddleOCR(use_angle_cls="False", lang="japan", show_log=False, det_db_unclip_ratio=2.2)
        self.paddleocr_en = PaddleOCR(use_angle_cls="False", lang="en", show_log=False)
        
    def containsNumber(self, str):
        for character in str:
            if character.isdigit():
                return True
        return False

    def convert_full_width(self, s):
        '''
        Convert all ASCII characters to the full-width counterpart.
        '''
        HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
        HALF2FULL[0x20] = 0x3000
        return str(s).translate(HALF2FULL)
        
    def is_latin(self, uchr):
        latin_letters= {}
        try: return latin_letters[uchr]
        except KeyError:
            return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

    def only_roman_chars(self, unistr):
        return all(self.is_latin(uchr)
            for uchr in unistr
            if uchr.isalpha())

    def crop_rect(self, img, box):
        # box[0][0] -= 5
        # box[1][0] += 5
        # box[2][0] += 5
        # box[3][0] -= 5
        cnt = np.array(box).astype(int)
        rect = cv2.minAreaRect(cnt)
        # get the parameter of the small rectangle
        center, size, angle = rect[0], rect[1], rect[2]
        center, size = tuple(map(int, center)), tuple(map(int, size))

        # get row and col num in img
        height, width = img.shape[0], img.shape[1]

        # calculate the rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1)
        # rotate the original image
        img_rot = cv2.warpAffine(img, M, (width, height))

        # now rotated rectangle becomes vertical, and we crop it
        img_crop = cv2.getRectSubPix(img_rot, size, center)
        if img_crop.shape[0] > img_crop.shape[1]:
            img_crop = cv2.rotate(img_crop, cv2.ROTATE_90_CLOCKWISE)

        return img_crop

    def inference_single(self, img_path, license_type):
        output = {"name":"", "address":""}
        img = cv2.imread(img_path)
        h, w, _ = img.shape
        img = cv2.resize(img, (int(w*1.2), int(h*1.2)), interpolation= cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(src=img, ksize=(3, 3), sigmaX=0, sigmaY=0)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(12, 12))
        img = clahe.apply(img)
        result = self.paddleocr_jp.ocr(img, det=True, cls=False)
        result = result[0]
        result = sorted(result)
        
        if license_type == "driver_license":
            for i in range(len(result)):
                ocr_res = result[i][1][0]
                box = result[i][0]
                if ("氏名" in ocr_res or "氏" in ocr_res or "名" in ocr_res) and (len(ocr_res) == 2):
                    mid_point = (box[0][1] + box[3][1]) / 2
                    for j in range(len(result)):
                        if i == j:
                            continue
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                            and result[j][0][1][0] < int(w-w/4)
                        ):
                            if self.only_roman_chars(result[j][1][0]):
                                img_crop = self.crop_rect(img, result[j][0])
                                result_crop = self.paddleocr_en.ocr(img_crop, det=False, cls=False)[0][0][0]
                                output["name"] += self.convert_full_width(result_crop)
                            else:
                                if not self.containsNumber(result[j][1][0]):
                                    output["name"] += self.convert_full_width(result[j][1][0])

                if ("住所" in ocr_res or "住" in ocr_res or "所" in ocr_res) and (len(ocr_res) == 2):
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                        ):
                            if self.only_roman_chars(result[j][1][0]):
                                img_crop = self.crop_rect(img, result[j][0])
                                result_crop = self.paddleocr_en.ocr(img_crop, det=False, cls=False)[0][0][0]
                                output["address"] += self.convert_full_width(result_crop)
                            else:
                                output["address"] += self.convert_full_width(result[j][1][0])
                if output["name"] != "" and output["address"] != "":
                    break

        if license_type == "my_number_card":
            for i in range(len(result)):
                ocr_res = result[i][1][0]
                box = result[i][0]
                if ("氏名" in ocr_res or "氏" in ocr_res or "名" in ocr_res) and (len(ocr_res) == 2):
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                            and result[j][0][0][0] < int(w-w/6)
                        ):
                            if self.only_roman_chars(result[j][1][0]):
                                img_crop = self.crop_rect(img, result[j][0])
                                result_crop = self.paddleocr_en.ocr(img_crop, det=False, cls=False)[0][0][0]
                                output["name"] += self.convert_full_width(result_crop)
                            else:
                                output["name"] += self.convert_full_width(result[j][1][0])

                if ("住所" in ocr_res or "住" in ocr_res or "所" in ocr_res) and (len(ocr_res) == 2):
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1] 
                            and mid_point < result[j][0][2][1] 
                            and result[j][0][0][0] < int(w-w/6)
                            and result[j][1][0] != "カード"
                        ):
                            if self.only_roman_chars(result[j][1][0]):
                                img_crop = self.crop_rect(img, result[j][0])
                                result_crop = self.paddleocr_en.ocr(img_crop, det=False, cls=False)[0][0][0]
                                output["address"] += self.convert_full_width(result_crop)
                            else:
                                output["address"] += self.convert_full_width(result[j][1][0])
                if output["name"] != "" and output["address"] != "":
                    break

        return output