from Order import Order

class Check:

    def __init__(self, order: Order, order_succeed: bool) -> None:
        self._order = order
        self._order_succeed = order_succeed
    
    def generate_check(self) -> None:
        total_cost = sum(item.getPrice() for item in self._order._list_order)
        print("======= Чек =======")
        if self._order_succeed:
            print("Статус заказа: Успешно")
        else:
            print("Статус заказа: Средств недостаточно")
        print("Позиции заказа:")
        for item in self._order._list_order:
            print(f"{item.getName()}: {item.getPrice()} руб.")
        print("===================")
        print(f"Итого: {total_cost} руб.")
