from collections import defaultdict

class Orderbook:
    def __init__(self):
        # Bids (buy orders) and Asks (sell orders) will hold prices and quantities
        self.bids = defaultdict(float)  # Dictionary for bid prices and quantities
        self.asks = defaultdict(float)  # Dictionary for ask prices and quantities

    def update(self, data):
        """Update the orderbook with new bid and ask data."""
        print("Incoming data:", data)  # Debugging: See incoming raw data

        # Clear existing bids and asks to refresh the orderbook with new data
        self.bids.clear()
        self.asks.clear()

        # Populate bids (sorted highest to lowest)
        for price, qty in data.get('Bids', []):
            if float(qty) > 0:  # Only consider non-zero quantities
                self.bids[float(price)] = float(qty)

        # Populate asks (sorted lowest to highest)
        for price, qty in data.get('Asks', []):
            if float(qty) > 0:  # Only consider non-zero quantities
                self.asks[float(price)] = float(qty)

        print("Updated Bids:", dict(self.bids))  # Debugging: See the updated bids
        print("Updated Asks:", dict(self.asks))  # Debugging: See the updated asks

    def calculate_price(self, quantity):
        """
        Calculate the price in ZAR for a given quantity of USDT by going through the orderbook's asks.
        This assumes you're buying USDT, so we aggregate from the lowest price ask upwards.
        """
        total_cost = 0.0
        qty_remaining = quantity

        # Sort asks by price (ascending)
        sorted_asks = sorted(self.asks.items())

        for price, qty in sorted_asks:
            if qty_remaining <= 0:
                break  # We have bought enough USDT

            if qty <= qty_remaining:
                # Buy all available USDT at this price
                total_cost += price * qty
                qty_remaining -= qty
            else:
                # Buy the remaining USDT needed at this price
                total_cost += price * qty_remaining
                qty_remaining = 0

        # If we couldn't fully satisfy the order, return the cost for what we could satisfy
        return total_cost if quantity > 0 else 0
