import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

class BlindWatermarkDecoder:
    def __init__(self, seed=20160930, oldseed=False, alpha=3.0, debug=False):
        self.seed = seed
        self.oldseed = oldseed
        self.alpha = alpha
        self.debug = debug

    def bgr_to_rgb(self, img):
        b, g, r = cv2.split(img)
        return cv2.merge([r, g, b])

    def old_shuffle(self, x):
        for i in reversed(range(1, len(x))):
            j = int(random.random() * (i + 1))
            x[i], x[j] = x[j], x[i]

    def decode(self, fn1, fn2, fn3):
        print(f'image<{fn1}> + image(encoded)<{fn2}> -> watermark<{fn3}>')
        img = cv2.imread(fn1)
        img_wm = cv2.imread(fn2)
        if img is None:
            raise FileNotFoundError(f"can't find {fn1}")
        if img_wm is None:
            raise FileNotFoundError(f"can't find {fn2}")

        if self.debug:
            plt.subplot(231), plt.imshow(self.bgr_to_rgb(img)), plt.title('image')
            plt.xticks([]), plt.yticks([])
            plt.subplot(234), plt.imshow(self.bgr_to_rgb(img_wm)), plt.title('image(encoded)')
            plt.xticks([]), plt.yticks([])

        h, w = img.shape[:2]
        random.seed(self.seed, version=1 if self.oldseed else 2)
        m, n = list(range(int(h * 0.5))), list(range(w))
        if self.oldseed:
            self.old_shuffle(m)
            self.old_shuffle(n)
        else:
            random.shuffle(m)
            random.shuffle(n)

        f1 = np.fft.fft2(img)
        f2 = np.fft.fft2(img_wm)
        rwm = (f2 - f1) / self.alpha
        rwm = np.real(rwm)

        if self.debug:
            plt.subplot(232), plt.imshow(self.bgr_to_rgb(np.real(f1))), plt.title('fft(image)')
            plt.subplot(235), plt.imshow(self.bgr_to_rgb(np.real(f2))), plt.title('fft(image(encoded))')
            plt.subplot(233), plt.imshow(self.bgr_to_rgb(rwm)), plt.title('encrypted(watermark)')
            plt.xticks([]), plt.yticks([])

        wm = np.zeros(rwm.shape)
        for i in range(int(rwm.shape[0] * 0.5)):
            for j in range(rwm.shape[1]):
                wm[m[i]][n[j]] = np.uint8(rwm[i][j])
        for i in range(int(rwm.shape[0] * 0.5)):
            for j in range(rwm.shape[1]):
                wm[-(i + 1)][-(j + 1)] = wm[i][j]

        cv2.imwrite(fn3, wm)

        if self.debug:
            plt.subplot(236), plt.imshow(self.bgr_to_rgb(wm)), plt.title('watermark')
            plt.xticks([]), plt.yticks([])
            plt.show()

class DecoderAdapter:
    def decode(self, origin_file, hide_file):
        out_path = 'output/DataEncode/' + origin_file.split('/')[-1]
        decoder = BlindWatermarkDecoder()
        decoder.decode(origin_file, hide_file, out_path)

def get_decoder():
    return DecoderAdapter()