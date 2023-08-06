# Copyright 2022 iiPython

# Modules
import os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# Helper functions
def encrypt(key: bytes, source: bytes) -> bytes:
    key, IV = SHA256.new(key).digest(), Random.new().read(AES.block_size)
    padding = AES.block_size - len(source) % AES.block_size
    data = IV + AES.new(key, AES.MODE_CBC, IV).encrypt(source + bytes([padding]) * padding)
    return data

def decrypt(key: bytes, source: bytes) -> bytes:
    key, IV = SHA256.new(key).digest(), source[:AES.block_size]
    data = AES.new(key, AES.MODE_CBC, IV).decrypt(source[AES.block_size:])
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid key!")

    return data[:-padding]

# Open function wrapper
class FileHandle(object):
    def __init__(self, filename: str, key: str | bytes, codec: str = None):
        self.filename = filename
        self.key = key.encode("utf8") if not isinstance(key, bytes) else key
        self.codec = codec

        if not os.path.isfile(self.filename):
            self.write("")

    def __enter__(self) -> object:
        return self

    def __exit__(self, type, value, trace) -> None:
        del self.filename, self.key

    def read(self) -> str | bytes:
        with open(self.filename, "rb") as fh:
            data = decrypt(self.key, fh.read())
            return data if not self.codec else data.decode(self.codec)

    def write(self, data: str | bytes) -> None:
        if self.codec is not None and isinstance(data, str):
            data = data.encode(self.codec)

        with open(self.filename, "wb") as fh:
            fh.write(encrypt(self.key, data))

open_with_key = FileHandle
