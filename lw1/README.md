# Лабораторная работа №1
**Цель**: 
- Изучить основные возможности языка Python для разработки программных систем с интерфейсом командной строки (CLI)
-  Разработать программную систему на языке Python согласно описанию предметной области

**Задача**:

**Модель мониторинга финансов 81**

**Предметная область**: отслеживание и анализ финансовых операций.

**Важные сущности**: банковские счета, транзакции, бюджет, инвестиции, отчеты.

**Операции**: операция внесения и снятия денег, операция анализа расходов и доходов, операция инвестирования и управления портфелем, операция формирования бюджета, операция генерации финансовых отчетов.

<hr>

### Класс **Budget**
Представляет собой бюджет, предназначенный для хранения денежных средств
#### Свойства:
- `money_amount` - количество денежных средств

#### Методы:
- `__init__(self, money_amount: float = 0.0)` - создает бюджет с указанной суммой
- `get_money_amount(self) -> float` - получение суммы, хранящейся на балансе
- `set_money_amount(self, new_amount: float) -> None` - установка значения суммы, хранящейся на балансе

Выбрасывает исключения: **ValueError**

<hr>

### Класс **Transaction**
Представляет собой транзакцию
#### Свойства
- `money_amount_spent: float` - количество потраченных денег
- `company_or_bank_account_number: float` - название компании либо номера банковского счета, чья транзацкия
- `correct_operation` - была ли завершена транзакция

#### Методы
- `__init__(self, money_amount_spent: float = 0.0, company_or_bank_account_number: str = '', correct_operation: bool = True)` - создать бюджет с указанными свойствами
- `get_money_amount_spent(self) -> float` - получение количества потраченных денег
- `get_company_or_bank_account_number(self) -> str` - получение названия компании либо банковского счета
- `get_correct_operation(self) -> bool` - получение значения корректности операции
- `set_money_amount_spend(self, money_amount: float = 0.0) -> None` - установка значения потраченного количества денег
- `set_correct_operation(self, correct: bool = True) -> None` - установка значения корректности операции

Выбрасывает исключения: **ValueError**

<hr>

### Класс **Investment**
Представляет собой инвестицию
#### Свойства
- `scope_of_investment: str` - сфера инвестирования
- `price` - вложенные средства
- `risk` - риск потери средств
- `profit_ratio` - коэффициент прибыли

#### Методы
- `__init__(self, scope_of_investment: str = 'NoName Company', price: float = 0.0, risk: float = 0.0, profit_ratio: float = 0.0)` - создание инвестиции с указанными свойствами
- `risk_changing(self, increasing: bool = True) -> None` - изменение риска, `increasing` отвечает за увеличение/уменьшение параметра
- `profit_ratio_changing(self, increasing: bool = True) -> None` - изменение коэффициента прибыли, `increasing` отвечает за увеличение/уменьшение параметра
- `get_scope_of_investment(self) -> str` - получение сферы инвестирования
- `get_price(self) -> float` - получение вложенных средств
- `get_risk(self) -> float` - получение риска
- `get_profit_ratio(self) -> float` - получение коэффициента прибыли
- `set_price(self, money_amount: float) -> None` - установка вложенных средств
- `__eq__(self, other) -> bool` - оператор сравнения

Выбрасывает исключения: **ValueError**

<hr>

### Класс **Report**
Представляет собой отчет
#### Свойства
- `text` - текст
- `date` - дата

#### Методы
- `__init__(self, text='Classic report without information', date='01.01.01')` - создание отчета с указанными текстом и датой
- `form_analysis_text(self, transaction_history: list = None, investments: list = None, owner_name: str = '') -> None:` - формирование текста анализа на основе истории транзакций и текущих инвестициях
- `form_financial_report_text(self, balance: float = 0, transactions_amount: int = 0, investments_amount: int = 0, owner_name: str = 'Tyler') -> None` - формирование финансового отчета на основе текущего баланса, количестве совершенных транзакций и количестве инвестиций
- `get_text(self) -> str` - получение текста отчета

