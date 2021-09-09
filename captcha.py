#coding=UTF-8
import easyocr
import io
import numpy
from PIL import Image

def read_captcha(img_byte):
    image = numpy.array(Image.open(io.BytesIO(img_byte)))
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image, detail = 0)
    return result[0]