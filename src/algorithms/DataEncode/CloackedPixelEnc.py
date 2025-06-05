import sys
import struct
import os
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from PIL import Image
import random
import string

class AESCipher:
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw: bytes) -> bytes:
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc: bytes) -> bytes:
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s: bytes) -> bytes:
        pad_len = self.bs - len(s) % self.bs
        return s + bytes([pad_len] * pad_len)

    @staticmethod
    def _unpad(s: bytes) -> bytes:
        return s[:-s[-1]]

class CloackedPixelEncoder:
    def __init__(self):
        pass

    def decompose(self, data: bytes):
        v = []
        f_size = len(data)
        bytes_data = list(struct.pack("i", f_size)) + list(data)
        for b in bytes_data:
            for i in range(7, -1, -1):
                v.append((b >> i) & 0x1)
        return v

    def set_bit(self, n, i, x):
        mask = 1 << i
        n &= ~mask
        if x:
            n |= mask
        return n

    def encode(self, payload, password, img_file):
        img_file = img_file
        data = payload.encode()
        password = password
        out_file = 'output/DataEncode/' + random_string(8) + '.png'

        img = Image.open(img_file).convert("RGBA")
        width, height = img.size
        pixels = list(img.getdata())
        print(f"[*] Input image size: {width}x{height} pixels.")

        max_size = width * height * 3.0 / 8 / 1024
        print(f"[*] Usable payload size: {max_size:.2f} KB.")

        # with open(payload, "rb") as f:
        #     data = f.read()
        print(f"[+] Payload size: {len(data) / 1024.0:.3f} KB")

        cipher = AESCipher(password)
        data_enc = cipher.encrypt(data)
        v = self.decompose(data_enc)

        while len(v) % 3:
            v.append(0)

        payload_size = len(v) / 8 / 1024.0
        print(f"[+] Encrypted payload size: {payload_size:.3f} KB")

        if payload_size > max_size - 4:
            print("[-] Cannot embed. File too large")
            return

        steg_pixels = []
        idx = 0
        for pixel in pixels:
            r, g, b, a = pixel
            if idx < len(v):
                r = self.set_bit(r, 0, v[idx])
                g = self.set_bit(g, 0, v[idx + 1])
                b = self.set_bit(b, 0, v[idx + 2])
                idx += 3
            steg_pixels.append((r, g, b, a))

        steg_img = Image.new("RGBA", (width, height))
        steg_img.putdata(steg_pixels)
        steg_img.save(out_file, "PNG")
        print(f"[+] {payload} embedded successfully into {out_file}!")
        
        return out_file

def get_encoder():
    return CloackedPixelEncoder()

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))