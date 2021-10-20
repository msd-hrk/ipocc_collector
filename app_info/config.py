import json

class Config:
    def __init__(self):
        config_path = "app_info/config.json"
        config = json.load(open(config_path, "r"))
        self.address = config["address"]
        self.password = config["password"]
        self.mongo_url = config["mongo_url"]
        self.ignore_nums = config["ignore_nums"]
        self.data_insert_flg = bool(config["data_insert_flg"])