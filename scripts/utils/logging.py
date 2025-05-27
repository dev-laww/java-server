import logging
from typing import Optional

from rich import box
from rich.console import Group
from rich.layout import Layout
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

from .server import ServerStatus


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name is None:
        name = __name__

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    rich_handler = RichHandler(rich_tracebacks=True, markup=True)
    rich_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(message)s')
    rich_handler.setFormatter(formatter)

    logger.addHandler(rich_handler)

    return logger


def render_server_status(server_info: ServerStatus) -> Layout:
    layout = Layout()

    server_logs, playit_logs, server_status, time_idle = (
        server_info.server_logs,
        server_info.playit_logs,
        server_info.server_status,
        server_info.time_idle,
    )

    layout.split_row(
        Layout(Panel(server_logs, title="🖥️ Minecraft Server", border_style="cyan", box=box.ROUNDED)),
        Layout(Panel(playit_logs, title="🌐 Playit Tunnel", border_style="green", box=box.ROUNDED)),
    )

    footer = Group(
        Text(server_status, style="bold yellow"),
        Text(f"⏱️ Time since last player left: {time_idle}", style="italic"),
    )

    layout.split_column(
        layout,
        Layout(Panel(footer, title="📊 Server Stats", border_style="magenta"))
    )

    return layout
