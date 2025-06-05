from PIL import Image
import os

class NovelToImageDecoder:
    def __init__(self):
        pass

    def decode(self, filename):
        # filename = input("Enter encoded image path: ").strip()
        # output_path = 'output/DataEncode/' + random_string(8) + '.bmp'
        # encoding = input("Enter output encoding (utf-8 or gbk): ").strip().lower()

        try:
            im = Image.open(filename)
        except Exception as e:
            print(f"[ERROR] Cannot open image: {e}")
            return

        width, height = im.size
        chars = []
        for y in range(height):
            for x in range(width):
                r, g, b = im.getpixel((x, y))
                if (r | g | b) == 0:
                    break
                index = (g << 8) + b
                chars.append(chr(index))

        decoded_text = ''.join(chars)
        # output_dir = os.path.dirname(output_path)
        # if output_dir and not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        # try:
        #     with open(output_path, "w", encoding=encoding) as f:
        #         f.write(decoded_text)
        #     print(f"[+] Decoded text saved to: {output_path}")
        # except Exception as e:
        #     print(f"[ERROR] Failed to save decoded text: {e}")
        
        return decoded_text

def get_decoder():
    return NovelToImageDecoder()