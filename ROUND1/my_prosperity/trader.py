from datamodel import OrderDepth, TradingState, Order
from typing import List

class Trader:

    # ── Constants derived from your exploratory analysis ──────────────────
    OSMIUM_FAIR_VALUE = 10000   # from: osmium mean ≈ 10000
    OSMIUM_EDGE = 2             # place orders 2 away from fair value
    OSMIUM_LIMIT = 50           # check competition wiki for actual limit

    PEPPER_LIMIT = 50           # check competition wiki for actual limit

    def run(self, state: TradingState):
        result = {}

        for product, order_depth in state.order_depths.items():

            orders: List[Order] = []
            position = state.position.get(product, 0)

            # ── ASH_COATED_OSMIUM: market make around 10,000 ──────────────
            if product == "ASH_COATED_OSMIUM":
                fv = self.OSMIUM_FAIR_VALUE
                limit = self.OSMIUM_LIMIT

                buy_capacity  = limit - position   # how much more we can buy
                sell_capacity = limit + position   # how much more we can sell

                # Hit any asks below fair value (free money)
                for ask_price, ask_vol in sorted(order_depth.sell_orders.items()):
                    if ask_price < fv and buy_capacity > 0:
                        qty = min(-ask_vol, buy_capacity)
                        orders.append(Order(product, ask_price, qty))
                        buy_capacity -= qty

                # Hit any bids above fair value (free money)
                for bid_price, bid_vol in sorted(order_depth.buy_orders.items(), reverse=True):
                    if bid_price > fv and sell_capacity > 0:
                        qty = min(bid_vol, sell_capacity)
                        orders.append(Order(product, bid_price, -qty))
                        sell_capacity -= qty

                # Post passive orders to earn the spread
                if buy_capacity > 0:
                    orders.append(Order(product, fv - self.OSMIUM_EDGE, buy_capacity))
                if sell_capacity > 0:
                    orders.append(Order(product, fv + self.OSMIUM_EDGE, -sell_capacity))

            # ── INTARIAN_PEPPER_ROOT: always be max long ──────────────────
            elif product == "INTARIAN_PEPPER_ROOT":
                limit = self.PEPPER_LIMIT
                buy_capacity = limit - position

                # Buy as much as possible at the best available prices
                for ask_price, ask_vol in sorted(order_depth.sell_orders.items()):
                    if buy_capacity <= 0:
                        break
                    qty = min(-ask_vol, buy_capacity)
                    orders.append(Order(product, ask_price, qty))
                    buy_capacity -= qty

            result[product] = orders

        return result, 0, ""