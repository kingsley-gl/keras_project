from keras import layers
import os
import numpy as np
from PIL import Image, ImageFilter


def classification_code():
    pass


def get_data_set():
    data_set = []
    for cut_img in os.listdir('./cut_code'):
        if cut_img != 'useless_code':
            with Image.open('/'.join(['./cut_code', cut_img])) as i:
                i = i.filter(ImageFilter.SMOOTH)
                i = i.filter(ImageFilter.CONTOUR)
                i = i.filter(ImageFilter.SHARPEN)
                i = i.convert('L')
                table = []

                for j in range(256):
                    if j < 155:
                        table.append(0)
                    else:
                        table.append(1)
                i = i.point(table, '1')
                data_set.append(np.array(i, dtype='uint8'))
    return data_set


get_data_set()
