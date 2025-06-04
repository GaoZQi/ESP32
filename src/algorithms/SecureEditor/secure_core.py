from .sm4_cipher import SM4
from .sm3_cipher import SM3
from datetime import datetime
import sys
import os

IV = b"0123456789012345"
KEY = b"0123456789012345"
MAGIC_HEADER = b"NPUSECENC001"
HASH_SIZE = 32

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, "secure_editor.log")


def write_log(action: str, filepath: str, result: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action} | 文件: {filepath} | 结果: {result}\n"
        )


def load_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        raw = f.read()

    if not raw.startswith(MAGIC_HEADER):
        raise ValueError("不是受控文件")

    if len(raw) < len(MAGIC_HEADER) + HASH_SIZE + 16:
        raise ValueError("文件结构异常")

    encrypted_data = raw[len(MAGIC_HEADER) : -HASH_SIZE]
    hash_stored = raw[-HASH_SIZE:]

    expected_length = len(MAGIC_HEADER) + len(encrypted_data) + HASH_SIZE
    if len(raw) != expected_length:
        raise ValueError("文件被篡改（长度不一致）")

    try:
        cipher = SM4(iv=IV, key=KEY)
        decrypted = cipher.decrypt(encrypted_data)
    except Exception:
        raise ValueError("文件被篡改（解密失败）")

    sm3 = SM3()
    hash_calculated = sm3.hash(decrypted)
    if hash_calculated != hash_stored:
        raise ValueError("文件被篡改（哈希校验失败）")

    try:
        return decrypted.decode("utf-8")
    except Exception:
        raise ValueError("文件内容解码失败（可能被破坏）")


def save_file(file_path: str, plaintext: str):
    data = plaintext.encode("utf-8")
    cipher = SM4(iv=IV, key=KEY)
    encrypted = cipher.encrypt(data)

    sm3 = SM3()
    hash_value = sm3.hash(data)

    with open(file_path, "wb") as f:
        f.write(MAGIC_HEADER + encrypted + hash_value)
