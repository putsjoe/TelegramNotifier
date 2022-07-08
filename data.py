# Handle persistent data without a database
import os
import pickle
from dataclasses import dataclass

CONFIG_FILE = os.path.join(os.getcwd(), 'config.p')


@dataclass
class Config:
    user_id: str = None
    bot_token: str = None
    api_token: str = 'Nothing'

    def save(self):
        with open(CONFIG_FILE, "wb+") as conffile:
            pickle.dump(self.__dict__, conffile)
        return


def get_config():
    with open(CONFIG_FILE, "rb+") as conffile:
        try:
            data = pickle.load(conffile)
        except EOFError:
            return Config(None, None)
    return Config(**data)
