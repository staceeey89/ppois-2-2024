# Asset

**Abstract class representing a financial asset**

## Attributes

- `symbol`: str, the unique identifier of the asset
- `name`: str, the name of the asset

## Methods

- `__init__(self, symbol, name)`: initialize the asset with a symbol and name
- `__eq__(self, other)`: check if two assets have the same symbol
- `__hash__()`: return the hash value of the symbol
- `symbol`: getter for the symbol
- `symbol(value)`: setter for the symbol
- `name`: getter for the name
- `name(value)`: setter for the name
- `info(self) -> str`: return a string representation of the asset's information (to be implemented in subclasses)

# Bond

The `Bond` class represents a financial asset that extends the `Stock` class.

## Attributes

- `symbol`: str - The unique identifier of the bond.
- `name`: str - The name of the bond.
- `price`: float - The price of the bond.
- `maturity_date`: date - The date when the bond matures.

## Methods

- `__init__(symbol: str, name: str, price: float, maturity_date: date)`: Initializes a new `Bond` object with the given symbol, name, price, and maturity date.
- `__eq__(other)`: Compares this bond to another bond for equality based on symbol and maturity date.
- `__hash__()`: Returns a hash value for the bond based on its symbol and maturity date.
- `maturity_date`: property - Gets the maturity date of the bond.
- `maturity_date(value: date)`: setter - Sets the maturity date of the bond.
- `info() -> str`: Returns a string representation of the bond.

# Broker

The `Broker` class represents a financial broker that operates in various stock exchanges and deals with different types of assets.

## Properties

* `name`: str
    The name of the broker.
* `license_number`: str
    The license number of the broker.
* `exchanges`: set[StockExchange]
    The set of stock exchanges where the broker operates.
* `commission`: float
    The commission rate charged by the broker.

## Methods

* `__init__(self, name: str, license_number: str, exchanges: set[StockExchange], commission: float)`
    Initializes a new `Broker` object with the given name, license number, set of stock exchanges, and commission rate.
* `name(self) -> str`
    Returns the name of the broker.
* `license_number(self) -> str`
    Returns the license number of the broker.
* `exchanges(self) -> set[StockExchange]`
    Returns the set of stock exchanges where the broker operates.
* `commission(self) -> float`
    Returns the commission rate charged by the broker.
* `name(self, value: str) -> None`
    Sets the name of the broker to the given value.
* `license_number(self, value: str) -> None`
    Sets the license number of the broker to the given value.
* `exchanges(self, value: set[StockExchange]) -> None`
    Sets the set of stock exchanges where the broker operates to the given value.
* `commission(self, value: float) -> None`
    Sets the commission rate charged by the broker to the given value.
* `info(self) -> str`
    Returns a string representation of the broker's information, including its name, license number, commission rate, the names of the stock exchanges where it operates, and the information of all the assets it deals with.
* `add_exchange(self, exchange: StockExchange) -> None`
    Adds a new stock exchange to the set of stock exchanges where the broker operates.
* `get_all_assets(self) -> set[Asset]`
    Returns the set of all assets that the broker deals with.
* `get_all_currencies(self) -> set[Currency]`
    Returns the set of all currencies that the broker deals with.
* `get_all_shares(self) -> set[Share]`
    Returns the set of all shares that the broker deals with.
* `get_all_bonds(self) -> set[Bond]`
    Returns the set of all bonds that the broker deals with.

## Exceptions

* `BrokerException`
    Raised when an attempt is made to add a stock exchange that is already in the set of stock exchanges where the broker operates.

# Currency

The `Currency` class represents a currency asset.

## Attributes

* `symbol` (str): The symbol of the currency.
* `name` (str): The name of the currency.
* `code` (int): The code of the currency.
* `exchange_rate` (float): The exchange rate of the currency.

## Methods

