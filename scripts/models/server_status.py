from typing import Optional

from pydantic import BaseModel


class ServerStatus(BaseModel):
    status: str = 'Unknown'
    players_online: Optional[int] = 0
    max_players: Optional[int] = 0
    latency: Optional[float] = None
    server_logs: Optional[str] = None
    playit_logs: Optional[str] = None
