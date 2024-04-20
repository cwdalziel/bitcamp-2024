import json
from dataclasses import dataclass
from os.path import exists


def load_data(path: str) -> dict:
    with open(path, 'r') as f:
        return json.loads(f.read())

def write_data(data: dict, path: str = 'backend/players.json') -> None:
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=2))

@dataclass
class Stats:
    xp: int = 0
    xp_per_second: int = 1
    

class GameDB:
    def __init__(self, data_path: str = 'backend/players.json'):
        self.data_path = data_path
        
        if exists(data_path):
            self.data = load_data(data_path)
        else:
            with open(data_path, 'w') as f:
                f.write("{}")
            self.data = {}
    
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
    
    def user_exists(self, username: str):
        return not username in self.data
    
    def get_user_account_id(self, username: str, password: str) -> str | None:
        if username in self.data.keys():
            if password == self.data[username]['password']:
                return self.data[username]['account_id']
        
        return None

    def get_user_stats(self, id: str) -> Stats: pass

# XP
# XP per second
# Money
# Last Log-on