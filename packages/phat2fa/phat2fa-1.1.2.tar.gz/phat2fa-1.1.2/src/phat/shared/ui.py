# Copyright 2022 iiPython

# Modules
import shutil
from time import sleep
from typing import Tuple
from iipython import readchar, keys

from rich.live import Live
from rich.panel import Panel
from rich.align import Align

from phat import __version__
from phat.errors import DeclinedKeyRequest
from phat.shared.drives import DriveHandler

# Primary UI class
class UI(object):
    def __init__(self) -> None:
        self.live = None

    def display(self, text: str) -> None:
        pane = Panel(
            Align(text, "center", vertical = "middle"),
            title = f"PHAT v{__version__}",
            title_align = "left",
            subtitle = "(c) 2022 iiPython",
            subtitle_align = "left",
            height = shutil.get_terminal_size()[1] - 1
        )
        self.live.update(pane)

# Initialization
ui, drives = UI(), DriveHandler()
loading_keys = "-\\|/"

# Handlers
def confirm(live) -> None:
    k = None
    while k not in ["y", "n", keys.CTRL_C]:
        k = readchar()

    live.console.clear()
    if k in ["n", keys.CTRL_C]:
        raise DeclinedKeyRequest

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

def request_key(pid: str) -> Tuple[bool, str]:
    with Live(refresh_per_second = 4) as live:
        live.console.clear()
        idx, ui.live = 0, live
        while not drives.search():
            ui.display(f"[yellow]\\[{loading_keys[idx]}] Please insert your key USB.[/]")
            idx = 0 if idx == 3 else idx + 1
            sleep(.25)  # Prevents ripping CPUs, plus it's as fast as possible

        # Turn live into a refresh-as-needed state
        class FakeLive:
            def update(content: str) -> None:
                live.console.clear()
                live.console.print(content, end = "")

        ui.live = FakeLive
        live.console.line = lambda: 0
        live.stop()
        live.console.clear()

        # Handle authorization
        usb, att = drives.mount, 0
        try:
            while True:
                try:
                    psw = get_input(f"Hello, [green]{usb.get_user()}[/]! Enter your password:", "*")
                    usb.authenticate(psw)
                    del psw
                    break

                except ValueError:
                    att += 1
                    if att > 2:
                        ui.display("[red]Invalid password specified.[/]\nYou have ran out of attempts, press any key to cancel 2FA request.")
                        readchar()
                        raise DeclinedKeyRequest

                    ui.display("[red]Invalid password specified.[/]\nPress any key to try again.")
                    readchar()

            fmt = lambda x: f"Hello, [green]{usb.get_user()}[/]!\n\n{x}\n[green]\\[Y]es[/]  or  [red]\\[N]o[/]"  # noqa
            if usb.has_key(pid):  # noqa: W601
                ui.display(fmt(f"Confirm authentication for [yellow]{pid}[/]?"))
                confirm(live)
                return True, usb.get_key(pid)

            else:
                ui.display(fmt(f"Create new key for [yellow]{pid}[/]?"))
                confirm(live)
                return False, usb.create_key(pid)

        except FileNotFoundError:
            ui.display("[red]The key USB was removed prior to authentication.[/]\nPress [yellow]any key[/] to cancel.")
            readchar()
            raise DeclinedKeyRequest
