def pkcs7_padding(data: bytes, block_size: int = 16) -> bytes:
    """
    对输入数据进行 PKCS7 填充，保证数据长度是 block_size 的倍数

    :param data: 需要填充的数据（bytes）
    :param block_size: 块大小，默认为 16 字节
    :return: 填充后的数据（bytes）
    """
    pad_len = block_size - (len(data) % block_size)
    padding = bytes([pad_len] * pad_len)
    return data + padding

def pkcs7_unpadding(data: bytes) -> bytes:
    """
    去除 PKCS7 填充，返回原始数据

    :param data: 带填充的数据（bytes）
    :return: 去除填充后的数据（bytes）
    :raises ValueError: 如果填充无效，抛出异常
    """
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def xor_bytes(a: bytes, b: bytes) -> bytes:
    """
    对两个字节数组进行逐字节的异或操作

    :param a: 字节数组 a
    :param b: 字节数组 b
    :return: 异或后的结果（bytes）
    """
    return bytes(x ^ y for x, y in zip(a, b))

def bytes_to_list(data: bytes) -> list:
    """
    将字节序列转换为整数列表

    :param data: 输入的字节序列
    :return: 转换后的整数列表
    """
    return [i for i in data]