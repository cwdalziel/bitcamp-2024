import json
import dataclasses

class GameDB:
    
    @classmethod
    def load_data(path: str) -> dict:
        with open(path, 'r') as f:
            return json.loads(f.read())
    
    @classmethod
    def write_data(data: dict, path: str = None) -> None:
        with open(path, 'w') as f:
            f.write(json.dumps(data))
    
    def __init__(self, data_path: str = 'backend/players.json'):
        self.data_path = data_path
        self.data = self.load_data(data_path)
    
    def new_player(self, name: str): pass
    
# XP
# XP per second
# Money
# Last Log-on