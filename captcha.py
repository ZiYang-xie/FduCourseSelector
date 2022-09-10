#coding=UTF-8
import easyocr
import cv2
import io
import json
import numpy
import base64
from PIL import Image
from PIL import ImageEnhance


def read_captcha(img_byte, captcha_type='slide'):
    if captcha_type == 'slide':
        captcha_info = json.loads(img_byte)
        result = read_slide_captcha(captcha_info)
    elif captcha_type == 'img':
        result = read_slide_captcha(img_byte)
    else:
        raise NotImplementedError
    return result


def read_slide_captcha(captcha_info):
	SrcImg = Image.open(io.BytesIO(base64.b64decode(captcha_info['SrcImage'])))
	CutImg = Image.open(io.BytesIO(base64.b64decode(captcha_info['CutImage'])))
	SrcImg = cv2.cvtColor(numpy.array(SrcImg), cv2.COLOR_RGB2BGR)
	CutImg = cv2.cvtColor(numpy.array(CutImg), cv2.COLOR_RGB2BGR)
	bottom_right = _detect_displacement(SrcImg, CutImg)
	moveEnd_X = bottom_right[0]
	wbili = moveEnd_X / captcha_info['SrcImageWidth']
	return moveEnd_X, wbili

def _tran_canny(image):
	image = cv2.GaussianBlur(image, (3, 3), 0)
	return cv2.Canny(image, 50, 150)

def _detect_displacement(SrcImg, CutImg):
	# 寻找最佳匹配
	res = cv2.matchTemplate(_tran_canny(SrcImg), _tran_canny(CutImg), cv2.TM_CCOEFF_NORMED)
	# 最小值，最大值，并得到最小值, 最大值的索引
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

	bottom_right = min_loc
	return bottom_right

'''
[Archived] Recognize the Image CAPTCHA
'''
def read_img_captcha(img_byte):
	img = Image.open(io.BytesIO(img_byte)).convert('L')
	enh_bri = ImageEnhance.Brightness(img)
	new_img = enh_bri.enhance(factor=1.5)

	image = numpy.array(new_img)
	reader = easyocr.Reader(['en'])
	horizontal_list, free_list = reader.detect(image, optimal_num_chars=4)
	character = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	allow_list = list(character)
	allow_list.extend(list(character.lower()))

	result = reader.recognize(image, 
            	allowlist=allow_list,
            	horizontal_list=horizontal_list[0],
            	free_list=free_list[0],
            	detail = 0)
	return result[0]
