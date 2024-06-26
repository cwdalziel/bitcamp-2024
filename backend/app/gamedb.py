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
    data = dataclass_json_dump(data)
    
    with open(path, 'w') as f:
        f.write(data)

@dataclass
class Stats:
    amount: int = 0
    date: str = ""
    desc: str = ""

    def __getitem__(self, item):
        return getattr(self, item)
    
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
            'health': 1000,
            'damage': 3,
            'enemy_health': 1000,
            'enemy_damage': 1,
            'enemy_id': 1,
            'enemies_defeated': 0
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

    def get_user_stats(self, username: str) -> list[Stats]:
        return self.data[username]['stats']
    
    def get_user_health(self, username: str) -> int:
        return self.data[username]['health']

    def get_enemy_health(self, username: str) -> int:
        return self.data[username]['enemy_health']
    
    def add_user_stat(self, username: str, stat: Stats) -> None:
        self.data[username]['stats'].append(stat)
        write_data(self.data)
    
    def set_user_health(self, username: str, val: int) -> None:
        self.data[username]['health'] = val
        write_data(self.data)
    
    def set_enemy_health(self, username: str, val: int) -> None:
        self.data[username]['enemy_health'] = val
        write_data(self.data)

    def get_user_damage(self, username: str) -> int:
        return self.data[username]['damage']
    
    def set_user_damage(self, username: str, val: int) -> None:
        self.data[username]['damage'] = val
        write_data(self.data)

    def get_enemy_damage(self, username: str) -> int:
        return self.data[username]['enemy_damage']
    
    def set_enemy_damage(self, username: str, val: int) -> None:
        self.data[username]['enemy_damage'] = val
        write_data(self.data)
    
    def get_user_id(self, username: str) -> int:
        return self.data[username]['account_id']
    
    def get_enemy_id(self, username: str) -> int:
        return self.data[username]['enemy_id']
    
    def set_enemy_id(self, username: str, id: int) -> int:
        self.data[username]['enemy_id'] = id
        write_data(self.data)
    
    def get_enemies_defeated(self, username: str) -> int:
        return self.data[username]['enemies_defeated']

    def increment_enemies_defeated(self, username: str, i = 0) -> int:
        self.data[username]['enemies_defeated'] = self.get_enemies_defeated(username) + i
        write_data(self.data)