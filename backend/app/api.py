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
    return {"data": db.get_user_stats(username, False)}

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

@app.get('user/enemy/health/set{username}')
async def set_enemy_health(username: str, health: int) -> dict:
    db.set_enemy_health(username, health)
    return {"status": True}

class Stat(BaseModel):
    amount: int = 0
    date: str = ""
    desc: str = ""

@app.get('/user/stat/add')
async def add_user_stat(username: str, stat: Stat) -> dict:
    db.add_user_stat(username=username, stat=Stats(stat))
    return {"status": "success"}



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

