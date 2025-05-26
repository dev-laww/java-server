from rich import box
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from .server import ServerInfo


def create_layout(server_info: ServerInfo) -> Layout:
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
