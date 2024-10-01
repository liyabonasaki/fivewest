from collections import defaultdict

class Orderbook:
    def __init__(self):
        # Bids (buy orders) and Asks (sell orders) will hold prices and quantities
        self.bids = defaultdict(float)
        self.asks = defaultdict(float)

    def update(self, data):
        """Update the orderbook with new bid and ask data."""
        print("Incoming data:", data)

        # Clear existing bids and asks to refresh the orderbook with new data
        self.bids.clear()
        self.asks.clear()

        # Populate bids (sorted highest to lowest)
        for bid in data.get('Bids', []):
            price = float(bid['price'])
            quantity = float(bid['quantity'])
            if quantity > 0:  # Only consider non-zero quantities
                self.bids[price] = quantity

        # Populate asks (sorted lowest to highest)
        for ask in data.get('Asks', []):
            price = float(ask['price'])
            quantity = float(ask['quantity'])
            if quantity > 0:  # Only consider non-zero quantities
                self.asks[price] = quantity

        print("Updated Bids:", dict(self.bids))
        print("Updated Asks:", dict(self.asks))

    def calculate_price(self, quantity):
        """Calculate the total cost for the given quantity using the ask prices."""
        total_cost = 0.0
        qty_remaining = quantity

        # Sort asks by price (to get the best offers first)
        sorted_asks = sorted(self.asks.items())
        print("Sorted Asks for Calculation:", sorted_asks)

        for price, qty in sorted_asks:
            if qty_remaining <= 0:
                break
            if qty <= qty_remaining:
                total_cost += price * qty
                qty_remaining -= qty
            else:
                total_cost += price * qty_remaining
                qty_remaining = 0

            print(f"Price: {price}, Qty: {qty}, Total Cost So Far: {total_cost}, Qty Remaining: {qty_remaining}")

        # Return the total cost only if all quantity is fulfilled, otherwise 0
        return total_cost if quantity > 0 and qty_remaining == 0 else 0
