import unittest
from Food import Food

class TestFood(unittest.TestCase):
    
    def setUp(self):
        self.food = Food("Pizza", 10, "Delicious pizza", ["dough", "tomato sauce", "cheese"])
        
    def test_get_name(self):
        self.assertEqual(self.food.getName(), "Pizza")
        
    def test_set_name(self):
        self.food.setName("Pasta")
        self.assertEqual(self.food.getName(), "Pasta")
        
    def test_get_price(self):
        self.assertEqual(self.food.getPrice(), 10)
        
    def test_set_price(self):
        self.food.setPrice(15)
        self.assertEqual(self.food.getPrice(), 15)
        
    def test_get_description(self):
        self.assertEqual(self.food.getDescription(), "Delicious pizza")
        
    def test_set_description(self):
        self.food.setDescription("Tasty pasta")
        self.assertEqual(self.food.getDescription(), "Tasty pasta")
        
    def test_get_ingredients(self):
        self.assertEqual(self.food.getIngr(), ["dough", "tomato sauce", "cheese"])
        
if __name__ == '__main__':
    unittest.main()
