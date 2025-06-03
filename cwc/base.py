from abc import ABC, abstractmethod

class Cipher(ABC):
    """抽象基类：定义统一的加密算法接口"""

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        """加密方法，子类需要实现"""
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        """解密方法，子类需要实现"""
        pass

class SignatureAlgorithm(ABC):
    """抽象基类：定义统一的签名算法接口"""

    @abstractmethod
    def sign(self, message: bytes) -> bytes:
        """签名方法，子类需要实现"""
        pass

    @abstractmethod
    def verify(self, message: bytes, signature: bytes) -> bool:
        """验证签名方法，子类需要实现"""
        pass
