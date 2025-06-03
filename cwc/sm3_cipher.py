from base import Cipher

class SM3(Cipher):
    def __init__(self):
        self.IV = [
            0x7380166F, 0x4914B2B9,
            0x172442D7, 0xDA8A0600,
            0xA96F30BC, 0x163138AA,
            0xE38DEE4D, 0xB0FB0E4E
        ]

        self.T = [0x79cc4519] * 16 + [0x7a879d8a] * 48

    # 常用运算
    def _rotate_left(self, x, n):
        return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

    def _ff(self, x, y, z, j):
        return (x ^ y ^ z) if j < 16 else ((x & y) | (x & z) | (y & z))

    def _gg(self, x, y, z, j):
        return (x ^ y ^ z) if j < 16 else ((x & y) | ((~x) & z))

    def _p0(self, x):
        return x ^ self._rotate_left(x, 9) ^ self._rotate_left(x, 17)

    def _p1(self, x):
        return x ^ self._rotate_left(x, 15) ^ self._rotate_left(x, 23)

    # 填充消息
    def _padding(self, message: bytes) -> bytes:
        """
        对输入的消息进行填充，使其长度符合 SM3 的要求

        :param message: 原始消息（bytes）
        :return: 填充后的消息（bytes）
        """
        mlen = len(message) * 8
        message += b'\x80'
        message += b'\x00' * ((56 - (len(message) % 64)) % 64)
        message += mlen.to_bytes(8, 'big')
        return message

    # 消息分组
    def _message_expand(self, b):
        """
        对 512 位（64 字节）的消息分组进行消息扩展，生成 w 和 w' 列表

        :param b: 64 字节的消息分组（bytes）
        :return: 扩展后的 132 个 32 位整数列表 w 和 w'
        """
        w = [int.from_bytes(b[i:i + 4], 'big') for i in range(0, 64, 4)]
        for j in range(16, 68):
            w.append(self._p1(w[j - 16] ^ w[j - 9] ^ self._rotate_left(w[j - 3], 15)) ^ self._rotate_left(w[j - 13], 7) ^ w[j - 6])
        for j in range(64):
            w.append(w[j] ^ w[j + 4])
        return w

    def _cf(self, v, b):
        """
        SM3 迭代压缩函数，用于对一个消息分组进行迭代压缩操作

        :param v: 输入的8个32位的初始向量（IV）或上一轮的结果列表
        :param b: 一个64字节的消息分组（bytes）
        :return: 压缩后的8个32位整数（状态变量列表）
        """
        w = self._message_expand(b)
        a, b, c, d, e, f, g, h = v
        for j in range(64):
            ss1 = self._rotate_left((self._rotate_left(a, 12) + e + self._rotate_left(self.T[j], j % 32)) & 0xFFFFFFFF, 7)
            ss2 = ss1 ^ self._rotate_left(a, 12)
            tt1 = (self._ff(a, b, c, j) + d + ss2 + w[j + 68]) & 0xFFFFFFFF
            tt2 = (self._gg(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
            d = c
            c = self._rotate_left(b, 9)
            b = a
            a = tt1
            h = g
            g = self._rotate_left(f, 19)
            f = e
            e = self._p0(tt2)
        return [(x ^ y) & 0xFFFFFFFF for x, y in zip(v, [a, b, c, d, e, f, g, h])]

    def _SM3Hash(self, message: bytes) -> bytes:
        """
        SM3 哈希主函数，用于对整个消息进行哈希计算

        :param message: 要进行哈希的原始消息（bytes）
        :return: 哈希值，长度为32字节（256位）（bytes）
        """
        message = self._padding(message)
        v = self.IV.copy()
        for i in range(0, len(message), 64):
            v = self._cf(v, message[i:i + 64])
        result = b''.join(x.to_bytes(4, 'big') for x in v)
        return result
    
    def encrypt(self, message: bytes) -> bytes:
        return self._SM3Hash(message)

    def decrypt(self, ciphertext: bytes) -> bytes:
        raise NotImplementedError("SM3 does not support decrypt.")
    
    def hash(self, message: bytes) -> bytes:
        """
        计算输入消息的 SM3 哈希值

        :param message: 要计算哈希值的消息（bytes）
        :return: 32字节（256位）的哈希值（bytes）
        """
        return self._SM3Hash(message)

if __name__ == '__main__':
    sm3 = SM3()
    message = b'123'
    
    print(sm3.hash(message))
    message = b'123'
    print(sm3.hash(message))