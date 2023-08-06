# Copyright 2022 iiPython
# PHAT Key Controller Script

# Modules
import os
import json
from rich.console import Console
from iipython import readchar, keys

from phat.api import encrypt, decrypt
from phat.shared.ui import UI
from phat.shared.drives import (
    linux_get_drives, windows_get_drives
)

if os.name in ["nt", "win32"]:
    import win32api

# Initialization
ui, con = UI(), Console()

# USB post-initialization
def get_usbs_win() -> list:
    return [win32api.GetVolumeInformation(d)[0].strip() or "Unknown" + "-" + d for d in windows_get_drives()]

def get_usbs_linux() -> list:
    return [f"{p.device} - {p.mountpoint}" for p in linux_get_drives()]

get_usbs = {
    "win32": get_usbs_win, "nt": get_usbs_win,
    "posix": get_usbs_linux
}.get(os.name, lambda: exit("Unsupported OS."))

# UI Handlers
def fetch_keypress(accept: list) -> int | str:
    k = None
    while k not in [keys.CTRL_C] + accept:
        k = readchar()

    return k if k != keys.CTRL_C else exit()

def get_input(text: str, replace: str = None) -> str:
    res = ""
    while True:
        ui.display(f"{text}\n> {res if replace is None else replace * len(res)}")
        k = readchar()
        if isinstance(k, str):
            res += k

        elif k == keys.BACKSPACE and res:
            res = res[:-1]

        elif k == keys.ENTER and res:
            break

        elif k == keys.CTRL_C:
            exit()

    return res

def select_menu(text: str, entries: list, return_idx: bool = False) -> str | int:
    idx = 0
    while True:
        ui.display(f"{text}\n\n" + "\n".join([
            f"{'[yellow]> ' if entries.index(u) == idx else '[white]'}{u} [/]" for u in entries
        ]))
        k = readchar()
        if k == keys.UP:
            idx = (len(entries) if idx <= 0 else idx) - 1

        elif k == keys.DOWN:
            idx = (-1 if idx >= len(entries) - 1 else idx) + 1

        elif k == keys.ENTER:
            break

        elif k == keys.CTRL_C:
            exit()

    return entries[idx] if not return_idx else idx

def select_drive() -> str:
    ui.display("[yellow]Welcome to the PHAT Setup Script.[/]\nPlease insert a USB device and press ENTER.")

    # Fetch keypress
    fetch_keypress([keys.ENTER])

    # Grab drives
    while True:
        usb = select_menu("Please select a USB:", get_usbs() + ["Refresh", "Manually enter"]).split(" - ")
        if len(usb) == 1:
            if usb[0][0] == "R":
                continue

            else:
                mp = get_input("[yellow]Enter the device mountpoint (eg. /mnt/device or C:\\):[/]")
                if os.path.isdir(mp):
                    return mp

                ui.display("[red]Invalid device mountpoint specified.[/]\nPress any key to return to select menu.")
                readchar()
                continue

        return usb[1]

def create_key(directory: str) -> None:
    ui.display("[yellow]The selected drive has not been configured yet.[/]\nConfigure it as a key now? [green]\\[Y]es[/] [red]\\[N]o[/]")
    if fetch_keypress(["y", "n"]) != "y":
        return exit("Nothing to do.")

    name = get_input("[yellow]Enter your name (or nickname):[/]")
    while True:
        psw = get_input("[yellow]Enter a password for your keys:[/]", "*")
        psw_conf = get_input("[yellow]Confirm password:[/]", "*")
        if psw != psw_conf:
            ui.display("[red]Passwords do not match.[/]\nPress any key to reenter.")
            readchar()

        else:
            del psw_conf
            break

    # Create drive
    j = lambda x: os.path.abspath(os.path.join(directory, x))  # noqa
    os.mkdir(directory)
    with open(j("user.json"), "w+") as userfh:
        userfh.write(json.dumps({"name": name}))

    with open(j("keys.db"), "wb") as keysfh:
        keysfh.write(encrypt(psw.encode("utf8"), b"{}"))

    del psw  # Safer to delete it immediately after use

def change_options(directory: str) -> None:
    j = lambda x: os.path.abspath(os.path.join(directory, x))  # noqa
    ui.display("[yellow]The selected drive has already been configured.[/]\nEdit? [green]\\[Y]es[/] [red]\\[N]o[/]")
    if fetch_keypress(["y", "n"]) != "y":
        return exit("Nothing to do.")

    while True:
        opt = select_menu(
            "Select an action to perform.",
            ["Change name", "Change password", "Exit"],
            return_idx = True
        )
        if opt == 0:
            with open(j("user.json"), "r") as userfh:
                old_name = json.loads(userfh.read())["name"]

            name = get_input(f"Changing name from '{old_name}' to:")
            with open(j("user.json"), "w") as userfh:
                userfh.write(json.dumps({"name": name}))

            ui.display("[green]Name updated successfully.[/]\nPress any key to return to the previous menu.")
            readchar()

        elif opt == 1:
            try:
                psw = get_input("Current password:", "*")
                with open(j("keys.db"), "rb") as keyfh:
                    keydb = keyfh.read()

                keydb = decrypt(psw.encode("utf8"), keydb)

            except ValueError:
                ui.display("[red]Invalid password.[/]\nPress any key to return to the previous menu.")
                readchar()
                continue

            while True:
                psw = get_input("[yellow]New password:[/]", "*")
                psw_conf = get_input("[yellow]Confirm password:[/]", "*")
                if psw != psw_conf:
                    ui.display("[red]Passwords do not match.[/]\nPress any key to reenter.")
                    readchar()

                else:
                    del psw_conf
                    break

            with open(j("keys.db"), "wb") as keyfh:
                keyfh.write(encrypt(psw.encode("utf8"), keydb))

            ui.display("[green]Password updated successfully.[/]\nPress any key to return to the previous menu.")
            readchar()

        elif opt == 2:
            return

# Main live loop
class FakeLive:
    def update(content: str) -> None:
        con.clear()
        con.print(content, end = "")

def setup() -> None:
    con.clear()
    ui.live = FakeLive

    # Identify drive
    phat_directory = os.path.join(select_drive(), "$PHAT")

    # Check operation
    if not os.path.isdir(phat_directory):
        create_key(phat_directory)

    else:
        change_options(phat_directory)

    ui.display("The USB device has been configured successfully.\nPlease unplug the device until needed.\n\n[green]Press any key to exit.[/]")
    readchar()
