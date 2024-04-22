import unittest
from Inventory import Inventory

class TestInventory(unittest.TestCase):
    
    def test_initialization_with_ingredients(self):
        inventory = Inventory(["bread", "cheese", "tomato"])
        self.assertEqual(inventory.getItems(), ["bread", "cheese", "tomato"])
        
    def test_initialization_without_ingredients(self):
        inventory = Inventory()
        self.assertEqual(inventory.getItems(), [])
        
    def test_add_item(self):
        inventory = Inventory()
        inventory.addItem("fish")
        self.assertEqual(inventory.getItems(), ["fish"])
        
    def test_add_multiple_items(self):
        inventory = Inventory()
        inventory.addItem("cheese")
        inventory.addItem("ham")
        inventory.addItem("bread")
        self.assertEqual(inventory.getItems(), ["cheese", "ham", "bread"])
        
if __name__ == '__main__':
    unittest.main()
