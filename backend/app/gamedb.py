import json
import dataclasses
from dataclasses import dataclass
from os.path import exists

class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def dataclass_json_dump(data: dict) -> str:
    return json.dumps(data, cls=DataclassJSONEncoder, indent=2)

def load_data(path: str) -> dict:
    with open(path, 'r') as f:
        return json.loads(f.read())

def write_data(data: dict, path: str = 'backend/players.json') -> None:
    with open(path, 'w') as f:
        f.write(dataclass_json_dump(data))

@dataclass
class Stats:
    amount: int = 0
    date: str = ""
    desc: str = ""
    
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
            'stats': [],
            'health': 0,
            'enemy_health': 0
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

    def get_user_stats(self, username: str, as_json = False) -> Stats:
        if as_json:
            return self.data[username]['stats']
        return self.data[username]['stats']
    
    def get_user_health(self, username: str) -> int:
        return self.data[username]['health']

    def get_enemy_health(self, username: str) -> int:
        return self.data[username]['enemy_health']
    
    def add_user_stat(self, username: str, stat: Stats) -> None:
        self.data[username]['stats'].append(stat)
    
    def set_user_health(self, username: str, val: int) -> None:
        self.data[username]['health'] = val
    
    def set_enemy_health(self, username: str, val: int) -> None:
        self.data[username]['enemy_health'] = val
    
# Things to add endpoints for:
# 
# Get user stats
# Get user health
# Get enemy health
# 