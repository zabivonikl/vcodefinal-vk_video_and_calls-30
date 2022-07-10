import ast
import json
import os
from random import randint

import dotenv
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.vk_api import VkApiMethod

dotenv.load_dotenv()


class Vk:
    _user_session: VkApi
    _user_api: VkApiMethod
    _streams: set = set()

    def __init__(self):
        self._user_session = VkApi(token=os.environ["USER_API_KEY"])
        self._user_session.api_version = "5.131"
        self._user_api = self._user_session.get_api()

    def get_new_streams(self, owner_id):
        videos = self._user_api.video.get(owner_id=owner_id, count=200)["items"]
        current_streams = set(map(lambda x: str({
            "live_status": x["live_status"],
            "title": x["title"],
            "player": f"https://vk.com/video{x['owner_id']}_{x['id']}"
        }), filter(
            lambda x: x['type'] == "live" and x['live_status'] == "started",
            videos
        )))
        new_translations = current_streams - self._streams
        self._streams = current_streams
        return list(map(lambda x: ast.literal_eval(x), new_translations))
