import json
import dataclasses

def load_data(path: str) -> dict:
    with open(path, 'r') as f:
        return json.loads(f.read())


def write_data(data: dict, path: str = 'backend/players.json') -> None:
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=2))

class GameDB:
    def __init__(self, data_path: str = 'backend/players.json'):
        self.data_path = data_path
        self.data = load_data(data_path)
    
    def new_user(self, username: str, password: str, account_id: str, _write = False):
        data = {
            'password': password,
            'account_id': account_id,
            'player': {}
        }
        
        if username in self.data.keys():
            return False
        
        self.data[username] = data
        
        if _write:
            write_data(self.data)
            
        return True
    
# XP
# XP per second
# Money
# Last Log-on