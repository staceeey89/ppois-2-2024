# Модель банковской карты

Документация для системы, описывающей работу с банковскими картами, банками и транзакциями

## Класс FinanceException

Класс исключений финансовой предметной области. Унаследован от Exception

## Класс Bank
Представляет банк, обслуживающий кредитные карты и хранящий историю транзакций между ними

### Методы

- \_\_init__(self, name: str)

Создает банк с указанным названием

- add_card(self, card: CreditCard) -> None

Добавляет указанную кредитную карту в банк.

- remove_card(self, card: CreditCard) -> None

Удаляет указанную кредитную карту из банка.

- get_cards(self) -> list[CreditCard]

Возвращает список кредитных карт, обслуживаемых банком.

- transfer(self, sender_card: CreditCard, receiver_card: CreditCard, pin: int, amount: int) -> None

Переводит amount денег с карты sender_card с пин-кодом pin на карту receiver_card внутри банка

Выбрасывает исключения FinanceException, ValueError

## Класс CardOwner

Представляет держателя карты

### Методы

- \_\_init__(self, name: str, address: str, email: Optional[str], phone: str):

Создает держателя карты с заданным именем, адресом, номером телефона и (опционально) эл. почтой

## Класс Transaction

Представляет банковскую транзакцию

### Методы

- \_\_init__(self, sender_card: CreditCard, receiver_card: CreditCard, amount: int, timestamp: datetime):

Создаёт транзакцию с картой отправителя, картой получателя, количеством переведенных средств, датой проводки


## Класс PaymentMean

Абстрактный класс, представляющий сущности для хранения и распоряжения денежными средствами

### Методы

- pay(self, amount: int, pin: Optional[int]) -> None:

Оплата услуги/товара

- deposit(self, amount: int) -> None:

Пополнение баланса

- withdraw(self, amount: int, pin: Optional[int]) -> None:

Списание средств с баланса

## Класс CreditCard

Унаследован от PaymentMean

### Методы

- \_\_init__(self,
                 card_number,
                 owner: CardOwner,
                 pin: int = random.randint(1000, 10000),
                 is_blocked: bool = False):

Создаёт кредитную карту с заданным владельцем, пин-кодом, номером и активным/неактивным состоянием

- deposit(self, amount: int) -> None:

Пополняет баланс карты на amount если карта не заблокирована

Выбрасывает исключения FinanceException, ValueError

- withdraw(self, amount: int, pin: int) -> None:

Снимает с баланса карты amount денег, если карта не заблокирована и указанный pin действителен

Выбрасывает исключения FinanceException, ValueError

- pay(self, amount: int, pin: int) -> None:

Снимает с баланса карты amount денег, если карта не заблокирована, не превышен разовый лимит по оплате и указанный pin действителен

Выбрасывает исключения FinanceException, ValueError

- get_balance(self, pin: int) -> int:

Возвращает баланс карты при действительном пин-коде

Выбрасывает исключения FinanceException

- is_blocked(self) -> bool:

Возвращает флаг, заблокирована ли карта

- block(self) -> None:

Блокирует карту

- unblock(self) -> None:

Разблокирует карту

- change_pin(self, new_pin: int) -> None:

Меняет текущий пин-код на заданный, если новый принадлежит диапазону [1000, 9999]

Выбрасывает исключение ValueError

- set_limit(self, pin: int, new_limit: int) -> None:

Устанавливает новый лимит разовой оплаты при верно указанном пин-коде и неотрицательном значении new_limit

Выбрасывает исключения FinanceException, ValueError
