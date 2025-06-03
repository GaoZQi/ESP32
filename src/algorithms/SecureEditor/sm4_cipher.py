from .base import Cipher
from .utils import pkcs7_padding, pkcs7_unpadding, xor_bytes

# SM4 S盒
Sbox = [
    0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7,
    0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
    0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3,
    0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a,
    0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
    0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95,
    0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
    0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba,
    0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
    0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b,
    0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
    0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2,
    0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
    0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52,
    0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
    0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5,
    0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
    0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55,
    0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
    0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60,
    0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
    0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f,
    0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
    0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f,
    0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
    0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd,
    0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
    0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e,
    0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
    0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20,
    0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48
]

# 系统参数 FK
FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]

# 固定参数 CK
CK = [
    0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
    0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
    0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
    0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
    0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
    0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
    0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
    0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279
]

class SM4(Cipher):
    def __init__(self, iv: bytes, key: bytes):
        self.iv = iv
        self.Sbox = Sbox
        self.FK = FK
        self.CK = CK
        self.round_keys = self._key_expansion(key)

    def _tau(self, B: int) -> int:
        """
        对输入 B 进行 Sbox 变换，返回 32 位整数

        :param B: 输入的 32 位整数
        :return: 经过 Sbox 变换后的 32 位整数
        """
        return (
            (self.Sbox[(B >> 24) & 0xFF] << 24) |
            (self.Sbox[(B >> 16) & 0xFF] << 16) |
            (self.Sbox[(B >> 8) & 0xFF] << 8) |
            self.Sbox[B & 0xFF]
        )

    def _left_rotate(self, x, n):
        """
        对 32 位整数 x 进行循环左移操作

        :param x: 要进行左移的 32 位整数
        :param n: 左移的位数
        :return: 左移后的 32 位整数
        """
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def _T(self, X: int, is_key_expansion: bool = False) -> int:
        """
        对输入 X 进行 T 变换，包含 Sbox 变换和线性变换 L 或 L'

        :param X: 输入的 32 位整数
        :param is_key_expansion: 标志是否在密钥扩展阶段使用（默认为 False）
        :return: 经过 T 变换后的 32 位整数
        """
        B = self._tau(X)
        if is_key_expansion:
            # 密钥扩展中的 T' 变换 (包含线性变换 L')
            return B ^ self._left_rotate(B, 13) ^ self._left_rotate(B, 23)
        else:
            # 加密/解密过程中的 T 变换 (包含线性变换 L)
            return B ^ self._left_rotate(B, 2) ^ self._left_rotate(B, 10) ^ \
                   self._left_rotate(B, 18) ^ self._left_rotate(B, 24)

    def _key_expansion(self, key: bytes) -> list[int]:
        """
        SM4 密钥扩展函数，用于将 128 位的密钥扩展为 32 轮的子密钥

        :param key: 一个16字节的密钥（bytes）
        :return: 包含32轮密钥的列表，每个密钥为32位整数
        """
        # 将密钥分成4个32位的MK
        if not isinstance(key, bytes) or len(key) != 16:
            raise ValueError("密钥必须是16字节（128位）长度的bytes类型")
        MK = [int.from_bytes(key[i*4:(i+1)*4], byteorder='big') for i in range(4)]

        # 使用FK进行初始密钥的计算
        K = [MK[i] ^ self.FK[i] for i in range(4)]

        round_keys = []
        for i in range(32):
            temp = K[i+1] ^ K[i+2] ^ K[i+3] ^ self.CK[i]
            K.append(K[i] ^ self._T(temp, is_key_expansion=True))
            round_keys.append(K[-1])

        return round_keys

    # SM4 加密函数
    def _encrypt_block(self, plain_block: bytes, round_keys: list[int]) -> bytes:
        """
        SM4 加密函数，用于加密一个16字节（128位）的明文块

        :param plain_block: 一个16字节的明文块（bytes）
        :param round_keys: 32轮的加密密钥列表，每个密钥是32位整数
        :return: 加密后的16字节密文块（bytes）
        """
        X = [int.from_bytes(plain_block[i*4:(i+1)*4], byteorder='big') for i in range(4)]

        for i in range(32):
            temp = X[i+1] ^ X[i+2] ^ X[i+3] ^ round_keys[i]
            X.append(X[i] ^ self._T(temp))

        # 注意：使用X[35]到X[32]逆序组合
        cipher_block = b''.join(X[i].to_bytes(4, byteorder='big') for i in range(35, 31, -1))
        return cipher_block

    # SM4 解密函数
    def _decrypt_block(self, cipher_block: bytes, round_keys: list[int]) -> bytes:
        """
        SM4 解密函数，用于解密一个16字节（128位）的密文块

        :param cipher_block: 一个16字节的密文块（bytes）
        :param round_keys: 32轮的加密密钥列表（与加密时相同），每个密钥是32位整数
        :return: 解密后的16字节明文块（bytes）
        """
        X = [int.from_bytes(cipher_block[i*4:(i+1)*4], byteorder='big') for i in range(4)]

        for i in range(32):
            temp = X[i+1] ^ X[i+2] ^ X[i+3] ^ round_keys[31 - i]
            X.append(X[i] ^ self._T(temp))

        # 注意：同样使用X[35]到X[32]逆序组合
        plain_block = b''.join(X[i].to_bytes(4, byteorder='big') for i in range(35, 31, -1))
        return plain_block

    def _encrypt_cbc(self, plaintext: bytes, iv: bytes) -> bytes:
        """
        SM4 CBC 模式加密函数，用于加密任意长度的明文数据

        :param plaintext: 明文数据（bytes）
        :param iv: 初始向量（bytes），长度为16字节
        :return: 加密后的密文数据（bytes）
        """
        # 填充明文数据
        plaintext = pkcs7_padding(plaintext)

        # 初始化向量
        prev_cipher_block = iv
        ciphertext = b''

        # 分组加密
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]
            # 与前一个密文块进行异或
            block = xor_bytes(block, prev_cipher_block)
            # 加密
            encrypted_block = self._encrypt_block(block, self.round_keys)
            ciphertext += encrypted_block
            # 更新前一个密文块
            prev_cipher_block = encrypted_block

        return ciphertext

    def _decrypt_cbc(self, ciphertext: bytes, iv: bytes) -> bytes:
        """
        SM4 CBC 模式解密函数，用于解密任意长度的密文数据

        :param ciphertext: 密文数据（bytes），长度必须是16的倍数
        :param iv: 初始向量（bytes），长度为16字节
        :return: 解密后的明文数据（bytes）
        """
        # 初始化向量
        prev_cipher_block = iv
        decrypted_data = b''

        # 分组解密
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            # 解密当前块
            decrypted_block = self._decrypt_block(block, self.round_keys)
            # 与前一个密文块异或
            decrypted_block = xor_bytes(decrypted_block, prev_cipher_block)
            decrypted_data += decrypted_block
            # 更新前一个密文块
            prev_cipher_block = block

        # 去除填充数据
        decrypted_data = pkcs7_unpadding(decrypted_data)

        return decrypted_data
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        SM4 加密接口函数，用于加密任意长度的明文数据

        :param plaintext: 明文数据（bytes）
        :return: 加密后的密文数据（bytes）
        """
        return self._encrypt_cbc(plaintext, self.iv)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        SM4 解密接口函数，用于解密任意长度的密文数据

        :param ciphertext: 密文数据（bytes）
        :return: 解密后的明文数据（bytes）
        """
        return self._decrypt_cbc(ciphertext, self.iv)
    
if __name__ == '__main__':
    iv = b'0123456789012345'
    key = b'0123456789012345'
    sm4 = SM4(iv, key)
    plaintext = b'plaintext'

    ciphertext = sm4.encrypt(plaintext)
    print(ciphertext)
    decryptext = sm4.decrypt(ciphertext)
    print(decryptext)
