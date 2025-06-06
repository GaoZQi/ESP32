import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
from tqdm import tqdm
import string
import random

class PeanoQRGenerator:
    def __init__(self, 
                 data: str,
                 size: int = 729,
                 fill_color: str = 'black',
                 back_color: str = 'white',
                 logo_path: str = None):
        """
        Initialize the QR code generator.
        :param data: Text to encode
        :param size: Output image size (square)
        :param fill_color: Color of the QR modules
        :param back_color: Background color
        :param logo_path: Optional logo image path
        """
        self.data = data
        self.size = size
        self.fill_color = fill_color
        self.back_color = back_color
        self.logo_path = logo_path
        self.qr_image = None

    def _create_qr_image(self):
        """
        Generate a centered QR code with optional logo.
        """
        version = 1
        border = 0

        while version <= 40:
            try:
                qr = qrcode.QRCode(
                    version=version,
                    error_correction=ERROR_CORRECT_H,
                    box_size=1,
                    border=border
                )
                qr.add_data(self.data)
                qr.make(fit=True)

                matrix_size = len(qr.modules)
                box_size = self.size // (matrix_size + 2 * border)

                if box_size > 0:
                    qr = qrcode.QRCode(
                        version=version,
                        error_correction=ERROR_CORRECT_H,
                        box_size=box_size,
                        border=border
                    )
                    qr.add_data(self.data)
                    qr.make(fit=True)

                    qr_image = qr.make_image(fill_color=self.fill_color, back_color=self.back_color).convert('RGB')
                    qr_size = qr_image.size[0]

                    if self.logo_path:
                        try:
                            logo = Image.open(self.logo_path).convert("RGBA")
                            logo_size = qr_size // 4
                            logo = logo.resize((logo_size, logo_size))
                            pos = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)
                            qr_image.paste(logo, pos, logo)
                        except Exception as e:
                            print(f"[!] Failed to insert logo: {e}")

                    final_image = Image.new("RGB", (self.size, self.size), self.back_color)
                    paste_x = (self.size - qr_size) // 2
                    paste_y = (self.size - qr_size) // 2
                    final_image.paste(qr_image, (paste_x, paste_y))

                    self.qr_image = final_image
                    return final_image
                version += 1
            except qrcode.exceptions.DataOverflowError:
                version += 1
        raise ValueError(f"Failed to generate a {self.size}px QR code. Data may be too long.")

    def _peano(self, n):
        """
        Recursively generate Peano curve coordinates.
        """
        if n == 0:
            return [[0, 0]]
        else:
            in_lst = self._peano(n - 1)
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

    def apply_peano(self, peano_order_num=6, save_path=None):
        """
        Apply Peano curve pixel rearrangement.
        :param peano_order_num: Peano curve order
        :param save_path: Optional save path
        :return: Transformed image object
        """
        if self.qr_image is None:
            self._create_qr_image()

        width, height = self.qr_image.size
        order = self._peano(peano_order_num)
        new_img = Image.new("RGB", (width, height))

        for i, (x, y) in tqdm(enumerate(order), total=len(order), desc="Peano transforming"):
            new_x, new_y = i % width, i // width
            if new_y >= height:
                break
            pixel = self.qr_image.getpixel((new_x, new_y))
            new_img.putpixel((x, height - 1 - y), pixel)

        if save_path:
            new_img.save(save_path)
            print(f"[+] Distorted QR code saved to: {save_path}")

        return new_img

    def save_qr_image(self, save_path):
        """
        Save the clean QR code image.
        :param save_path: File path to save
        """
        if self.qr_image is None:
            self._create_qr_image()
        self.qr_image.save(save_path)
        print(f"[+] Clean QR code saved to: {save_path}")

class PeanoEncoderAdapter:
    def encode(self, text):
        output_path = random_string(8) + '.png'
        qr = PeanoQRGenerator(
            data=text,
            size=729,
            fill_color="black",
            back_color="white",
            logo_path=None
        )
        qr.save_qr_image(output_path.replace(".png", "_clean.png"))
        qr.apply_peano(peano_order_num=6, save_path=output_path)
        
        return output_path

def get_encoder():
    return PeanoEncoderAdapter()

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))