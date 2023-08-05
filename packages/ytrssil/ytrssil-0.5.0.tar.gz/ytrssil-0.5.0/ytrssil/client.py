import requests
from inject import autoparams

from ytrssil.config import Configuration
from ytrssil.datatypes import User, Video


class HttpClient:
    @autoparams('config')
    def __init__(self, config: Configuration) -> None:
        self.base_url: str = config.api_url
        self.auth = requests.auth.HTTPBasicAuth(
            config.username,
            config.password,
        )

    def fetch(self) -> None:
        resp = requests.post(url=f'{self.base_url}/fetch')
        resp.raise_for_status()

    def register(self) -> None:
        user = User(username=self.auth.username, password=self.auth.password)
        resp = requests.post(url=f'{self.base_url}/fetch', json=user)
        resp.raise_for_status()

    def subscribe_to_channel(self, channel_id: str) -> None:
        resp = requests.post(
            url=f'{self.base_url}/api/channels/{channel_id}/subscribe',
            auth=self.auth,
        )
        resp.raise_for_status()

    def get_new_videos(self) -> list[Video]:
        resp = requests.post(
            url=f'{self.base_url}/api/videos/new',
            auth=self.auth,
        )
        resp.raise_for_status()
        data = resp.json()
        ret: list[Video] = []
        for video_data in data['videos']:
            ret.append(Video(**video_data))

        return ret

    def get_watched_videos(self) -> list[Video]:
        resp = requests.post(
            url=f'{self.base_url}/api/videos/watched',
            auth=self.auth,
        )
        resp.raise_for_status()
        data = resp.json()
        ret: list[Video] = []
        for video_data in data['videos']:
            ret.append(Video(**video_data))

        return ret

    def mark_video_as_watched(self, video_id: str) -> None:
        resp = requests.post(
            url=f'{self.base_url}/api/videos/{video_id}/watch',
            auth=self.auth,
        )
        resp.raise_for_status()

    def mark_video_as_unwatched(self, video_id: str) -> None:
        resp = requests.post(
            url=f'{self.base_url}/api/videos/{video_id}/unwatch',
            auth=self.auth,
        )
        resp.raise_for_status()
