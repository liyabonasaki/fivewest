# fivewest

USDT/ZAR Orderbook Monitoring System

This project consists of two components:

varl-project: Monitors and processes real-time data from VALR exchange's USDT/ZAR orderbook using WebSockets and provides an API to retrieve prices.


valr-frontend: A React-based application that interacts with the backend API to display calculated prices based on user input.


Backend Project
Features

    Connects to VALR's WebSocket to receive real-time USDT/ZAR orderbook data.
    Provides a REST API endpoint to calculate the total price for a given USDT quantity based on the current orderbook data.
    Utilizes FastAPI for the API and WebSockets for real-time data streaming.

Tech Stack

    Python (FastAPI, WebSockets, AsyncIO)
    VALR API (WebSocket streaming for orderbook data)
    Docker (Optional for containerization)

Requirements

    Python 3.9+
    poetry (Python package installer or dependency manager)

Frontend Project
Tech Stack

    React (Create React App)
    Axios (for API requests)
    HTML/CSS/JavaScript

Requirements

    Node.js 14+ (with npm)