<hr>

### Класс **FinancialManagementSystem**
Представляет собой систему управления финансами, которая хранит всевозможные транзакции и интвестиции
#### Свойства
- `possible_investments: list` - возможные инвестиции
- `possible_transactions: list` - возможные транзакции

#### Методы
- `def __init__(self, possible_investments: list = None, possible_transactions: list = None)` - создание системы управления финансами с указанными возможными операциями
- `investment_changing(self, investment: Investment = Investment()) -> None` - изменение инвестиции, а именно показателей риска и прибыли
- `get_possible_transactions(self) -> list` - получение возможных транзакций
- `get_possible_investments(self) -> list` - поулчение возможных инвестиций

Выбрасывает исключения: **ValueError**

<hr>

### Класс **InvestmentPortfolio**
Представляет собой инвестиционный портфель
#### Свойства
- `investments: list` - текущие инвестиции

#### Методы
- `__init__(self, investments: list = None)` - создание инвестиционного портфеля с указанными инвестициями
- `assert_allocation(self, investment: Investment = Investment()) -> None` - распределение активов
- `diversification(self, investment: Investment = Investment()) -> None` - диверсификация
- `risk_tolerance(self, investment: Investment = Investment()) -> None` - толерантность к риску
- `balance(self, investment: Investment = Investment()) -> None` - перебалансировка
- `end_investment(self, investment: Investment = Investment()) -> float` - окончание инвестиции с получением прибыли
- `remove_investment(self, investment: Investment = Investment) -> None` - окончание инвестиции в связи с потерей средств
- `add_new_investment(self, investment: Investment = Investment()) -> None` - добавление новой инвестиции в портфель
- `get_investments(self) -> list` - получение текущих инвестиций

Выбрасывает исключения: **ValueError**

<hr>

### Класс **BankAccount**
Представляет собой банковский аккаунт
#### Свойства
- `unique_number: str` - уникальный номер
- `owner_name: str` - имя владельца
- `budget: Budget` - бюджет
- `transactions_history: list` - история транзакций
- `investment_portfolio: InvestmentPortfolio` - инвестиционный портфель

#### Методы
- `__init__(self, unique_number: str = '0000', owner_name: str = 'Tyler', budget: Budget = Budget(), transactions_history: list = None, investment_portfolio: InvestmentPortfolio = InvestmentPortfolio()):` - создание банковского аккаунта с указанными свойствами
- `deposit(self, money_amount: float = 0.1) -> None` - внесение средств
- `withdrawal(self, money_amount: float = 0.1) -> None` - снятие средств
- `make_transaction(self, transaction: Transaction = Transaction(), money_amount: float = 0.0) -> None:` - совершение транзакции
- `make_investment(self, investment: Investment = Investment(), money_amount: float = 0.0) -> None` - совершение инвестиции
- `portfolio_management(self, investment: Investment = Investment(), operation_code: str = '1') -> None` - управление инвестиционным портфелем, где `operation_key` отвечает за операцию, которую может совершать экземпляр класса `InvestmentPortfolio`
- `form_new_budget(self, withdrawing_money: bool = False) -> None` - формирование нового бюджета
- `get_analysis(self) -> Report` - получение анализа банковского аккаунта
- `get_financial_report(self) -> Report` - получение финансового отчета о банковском аккаунте
- `investment_removing(self, investment: Investment = Investment()) -> None` - завершение инвестиции, связанное с потерей средств
- `get_unique_number(self) -> str` - получение уникального номера
- `get_owner_name(self) -> str` - получение имени владельца
- `get_transactions_history(self) -> list` - получение истории транзакций
- `get_investment_portfolio(self) -> InvestmentPortfolio` - получение инвестиционного портфеля
- `get_balance(self) -> float` - получение текущего баланса

Выбрасывает исключения: **ValueError**
