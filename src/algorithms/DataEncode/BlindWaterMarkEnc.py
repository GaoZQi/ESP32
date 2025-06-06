import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

class BlindWatermarkEncoder:
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

    def encode(self, fn1, fn2, fn3):
        print(f'image<{fn1}> + watermark<{fn2}> -> image(encoded)<{fn3}>')
        img = cv2.imread(fn1)
        wm = cv2.imread(fn2)
        if img is None:
            raise FileNotFoundError(f"can't find {fn1}")
        if wm is None:
            raise FileNotFoundError(f"can't find {fn2}")

        if self.debug:
            plt.subplot(231), plt.imshow(self.bgr_to_rgb(img)), plt.title('image')
            plt.xticks([]), plt.yticks([])
            plt.subplot(234), plt.imshow(self.bgr_to_rgb(wm)), plt.title('watermark')
            plt.xticks([]), plt.yticks([])

        h, w = img.shape[:2]
        hwm = np.zeros((int(h * 0.5), w, img.shape[2]))
        assert hwm.shape[0] > wm.shape[0]
        assert hwm.shape[1] > wm.shape[1]
        hwm2 = np.copy(hwm)
        for i in range(wm.shape[0]):
            for j in range(wm.shape[1]):
                hwm2[i][j] = wm[i][j]

        random.seed(self.seed, version=1 if self.oldseed else 2)
        m, n = list(range(hwm.shape[0])), list(range(hwm.shape[1]))
        if self.oldseed:
            self.old_shuffle(m)
            self.old_shuffle(n)
        else:
            random.shuffle(m)
            random.shuffle(n)

        for i in range(hwm.shape[0]):
            for j in range(hwm.shape[1]):
                hwm[i][j] = hwm2[m[i]][n[j]]

        rwm = np.zeros(img.shape)
        for i in range(hwm.shape[0]):
            for j in range(hwm.shape[1]):
                rwm[i][j] = hwm[i][j]
                rwm[-(i + 1)][-(j + 1)] = hwm[i][j]

        if self.debug:
            plt.subplot(235), plt.imshow(self.bgr_to_rgb(rwm)), plt.title('encrypted(watermark)')
            plt.xticks([]), plt.yticks([])

        f1 = np.fft.fft2(img)
        f2 = f1 + self.alpha * rwm
        _img = np.fft.ifft2(f2)
        img_wm = np.real(_img)

        cv2.imwrite(fn3, img_wm, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        img_wm2 = cv2.imread(fn3)
        diff = np.sum((img_wm - img_wm2) ** 2)
        miss = np.sqrt(diff) / (img_wm.size) * 100
        print(f'Miss {miss:.2f}% in save')

        if self.debug:
            plt.subplot(233), plt.imshow(self.bgr_to_rgb(np.uint8(img_wm))), plt.title('image(encoded)')
            plt.xticks([]), plt.yticks([])

        # 自动验证嵌入后的图中是否能取出水印
        f2 = np.fft.fft2(img_wm)
        rwm = (f2 - f1) / self.alpha
        rwm = np.real(rwm)
        wm_restore = np.zeros(rwm.shape)
        for i in range(int(rwm.shape[0] * 0.5)):
            for j in range(rwm.shape[1]):
                wm_restore[m[i]][n[j]] = np.uint8(rwm[i][j])
        for i in range(int(rwm.shape[0] * 0.5)):
            for j in range(rwm.shape[1]):
                wm_restore[-(i + 1)][-(j + 1)] = wm_restore[i][j]

        if self.debug:
            cv2.imwrite('_bwm.debug.wm.jpg', wm_restore)
            plt.subplot(236), plt.imshow(self.bgr_to_rgb(wm_restore)), plt.title('watermark')
            plt.xticks([]), plt.yticks([])
            plt.show()

class EncoderAdapter:
    def encode(self, origin_file, hide_file):
        out_path = origin_file.split('/')[-1]
        encoder = BlindWatermarkEncoder()
        encoder.encode(origin_file, hide_file, out_path)

def get_encoder():
    return EncoderAdapter()

if __name__ == '__main__':
    encoder = get_encoder()
    encoder.encode('C:/Users/12814/Downloads/1.png', 'C:/Users/12814/Downloads/2.png')