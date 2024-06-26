import os

import aiohttp
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .gamedb import GameDB, Stats
from pydantic import BaseModel
import json

API_HEAD = "http://api.nessieisreal.com"

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()
db = GameDB()

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_url_json(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

@app.get('/user/stats/{username}')
async def get_stats(username: str) -> dict:
    return {"data": db.get_user_stats(username)}

@app.get('/user/health/get/{username}')
async def get_health(username: str) -> dict:
    return {"data": db.get_user_health(username)}

@app.get('/user/health/set/{username}')
async def set_health(username: str, health: int) -> dict:
    db.set_user_health(username, health)
    return {"status": True}

@app.get('/user/enemy/health/get/{username}')
async def get_enemy_health(username: str) -> dict:
    return {"data": db.get_enemy_health(username)}

@app.get('/user/enemy/health/set/{username}')
async def set_enemy_health(username: str, health: int) -> dict:
    db.set_enemy_health(username, health)
    return {"status": True}

@app.get('/user/damage/get/{username}')
async def get_user_damage(username: str) -> dict:
    return {"data": db.get_user_damage(username)}

@app.get('/user/damage/set/{username}')
async def set_user_damage(username: str, dmg: int) -> dict:
    db.set_user_damage(username, dmg)
    return {"status": True}

@app.get('/user/enemy/damage/get/{username}')
async def get_enemy_damage(username: str) -> dict:
    return {"data": db.get_enemy_damage(username)}

@app.get('/user/enemy/damage/set/{username}')
async def set_enemy_damage(username: str, dmg: int) -> dict:
    db.set_enemy_damage(username, dmg)
    return {"status": True}

@app.get('/user/id/{username}')
async def get_user_id(username: str) -> dict:
    return {"data": db.get_user_id(username)}

class Stat(BaseModel):
    amount: int = 0
    date: str = ""
    desc: str = ""

@app.post('/user/stats/add')
async def add_user_stat(username: str, stat: Stat) -> dict:
    db.add_user_stat(username=username, stat=Stats(stat.amount, stat.date, stat.desc))
    return {"status": "success"}

@app.get('/user/balance/{username}')
async def get_user_balance(username: str) -> dict:
    total = 0
    for s in db.get_user_stats(username):
        total += s['amount']
    
    return {'data': total}

# enemy id
@app.get("/user/enemy/id/{username}")
async def get_user_enemy_id(username: str) -> dict:
    return {'id': db.get_enemy_id(username)}

# deal damage
@app.post("/user/damage/{username}")
async def user_deal_damage(username: str, damage: int) -> dict:
    e_hp = db.get_enemy_health(username) - (-(-damage // 2))
    u_hp = min(db.get_user_health(username) + (damage // 2), 10000)
    id = db.get_enemy_id(username)
    d = db.get_enemies_defeated(username)
    
    if e_hp <= 0:
        db.set_enemy_health(username, 1000)
        id = (id + 1) % 3
        if id == 0:
            db.set_enemy_health(username, 5000)
        db.set_enemy_id(username, id)
        d += 1 + (-e_hp) // 15
        db.increment_enemies_defeated(username, 1 + (-e_hp) // 1000)
        return {
            'enemy_killed': True,
            'player_killed': False,
            'enemy_id': id,
            'enemy_hp': db.get_enemy_health(username),
            'user_hp': u_hp,
            'enemies_defeated': d
        }
    
    if u_hp <= 0:
        return {
            'enemy_killed': False,
            'player_killed': True,
            'enemy_id': id,
            'enemy_hp': e_hp,
            'user_hp': 0,
            'enemies_defeated': d
        }
        
    db.set_user_health(username, u_hp)
    db.set_enemy_health(username, e_hp)
    
    return {
        'enemy_killed': False,
        'player_killed': False,
        'enemy_id': id,
        'enemy_hp': e_hp,
        'user_hp': u_hp,
        'enemies_defeated': d
    }
    
@app.get("/user/enemy/defeated/{username}")    
async def get_enemies_defeated(username: str) -> dict:
    return {'data': db.get_enemies_defeated(username)}

@app.get("/")
async def read_root() -> dict:
    return {"message": f"hello :)"}

# account endpoints
@app.get("/customers/{id}/accounts")
async def read_customer_accounts(id: str) -> dict:
    return {
        "data": await get_url_json(f"{API_HEAD}/customers/{id}/accounts?key={API_KEY}")
    }

# customer endpoints
@app.get("/accounts/{id}/customer")
async def read_account_customer(id: str) -> dict:
    data = await get_url_json(f"{API_HEAD}/accounts/{id}/customer?key={API_KEY}")
    return {"data": data}

# bill endpoints
@app.get("/accounts/{id}/bills")
async def read_account_bills(id: str) -> dict:
    return {"data": await get_url_json(f"{API_HEAD}/accounts/{id}/bills?key={API_KEY}")}

@app.get("/customers/{id}/bills")
async def read_customer_bills(id: str) -> dict:
    return {
        "data": await get_url_json(f"{API_HEAD}/customers/{id}/bills?key={API_KEY}")
    }

# transfer endpoints
@app.get("/accounts/{id}/transfers")
async def read_account_transfers(id: str, type: str) -> dict:
    return {
        "data": await get_url_json(
            f"{API_HEAD}/accounts/{id}/transfers?type={type}&key={API_KEY}"
        )
    }

# purchase endpoints
@app.get("/accounts/{id}/purchases")
async def read_account_purchases(id: str) -> dict:
    return {
        "data": await get_url_json(f"{API_HEAD}/accounts/{id}/purchases?key={API_KEY}")
    }

# deposit endpoints
@app.get("/accounts/{id}/deposits")
async def read_account_deposits(id: str) -> dict:
    return {
        "data": await get_url_json(f"{API_HEAD}/accounts/{id}/deposits?key={API_KEY}")
    }


class Account(BaseModel):
    type: str
    nickname: str
    rewards: int
    balance: int
    account_number: str


@app.post("/customers/{id}/accounts")
async def post_customer_accounts(id: str, account: Account) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_HEAD}/customers/{id}/accounts?key={API_KEY}",
            json=account.model_dump(),
        ) as resp:
            return {"data": await resp.json()}


class Address(BaseModel):
    street_number: str
    street_name: str
    city: str
    state: str
    zip: str


class Customer(BaseModel):
    first_name: str
    last_name: str
    address: Address


@app.post("/customers")
async def post_customer(customer: Customer) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_HEAD}/customers/?key={API_KEY}", json=customer.model_dump()
        ) as resp:
            return {"data": await resp.json()}


class Player(BaseModel):
    username: str
    password: str
    customer: Customer


@app.post("/new_player")
async def new_player(player: Player) -> dict:
    if db.user_exists(player.username):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_HEAD}/customers/?key={API_KEY}",
                json=player.customer.model_dump(),
            ) as resp:
                data = await resp.json()

                if data['code'] >= 300:
                    raise HTTPException(status_code=data['code'], detail=data['message'])

                id = data['objectCreated']['_id']
                db.new_user(player.username, player.password, id, _write=True)

        return {"id": id}
    raise HTTPException(status_code=400, detail="Username already in use.")


class PartialPlayer(BaseModel):
    username: str
    password: str


@app.post("/get_player_id")
async def read_player_id(partial: PartialPlayer) -> dict:
    id = db.get_user_account_id(partial.username, partial.password)

    if id:
        return {"id": id}
    raise HTTPException(status_code=400, detail = "Incorrect username/password combination or username doesn't exist.")

