import sys
import struct
import os
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from PIL import Image

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

class CloackedPixelDecoder:
    def __init__(self):
        pass

    def assemble(self, v):
        byte_array = bytearray()
        for idx in range(0, len(v) // 8):
            byte = 0
            for i in range(8):
                byte = (byte << 1) | v[idx * 8 + i]
            byte_array.append(byte)
        payload_size = struct.unpack("i", byte_array[:4])[0]
        return bytes(byte_array[4: 4 + payload_size])

    def decode(self, password, in_file):
        # in_file = input("Enter stego image path: ").strip()
        out_file = 'output/DataEncode/' + in_file.split(in_file)[-1].split('.')[0] + '.png'
        # password = input("Enter password: ").strip()

        img = Image.open(in_file).convert("RGBA")
        width, height = img.size
        pixels = list(img.getdata())
        print(f"[+] Image size: {width}x{height} pixels.")

        v = []
        for pixel in pixels:
            r, g, b, a = pixel
            v.append(r & 1)
            v.append(g & 1)
            v.append(b & 1)

        data_enc = self.assemble(v)
        cipher = AESCipher(password)
        try:
            data_dec = cipher.decrypt(data_enc)
        except ValueError:
            print("[-] Decryption failed. Possibly wrong password or corrupted data.")
            return

        # with open(out_file, "wb") as f:
        #     f.write(data_dec)
        # print(f"[+] Written extracted data to {out_file}.")
        
        return data_dec

def get_decoder():
    return CloackedPixelDecoder()