* `__init__(self, symbol: str, name: str, code: int, exchange_rate: float)`
    Initializes a new `Currency` object with the given symbol, name, code, and exchange rate.
* `__eq__(self, other)`
    Compares the currency with another object for equality.
* `__hash__(self)`
    Returns the hash value of the currency.
* `code(self) -> int`
    Returns the code of the currency.
* `exchange_rate(self) -> float`
    Returns the exchange rate of the currency.
* `code(self, new_code: int) -> None`
    Sets a new code for the currency.
* `exchange_rate(self, new_rate: float)`
    Sets a new exchange rate for the currency.
* `info(self) -> str`
    Returns a formatted string with information about the currency, including symbol, name, code, and exchange rate.

# Share

The `Share` class represents a share of a company.

## Attributes

* `symbol` (str): The symbol of the share.
* `name` (str): The name of the share.
* `price` (float): The current price of the share.

## Methods

* `__init__(self, symbol: str, name: str, price: float)`
    Initializes a new `Share` object with the given symbol, name, and price.
* `__eq__(self, other)`
    Compares the share with another object for equality.
* `__hash__(self)`
    Returns the hash value of the share.
* `info(self) -> str`
    Returns a formatted string with information about the share, including symbol, name, and price.

# Stock

The `Stock` class represents a stock asset.

## Attributes

* `symbol` (str): The symbol of the stock.
* `name` (str): The name of the stock.
* `price` (float): The current price of the stock.

## Methods

* `__init__(self, symbol: str, name: str, price: float)`
    Initializes a new `Stock` object with the given symbol, name, and price.
* `__eq__(self, other)`
    Compares the stock with another object for equality.
* `__hash__(self)`
    Returns the hash value of the stock.
* `price(self) -> float`
    Returns the current price of the stock.
* `price(self, price: float) -> None`
    Sets a new price for the stock.
* `info(self) -> str`
    Returns a formatted string with information about the stock, including symbol, name, and price.

# StockExchange

The `StockExchange` class represents a stock exchange.

## Attributes

* `name` (str): The name of the stock exchange.
* `assets` (set[Asset]): The set of assets traded in the stock exchange.

## Methods

* `__init__(self, name: str, assets: set[Asset])`
    Initializes a new `StockExchange` object with the given name and set of assets.
* `name(self) -> str`
    Returns the name of the stock exchange.
* `assets(self) -> set[Asset]`
    Returns the set of assets traded in the stock exchange.
* `name(self, value) -> None`
    Sets a new name for the stock exchange.
* `assets(self, value: set[Asset]) -> None`
    Sets a new set of assets for the stock exchange.
* `add_asset(self, asset: Asset) -> None`
    Adds a new asset to the stock exchange. Raises a `StockExchangeException` if the asset already exists in the stock exchange.

# Trader

The `Trader` class represents a trader.

## Attributes

* `name` (str): The name of the trader.
* `broker` (Broker): The broker used by the trader.
* `portfolio` (dict[Asset, int]): The portfolio of the trader, mapping assets to their quantities.
* `balance` (float): The balance of the trader.

## Methods

* `__init__(self, name: str, broker: Broker, portfolio: dict[Asset, int], balance: float)`
    Initializes a new `Trader` object with the given name, broker, portfolio, and balance.
* `name(self) -> str`
    Returns the name of the trader.
* `broker(self) -> Broker`
    Returns the broker used by the trader.
* `portfolio(self) -> dict[Asset, int]`
    Returns the portfolio of the trader, mapping assets to their quantities.
* `balance(self) -> float`
    Returns the balance of the trader.
* `name(self, name: str) -> None`
    Sets a new name for the trader.
* `broker(self, broker: Broker) -> None`
    Sets a new broker for the trader.
* `portfolio(self, portfolio: dict[Asset, int]) -> None`
    Sets a new portfolio for the trader, mapping assets to their quantities.
* `balance(self, balance: float) -> None`
    Sets a new balance for the trader.