# Copyright 2022 iiPython

# Modules
import os
import json
import random
import string
import psutil
import hashlib

from phat.errors import NotAuthenticated
from phat.encryption import open_with_key

# Platform-dependent
if os.name == "posix":
    import pyudev
    ctx = pyudev.Context()

elif os.name == "nt":
    import win32api
    import win32file

# Handle drive finding
def linux_get_drives() -> list:
    res, removable = [], [d for d in ctx.list_devices(
        subsystem = "block",
        DEVTYPE = "disk"
    ) if d.attributes.asstring("removable") == "1"]
    for device in removable:
        parts = [d.device_node for d in ctx.list_devices(subsystem = "block", DEVTYPE = "partition", parent = device)]
        for p in psutil.disk_partitions():
            if p.device in parts:
                res.append(p)

    return res

def windows_get_drives() -> list:
    res = []
    for device in win32api.GetLogicalDriveStrings().split("\x00")[:-1]:
        if win32file.GetDriveType(device) == win32file.DRIVE_REMOVABLE:
            res.append(device)

    return res

# Handle key editing
class KeyHandler(object):
    def __init__(self, mount: str) -> None:
        self.mount = mount
        self.keydb = os.path.join(self.mount, "keys.db")

    def authenticate(self, password: str) -> None:
        self.password = password
        with open_with_key(self.keydb, password, "utf8") as fh:
            self.entries = json.loads(fh.read())

    def generate_key(self) -> str:
        return hashlib.sha512("".join([random.choice(string.printable) for i in range(32)]).encode()).hexdigest()

    def has_key(self, pid: str) -> bool:
        if not hasattr(self, "entries"):
            raise NotAuthenticated

        return pid in self.entries

    def create_key(self, pid: str, auto_close: bool = True) -> str:
        if not hasattr(self, "entries"):
            raise NotAuthenticated

        key = self.generate_key()
        self.entries[pid] = key
        with open_with_key(self.keydb, self.password, "utf8") as fh:
            fh.write(json.dumps(self.entries))

        if auto_close:
            del self.entries, self.password

        return key

    def get_key(self, pid: str, auto_close: bool = True) -> str:
        if self.entries is None:
            raise NotAuthenticated

        key = self.entries[pid]
        if auto_close:
            del self.entries, self.password

        return key

    def get_user(self) -> str:
        with open(os.path.join(self.mount, "user.json"), "r") as fh:
            return json.loads(fh.read())["name"]

# Main handler
class DriveHandler(object):
    def __init__(self) -> None:
        if os.name == "posix":
            self.search = self.search_linux

        elif os.name == "nt":
            self.search = self.search_windows

        self.mount = None

    def check(self, mountpoint: str) -> bool:
        path = os.path.abspath(os.path.join(mountpoint, "$PHAT"))
        if not os.path.isdir(path):
            return False

        self.mount = KeyHandler(path)
        return True

    def search_linux(self) -> bool:
        for p in linux_get_drives():
            if self.check(p.mountpoint):
                return True

        return False

    def search_windows(self) -> bool:
        for device in windows_get_drives():
            if self.check(device):
                return True

        return False
