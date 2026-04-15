from datamodel import OrderDepth, TradingState, Order
from typing import List

class Trader:
    def run(self, state: TradingState):
        result = {}

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            # Your strategy logic here
            # e.g., buy cheap, sell high

            result[product] = orders

        # traderData = persist state between iterations (string)
        # conversions = for cross-exchange arbitrage
        return result, 0, ""