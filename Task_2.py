from config import ALPACA_CONFIG
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

class SwingHigh(Strategy):
    data = []
    order_number = 0
    def initialize(self):
        self.sleeptime = "10S"


    def on_trading_iteration(self):
        symbol = "GOOG"
        entry_price = self.get_last_price(symbol)
        self.log_message(f"Position: {self.get_position(symbol)}")
        self.data.append(self.get_last_price(symbol))

        if len(self.data) > 3:
            temp = self.data[-3:]
            if temp[-1] > temp[1] > temp[0]:
                self.log_message(f"Last 3 prints: {temp}")
                order = self.create_order(symbol, quantity = 1, side = "buy")
                self.submit_order(order)
                self.order_number += 1
                if self.order_number == 1:
                    self.log_message(f"Entry price: {temp[-1]}")
                    entry_price = temp[-1] # filled price
            if self.get_position(symbol) and self.data[-1] < entry_price * .995:
                self.sell_all()
                self.order_number = 0
            elif self.get_position(symbol) and self.data[-1] >= entry_price * 1.015:
                self.sell_all()
                self.order_number = 0


    def before_market_closes(self):
        self.sell_all()
    def stop_trading(self):
        print("Stopping trading.")
        self.stop_signal = True


if __name__ == "__main__":
    try:
    # Initialize the Alpaca broker with the configuration dictionary
        broker = Alpaca(ALPACA_CONFIG)

    # Create and configure your strategy
        strategy = SwingHigh(broker=broker)

    # Initialize the trader and add the strategy
        trader = Trader()
        trader.add_strategy(strategy)

    # Run the trader
        trader.run_all()

    except Exception as e:
        print(f"Error: {e}")


"""from config import ALPACA_CONFIG
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

class square(Strategy):
    def on_trading_iteration(self):
        symbol = 'GOOG'
        self.sell_all(symbol)

if __name__ == '__main__':
    broker = Alpaca(ALPACA_CONFIG)
    strategy = square(broker=broker)
    trader = Trader()
    trader.add_strategy(strategy)
    trader.run_all()"""