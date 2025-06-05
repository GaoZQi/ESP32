from PIL import Image
import math
import os
import random
import string

class GilbertEncoder:
    def __init__(self):
        pass

    def gilbert2d(self, width, height):
        coordinates = []

        def generate2d(x, y, ax, ay, bx, by, coords):
            w = abs(ax + ay)
            h = abs(bx + by)

            dax = int(math.copysign(1, ax)) if ax != 0 else 0
            day = int(math.copysign(1, ay)) if ay != 0 else 0
            dbx = int(math.copysign(1, bx)) if bx != 0 else 0
            dby = int(math.copysign(1, by)) if by != 0 else 0

            if h == 1:
                for _ in range(w):
                    coords.append((x, y))
                    x += dax
                    y += day
                return

            if w == 1:
                for _ in range(h):
                    coords.append((x, y))
                    x += dbx
                    y += dby
                return

            ax2 = ax // 2
            ay2 = ay // 2
            bx2 = bx // 2
            by2 = by // 2

            w2 = abs(ax2 + ay2)
            h2 = abs(bx2 + by2)

            if 2 * w > 3 * h:
                if (w2 % 2) and (w > 2):
                    ax2 += dax
                    ay2 += day
                generate2d(x, y, ax2, ay2, bx, by, coords)
                generate2d(x + ax2, y + ay2, ax - ax2, ay - ay2, bx, by, coords)
            else:
                if (h2 % 2) and (h > 2):
                    bx2 += dbx
                    by2 += dby
                generate2d(x, y, bx2, by2, ax2, ay2, coords)
                generate2d(x + bx2, y + by2, ax, ay, bx - bx2, by - by2, coords)
                generate2d(
                    x + (ax - dax) + (bx2 - dbx),
                    y + (ay - day) + (by2 - dby),
                    -bx2, -by2,
                    -(ax - ax2), -(ay - ay2),
                    coords
                )

        if width >= height:
            generate2d(0, 0, width, 0, 0, height, coordinates)
        else:
            generate2d(0, 0, 0, height, width, 0, coordinates)

        return coordinates

    def encode(self, file):
        input_path = file
        output_path = 'output/DataEncode/' + random_string(8) + '.png'

        try:
            img = Image.open(input_path)
        except Exception as e:
            print(f"[ERROR] Cannot open image: {e}")
            return

        width, height = img.size
        pixels = img.convert("RGBA").load()

        curve = self.gilbert2d(width, height)
        total = width * height
        offset = round((math.sqrt(5) - 1) / 2 * total)

        new_img = Image.new("RGBA", (width, height))
        new_pixels = new_img.load()

        for i in range(total):
            x_old, y_old = curve[i]
            x_new, y_new = curve[(i + offset) % total]
            new_pixels[x_new, y_new] = pixels[x_old, y_old]

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        new_img.save(output_path)
        print(f"[+] Encrypted image saved to: {output_path}")
        
        return output_path

def get_encoder():
    return GilbertEncoder()

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))