from PIL import Image
from tqdm import tqdm
import random
import string

class PeanoQRRestorer:
    def __init__(self, image_path: str, peano_order: int = 6):
        """
        Initialize the Peano QR restorer.
        :param image_path: Path to the distorted QR code image
        :param peano_order: Order of the Peano curve used to scramble
        """
        self.image_path = image_path
        self.peano_order = peano_order
        self.img = Image.open(image_path).convert("RGB")
        self.width, self.height = self.img.size
        self.order = self._generate_peano(peano_order)

    def _generate_peano(self, n):
        """
        Recursively generate the Peano curve coordinate sequence
        """
        if n == 0:
            return [[0, 0]]
        else:
            in_lst = self._generate_peano(n - 1)
            lst = in_lst.copy()
            px, py = lst[-1]
            lst.extend([[px - i[0], py + 1 + i[1]] for i in in_lst])
            px, py = lst[-1]
            lst.extend([[px + i[0], py + 1 + i[1]] for i in in_lst])
            px, py = lst[-1]
            lst.extend([[px + 1 + i[0], py - i[1]] for i in in_lst])
            px, py = lst[-1]
            lst.extend([[px - i[0], py - 1 - i[1]] for i in in_lst])
            px, py = lst[-1]
            lst.extend([[px + i[0], py - 1 - i[1]] for i in in_lst])
            px, py = lst[-1]
            lst.extend([[px + 1 + i[0], py + i[1]] for i in in_lst])
            px, py = lst[-1]
            lst.extend([[px - i[0], py + 1 + i[1]] for i in in_lst])
            px, py = lst[-1]
            lst.extend([[px + i[0], py + 1 + i[1]] for i in in_lst])
            return lst

    def restore(self, save_path: str = None):
        """
        Restore the image from a Peano-scrambled version.
        :param save_path: Optional output path for restored image
        :return: Restored PIL.Image object
        """
        new_img = Image.new("RGB", (self.width, self.height))

        for i, (x, y) in tqdm(enumerate(self.order), total=len(self.order), desc="Restoring"):
            new_x, new_y = i % self.width, i // self.width
            if new_y >= self.height:
                break
            pixel = self.img.getpixel((x, self.height - 1 - y))
            new_img.putpixel((new_x, new_y), pixel)

        if save_path:
            new_img.save(save_path)
            print(f"[+] Restored image saved to: {save_path}")
        return new_img

class PeanoDecoderAdapter:
    def decode(self, path):
        input_path = path
        print(input_path)
        output_path = input_path.split('/')[-1].replace('.png', '_restore.png')

        restorer = PeanoQRRestorer(image_path=input_path, peano_order=6)
        restorer.restore(save_path=output_path)
        
        return output_path

def get_decoder():
    return PeanoDecoderAdapter()

# def random_string(length):
#     return ''.join(random.choices(string.ascii_letters, k=length))