import unittest
from Order import Order
from Food import Food

class TestOrder(unittest.TestCase):
    
    def setUp(self):
        self.order = Order()
        
    def test_initialization(self):
        self.assertEqual(self.order.getTheOrder(), [])
        
    def test_add_to_order_with_available_ingredients(self):
        dish = Food("Pizza", 10, "Delicious pizza", ["dough", "tomato sauce", "cheese"])
        ingredients = ["dough", "tomato sauce", "cheese", "pepperoni"]
        self.order.addToOrder(dish, ingredients)
        self.assertEqual(self.order.getTheOrder(), [dish])
        
    def test_remove_existing_item(self):
        dish = Food("Pizza", 10, "Delicious pizza", ["dough", "tomato sauce", "cheese"])
        self.order.addToOrder(dish, ["dough", "tomato sauce", "cheese", "pepperoni"])
        self.order.removeItem(dish)
        self.assertEqual(self.order.getTheOrder(), [])
        
    def test_remove_nonexistent_item(self):
        dish1 = Food("Pizza", 10, "Delicious pizza", ["dough", "tomato sauce", "cheese"])
        dish2 = Food("Burger", 15, "Juicy burger", ["bun", "patty", "cheese", "lettuce"])
        self.order.addToOrder(dish1, ["dough", "tomato sauce", "cheese", "pepperoni"])
        result = self.order.removeItem(dish2)
        self.assertEqual(result, "No such dish in order")
        self.assertEqual(self.order.getTheOrder(), [dish1])
        
if __name__ == '__main__':
    unittest.main()
