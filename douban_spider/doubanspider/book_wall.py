# encoding:utf-8
"""豆瓣图书9分绑定图片墙"""

import os
import math

from PIL import Image


def generate_books_wall():
    """
    生成图书墙
    """
    curr_path = os.path.dirname(__file__)  # 当前文件文件夹所在目录
    parent_path = os.path.dirname(curr_path)  # 上层目录
    image_path = os.path.join(parent_path, 'books', 'full')
    images = os.listdir(image_path)
    size = int(math.sqrt(len(images)))
    default_width = 120
    default_height = 140
    width = size * default_width
    height = size * default_height
    image = Image.new('RGBA', (width, height))
    row = 0
    column = 0
    for image_name in images:
        try:
            img = Image.open(os.path.join(image_path, image_name))
        except IOError:
            pass
        else:
            img = img.resize((default_width, default_height), Image.ANTIALIAS)
            image.paste(img, (row * default_width, column * default_height))
            column += 1  #列数增加
            if column == size:  #当每行粘贴了指定size时换行粘贴
                column = 0
                row += 1
            if row * column > size * size:
                break

    image = image.convert("RGB")
    target_path = os.path.join(image_path, 'all.jpg')
    image.save(target_path)
    image.show()


if __name__ == "__main__":
    generate_books_wall()
