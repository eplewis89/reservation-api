import json

class Configuration:
    def __init__(self):
        self.app_config = self.get_app_config()

    def get_app_config(self):
        with open("config/app_config.json", "r") as config_file:
            return json.load(config_file)["app_config"]
    
    def get_path(self):
        return self.app_config["main_db"]