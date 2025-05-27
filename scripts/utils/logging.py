import logging
from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.logging import RichHandler
from rich.panel import Panel

from ..models import ServerStatus


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


def render_server_status(server_info: ServerStatus, time_idle: int = 0) -> Layout:
    layout = Layout(name='main_layout')

    status = [
        Align.center(
            f'🟢 Server Status: {server_info.status}',
            style='bold green' if server_info.status == 'Online' else 'bold red'
        ),
        Align.center(
            f'👥 Players Online: {server_info.players_online} / {server_info.max_players}' if server_info.max_players
            else '👥 Players Online: Unknown',
            style='bold blue'
        ),
        Align.center(
            f'🌐 Latency: {server_info.latency} ms' if server_info.latency is not None else '🌐 Latency: Unknown',
            style='bold yellow'
        ),
        Align.center(
            Align.center(f'⏱️ Time since last player left: {time_idle}', style='italic')
        )
    ]

    server_stats = Layout(
        Panel(
            Group(*status), title='📊 Server Status',
            border_style='magenta',
            expand=True
        )
    )

    layout.split_column(
        server_stats,
        Layout(Panel(server_info.server_logs, title='🖥️ Minecraft Server', border_style='cyan'), name='logs'),
    )

    return layout
