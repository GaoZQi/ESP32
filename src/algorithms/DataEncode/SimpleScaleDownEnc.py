from PIL import Image
import random
import string

class SimpleScaleDownEncoder:
    def __init__(self):
        pass

    def my_nearest_resize(self, big_img, small_img):
        big_w, big_h = big_img.size
        small_w, small_h = small_img.size

        dst_im = big_img.copy()

        stepx = big_w / small_w
        stepy = big_h / small_h

        for i in range(small_w):
            for j in range(small_h):
                map_x = int(i * stepx + stepx * 0.5)
                map_y = int(j * stepy + stepy * 0.5)

                if map_x < big_w and map_y < big_h:
                    dst_im.putpixel((map_x, map_y), small_img.getpixel((i, j)))

        return dst_im

    def encode(self, big_path, small_path):
        output_path = random_string(8) + '.png'

        big_img = Image.open(big_path)
        small_img = Image.open(small_path)

        result = self.my_nearest_resize(big_img, small_img)
        result.save(output_path)

        small_w, small_h = small_img.size
        print(f"[+] Encoded image saved to: {output_path}")
        print(f"[INFO] Please remember the embedded small image size: width={small_w}, height={small_h}")
        
        return output_path

def get_encoder():
    return SimpleScaleDownEncoder()

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))