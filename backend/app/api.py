import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import aiohttp

API_HEAD = "http://api.nessieisreal.com"

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def get_url_json(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

@app.get("/")
async def read_root() -> dict:
    return {"message": f"hello :)"}

# account endpoints
@app.get("/customers/{id}/accounts")
async def read_customer_accounts(id: str) -> dict:
    return {"data": await get_url_json(f"{API_HEAD}/customers/{id}/accounts?key={API_KEY}")}

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
    return {"data": await get_url_json(f"{API_HEAD}/customers/{id}/bills?key={API_KEY}")}

# transfer endpoints
@app.get("/accounts/{id}/transfers")
async def read_account_transfers(id: str, type: str) -> dict:
    return {"data": await get_url_json(f"{API_HEAD}/accounts/{id}/transfers?type={type}&key={API_KEY}")}

# purchase endpoints
@app.get("/accounts/{id}/purchases")
async def read_account_purchases(id:str) -> dict:
    return {"data": await get_url_json(f"{API_HEAD}/accounts/{id}/purchases?key={API_KEY}")}

# deposit endpoints
@app.get("/accounts/{id}/deposits")
async def read_account_deposits(id: str) -> dict:
    return {"data": await get_url_json(f"{API_HEAD}/accounts/{id}/deposits?key={API_KEY}")}

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
            json = account.model_dump()
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

@app.post("/customers/{id}/accounts")
async def post_customer_accounts(id: str, account: Account) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_HEAD}/customers/{id}/accounts?key={API_KEY}",
            json = account.model_dump()
        ) as resp:
            return {"data": await resp.json()}