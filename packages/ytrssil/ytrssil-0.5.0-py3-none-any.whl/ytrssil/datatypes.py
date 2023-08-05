from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Video:
    video_id: str
    name: str
    channel_name: str
    timestamp: datetime
    watch_timestamp: Optional[datetime] = None

    def __str__(self) -> str:
        return f'{self.channel_name} - {self.name} - {self.video_id}'


@dataclass
class Channel:
    channel_id: str
    name: str

    def __str__(self) -> str:
        return f'{self.name} - {self.channel_id}'


@dataclass
class User:
    username: str
    password: str
