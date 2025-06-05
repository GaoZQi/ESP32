from PIL import Image
import random
import string

class SimpleScaleDownDecoder:
    def __init__(self):
        pass

    def extract_small_image(self, big_img, small_w, small_h):
        return big_img.resize((small_w, small_h), Image.NEAREST)

    def decode(self, img_path, dims):
        big_path = img_path
        output_path = 'output/DataEncode/' + random_string(8) + '.png'

        try:
            dims = dims.strip().split(' ')
            small_w, small_h = int(dims[0]), int(dims[1])
        except (ValueError, IndexError):
            print("[ERROR] Invalid size input. Please enter two integers.")
            return

        big_img = Image.open(big_path)
        result = self.extract_small_image(big_img, small_w, small_h)
        result.save(output_path)
        print(f"[+] Decoded image saved to: {output_path}")
        
        return output_path

def get_decoder():
    return SimpleScaleDownDecoder()

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))