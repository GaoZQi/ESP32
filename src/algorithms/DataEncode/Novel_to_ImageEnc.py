# enc.py
from PIL import Image
import math
import os
import random
import string

class NovelToImageEncoder:
    def __init__(self):
        pass

    def encode(self, text):
        # filename = input("Enter text file path: ").strip()
        output_path = 'output/DataEncode/' + random_string(8) + '.bmp'

        # try:
        #     # 优先尝试 utf-8 编码读取文本
        #     try:
        #         with open(filename, encoding="utf-8") as f:
        #             text = f.read()
        #     except UnicodeDecodeError:
        #         with open(filename, encoding="gbk") as f:
        #             text = f.read()
        # except Exception as e:
        #     print(f"[ERROR] Failed to read file: {e}")
        #     return

        str_len = len(text)
        width = math.ceil(str_len ** 0.5)
        im = Image.new("RGB", (width, width), 0x0)

        x, y = 0, 0
        for i in text:
            index = ord(i)
            rgb = (0, (index & 0xFF00) >> 8, index & 0xFF)
            im.putpixel((x, y), rgb)
            if x == width - 1:
                x = 0
                y += 1
            else:
                x += 1

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        im.save(output_path)
        print(f"[+] Encoded image saved to: {output_path}")
        
        return output_path

def get_encoder():
    return NovelToImageEncoder()

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))