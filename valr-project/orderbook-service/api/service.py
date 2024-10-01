import asyncio
import json
import websockets
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

async def ping_periodically(websocket):
    """Send periodic ping messages to keep the WebSocket connection alive."""
    while True:
        try:
            await websocket.ping()
            await asyncio.sleep(30)  # Ping every 30 seconds
        except Exception as e:
            print(f"Ping failed: {e}")
            break


async def stream_orderbook():
    uri = "wss://api.valr.com/ws/trade"

    while True:  # Reconnection loop
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to VALR Websocket")

                # Subscribe to the FULL_ORDERBOOK_UPDATE event
                await websocket.send(json.dumps({
                    "type": "SUBSCRIBE",
                    "subscriptions": [
                        {"event": "FULL_ORDERBOOK_UPDATE", "currencyPair": "USDTZAR"}
                    ]
                }))

                # Start periodic pings to keep the connection alive
                asyncio.create_task(ping_periodically(websocket))

                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    print("Incoming data:", data)

                    # Ensure the data contains the bids and asks structure
                    if 'Bids' in data and 'Asks' in data:
                        orderbook.update(data)  # Update your orderbook with the new data

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e.code}, {e.reason}. Reconnecting...")
            await asyncio.sleep(5)  # Wait 5 seconds before attempting to reconnect


# FastAPI lifecycle event to start WebSocket connection on app startup
@app.on_event("startup")
async def start_stream_orderbook():
    asyncio.create_task(stream_orderbook())  # Start the orderbook streaming in the background


@app.get("/price")
async def get_price(quantity: float):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    price = orderbook.calculate_price(quantity)
    print(f"Requested quantity: {quantity}, Calculated price: {price}")  # Debugging line
    return JSONResponse(content={"price": price})




