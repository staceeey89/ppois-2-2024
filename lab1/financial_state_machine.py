from statemachine import State
from statemachine import StateMachine

from typing import Optional

from finances.bank import Bank
from finances.card_owner import CardOwner
from finances.credit_card import CreditCard
from repository.interfaces import Repository
from repository.exceptions import RepositoryException
from finances.finance_exceptions import FinanceException
import helper


class FinancialStateMachine(StateMachine):
    view_banks = State(initial=True)
    view_bank = State()
    create_bank = State()
    delete_bank = State()
    view_card = State()
    create_card = State()
    delete_card = State()
    view_balance = State()
    deposit = State()
    withdraw = State()
    pay = State()
    transfer = State()
    change_pin = State()
    change_limit = State()
    toggle_block = State()
    exit_ = State(final=True)

    move_next = (
            exit_.from_(view_banks, cond="navigating_backwards")

            | view_banks.from_(view_bank, cond="navigating_backwards")
            | view_banks.to(view_bank, cond="navigating_by_index")

            | view_bank.from_(view_card, cond="navigating_backwards")
            | view_card.from_(view_bank, cond="navigating_by_index")

            | view_banks.to(create_bank, cond="navigating_create")
            | view_banks.from_(create_bank)

            | view_bank.from_(create_card)
            | view_bank.to(create_card, cond="navigating_create")

            | view_bank.to(delete_bank, cond="navigating_delete")
            | view_banks.from_(delete_bank)

            | view_card.to(view_balance, cond="navigating_balance")
            | view_card.from_(view_balance)

            | view_card.to(delete_card, cond="navigating_delete")
            | view_bank.from_(delete_card)

            | view_card.to(withdraw, cond="navigating_withdraw")
            | view_card.from_(withdraw)

            | view_card.to(deposit, cond="navigating_deposit")
            | view_card.from_(deposit)

            | view_card.to(transfer, cond="navigating_transfer")
            | view_card.from_(transfer)

            | view_card.to(pay, cond="navigating_pay")
            | view_card.from_(pay)

            | view_card.to(toggle_block, cond="navigating_toggle_block")
            | view_card.from_(toggle_block)

            | view_card.to(change_limit, cond="navigating_limit")
            | view_card.from_(change_limit)

            | view_card.to(change_pin, cond="navigating_pin")
            | view_card.from_(change_pin)

            # in case user enters invalid transition
            | view_card.to.itself(internal=True)
            | view_bank.to.itself(internal=True)
            | view_banks.to.itself(internal=True)
    )

    def __init__(self, repository: Repository):
        self.repository: Repository = repository

        try:
            loaded_state = repository.load()
            self.selected_index: Optional[int] = loaded_state[0]
            self.selected_bank: Optional[Bank] = loaded_state[1]
            self.selected_card: Optional[CreditCard] = loaded_state[2]
            self.banks: list[Bank] = loaded_state[3]
        except RepositoryException:
            print("Loading default values")
            self.selected_index: Optional[int] = None
            self.selected_bank: Optional[Bank] = None
            self.selected_card: Optional[CreditCard] = None
            self.banks: list[Bank] = []

        super().__init__()

    def navigating_backwards(self, input_: str) -> bool:
        return input_ == 'q'

    def navigating_balance(self, input_: str) -> bool:
        return input_ == 'bal'

    def navigating_pay(self, input_: str) -> bool:
        return input_ == 'pay'

    def navigating_withdraw(self, input_: str) -> bool:
        return input_ == 'wdr'

    def navigating_deposit(self, input_: str) -> bool:
        return input_ == 'dep'

    def navigating_pin(self, input_: str) -> bool:
        return input_ == 'pin'

    def navigating_toggle_block(self, input_: str) -> bool:
        return input_ == 'blc'

    def navigating_limit(self, input_: str) -> bool:
        return input_ == 'lim'

    def navigating_transfer(self, input_: str) -> bool:
        return input_ == 'trs'

    def navigating_create(self, input_: str) -> bool:
        return input_ == 'c'

    def navigating_delete(self, input_: str) -> bool:
        return input_ == 'd'

    def navigating_by_index(self, input_: str) -> bool:
        if input_.isnumeric():
            self.selected_index = int(input_)
            return True
        return False

    def on_enter_view_banks(self) -> None:
        self.selected_bank = None
        print("List of all banks:")
        for i in range(len(self.banks)):
            print(f"{i} - {self.banks[i].name}")

    def on_enter_create_bank(self) -> None:
        new_bank = Bank(input("Input bank name"))
        self.banks.append(new_bank)
        print("Bank created")
        self.move_next()

    def on_enter_create_card(self) -> None:
        card_number = input("Input card number")
        card_owner = CardOwner('Sample name', 'Sample address', None, 'Sample phone')
        card_pin: int = helper.input_numeric("PIN")

        try:
            new_card = CreditCard(card_number, card_owner, card_pin, False)
            self.selected_bank.add_card(new_card)
            print("Card created")
        except ValueError as e:
            print(str(e))
        finally:
            self.move_next()

    def on_enter_view_card(self) -> None:
        try:
            if self.selected_card is None:
                self.selected_card = self.selected_bank.get_cards()[self.selected_index]

            print("Card information")
            print(self.selected_card.card_number)
            print(self.selected_card.owner.name)
            if self.selected_card.is_blocked():
                print("BLOCKED")
        except IndexError:
            print("Invalid index")
            self.move_next('q')

    def on_enter_view_bank(self) -> None:
        self.selected_card = None
        try:
            if self.selected_bank is None:
                self.selected_bank = self.banks[self.selected_index]

            print(f"{self.selected_bank.name} information:")
            cards = self.selected_bank.get_cards()
            for i in range(len(cards)):
                print(f"{i} - {cards[i].card_number}; {cards[i].owner.name}")
        except IndexError:
            print("Invalid index")
            self.move_next('q')

    def on_enter_delete_bank(self) -> None:
        print("Deleting bank")
        self.banks.remove(self.selected_bank)
        self.selected_bank = None
        self.move_next()

    def on_enter_delete_card(self) -> None:
        print("Deleting card")
        self.selected_bank.remove_card(self.selected_card)
        self.selected_card = None
        self.move_next()

    def on_enter_withdraw(self) -> None:
        input_amount: int = helper.input_numeric("withdraw amount")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.selected_card.withdraw(input_amount, input_pin)
            print("Withdrawal successful")
        except FinanceException as e:
            print(str(e))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_view_balance(self) -> None:
        input_pin: int = helper.input_numeric("PIN")

        try:
            balance: int = self.selected_card.get_balance(input_pin)
            print(f"Balance: {balance}")
        except FinanceException as e:
            print(str(e))
        finally:
            self.move_next()

    def on_enter_deposit(self) -> None:
        input_amount: int = helper.input_numeric("deposit amount")

        try:
            self.selected_card.deposit(input_amount)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_pay(self) -> None:
        input_amount: int = helper.input_numeric("pay amount")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.selected_card.pay(input_amount, input_pin)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_transfer(self) -> None:
        input_receiver: str = input("receiver card number")
        receiver_card = next((x for x in self.selected_bank.get_cards() if x.card_number == input_receiver), None)
        if receiver_card is None:
            print("No such card found")
            self.move_next()
            return

        input_amount: int = helper.input_numeric("transfer amount")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.selected_bank.transfer(self.selected_card, receiver_card, input_pin, input_amount)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_toggle_block(self) -> None:
        if self.selected_card.is_blocked():
            self.selected_card.unblock()
            print("Card unblocked")
        else:
            self.selected_card.block()
            print("Card blocked")

        self.move_next()

    def on_enter_change_limit(self) -> None:
        input_amount: int = helper.input_numeric("payment limit")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.selected_card.set_limit(input_amount, input_pin)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_change_pin(self) -> None:
        input_pin: int = helper.input_numeric("new PIN")

        try:
            self.selected_card.set_pin(input_pin)
        except ValueError as e:
            print(str(e))
        finally:
            self.move_next()

    def before_move_next(self):
        print()

    def on_enter_exit_(self):
        print("Saving state and exiting...")
        self.repository.save([self.selected_index,
                              self.selected_bank,
                              self.selected_card,
                              self.banks])
        exit()
