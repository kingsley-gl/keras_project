from PIL import Image
from PIL import ImageFilter
import numpy as np
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import shutil

np.set_printoptions(threshold=np.inf)

cut_array_list = []


class ImgProcess(object):
    def __init__(self, img_path):
        self.img = Image.open(img_path)
        self.binary_threshold = 155
        self.array = None

    def _img_binaryzation(self):
        '''
        二值化
        :return:
        '''
        img = self.img

        img = img.filter(ImageFilter.SMOOTH)
        img = img.filter(ImageFilter.CONTOUR)
        img = img.filter(ImageFilter.SHARPEN)

        img = img.convert('L')

        table = []

        for i in range(256):
            if i < self.binary_threshold:
                table.append(0)
            else:
                table.append(1)
        img = img.point(table, '1')

        self.img = img
        self.array = np.array(self.img)
        # print(self.array)
        # img = Image.fromarray(self.array, mode='L')
        # img.show()

    def _white_cut(self, array):
        '''
        白边裁剪
        :return:
        '''
        top = 0
        bottom = 0
        left = 0
        right = 0
        (row, col) = array.shape
        for top_row in range(0, row):
            if array.sum(axis=1)[top_row, ...] != 1 * col:
                top = top_row
                break

        for bottom_row in range(row - 1, 0, -1):
            if array.sum(axis=1)[bottom_row, ...] != 1 * col:
                bottom = bottom_row
                break

        for left_col in range(0, col):
            if array.sum(axis=0)[..., left_col] != 1 * row:
                left = left_col
                break

        for right_col in range(col - 1, 0, -1):
            if array.sum(axis=0)[..., right_col] != 1 * row:
                right = right_col
                break

        # img = Image.fromarray(array[top: bottom + 1, left: right + 1], mode='L')
        # img.show()
        return array[top: bottom + 1, left: right + 1]
        # print(array * 255)

    def _cal_cut_col(self, source_array):
        '''
        裁剪
        :param source_array:
        :return:
        '''
        try:
            (rows, cols) = source_array.shape
            cut_col = 0
            flag = True
            for col in range(cols):
                if source_array.sum(axis=0)[..., col] == 1 * rows:
                    cut_col = col
                    break

            array_1 = source_array[..., 0: cut_col]
            array_2 = source_array[..., cut_col + 1:]
            # print('a1:',  array_1.shape)
            # print('a2:', array_2.shape)

            if array_1.shape[1] == 0:
                flag = False
                array_1 = array_2

            if array_1.shape[1] == 0:
                return False, array_1

            cut_array_list.append(array_1)
            # self._save(array_1)

            return flag, array_2
        except Exception as e:
            print(e)
            raise e

    # @staticmethod
    # def _save(array):
    #     with Image.fromarray(array, mode='L') as image:
    #         image.save(f'./cut_code/{int(time.mktime(datetime.datetime.now().timetuple()))}.jpg')

    def _img_cut(self):
        '''
        单字裁剪
        :return:
        '''
        CUT_BREAK = True

        array = self.array
        while CUT_BREAK:
            CUT_BREAK, array = self._cal_cut_col(array)
            array = self._white_cut(array)

        # img = Image.fromarray(array, mode='L')
        # img.show()

    def __call__(self, *args, **kwargs):
        self._img_binaryzation()
        self.array = self._white_cut(self.array)
        self._img_cut()
        # print('%s done !' % args[0])


def run():
    img_path = []

    for img in os.listdir('./check_code'):
        img_path.append(ImgProcess('/'.join(['./check_code', img])))

    for p in img_path:
        p()

    for index, pic in enumerate(cut_array_list):
        Image.fromarray(pic).save(f'./cut_code/{index}.jpg')


def classify_useless_code():
    move_img_list = []
    for cut_img in os.listdir('./cut_code'):
        if cut_img != 'useless_code':
            with Image.open('/'.join(['./cut_code', cut_img])) as i:
                print(i)
                if i.size[0] > 30 or i.size[0] <= 2:
                    move_img_list.append(cut_img)
                i = i.resize((25, 25), Image.ANTIALIAS)
                i.save('/'.join(['./cut_code', cut_img]))
    if len(move_img_list) > 0:
        for move_img in move_img_list:
            shutil.move('/'.join(['./cut_code', move_img]), '/'.join(['./cut_code/useless_code', move_img]))


classify_useless_code()
