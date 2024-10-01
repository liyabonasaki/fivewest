import asyncio
import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .orderbook import Orderbook
from .config import origins

app = FastAPI()
orderbook = Orderbook()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

VALR_ORDERBOOK_URL = "https://api.valr.com/v1/public/USDTZAR/orderbook"

async def fetch_orderbook():
    """Fetches the orderbook data from the VALR REST API and updates the Orderbook."""
    while True:
        try:
            response = requests.get(VALR_ORDERBOOK_URL)
            if response.status_code == 200:
                data = response.json()
                print("Incoming data:", data)  # Debugging line

                # Ensure the data contains the bids and asks structure
                if 'Bids' in data and 'Asks' in data:
                    orderbook.update(data)  # Update the orderbook with the fetched data
            else:
                print(f"Failed to fetch orderbook: {response.status_code} {response.text}")

        except Exception as e:
            print(f"Error fetching orderbook: {e}")

        await asyncio.sleep(30)  # Fetch the orderbook every 30 seconds



@app.on_event("startup")
async def start_fetch_orderbook():
    asyncio.create_task(fetch_orderbook())  # Start the orderbook fetching task in the background


@app.get("/price")
async def get_price(quantity: float):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    price = orderbook.calculate_price(quantity)
    print(f"Requested quantity: {quantity}, Calculated price: {price}")  # Debugging line
    return JSONResponse(content={"price": price})
