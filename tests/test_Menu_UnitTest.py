import unittest
from Menu import Menu

class TestMenu(unittest.TestCase):
    
    def test_initialization(self):
        menu = Menu()
        self.assertEqual(menu.getItems(), [])
        
    def test_add_item(self):
        menu = Menu()
        menu.addItem("Pizza")
        self.assertEqual(menu.getItems(), ["Pizza"])
        
    def test_remove_existing_item(self):
        menu = Menu()
        menu.addItem("Pizza")
        menu.addItem("Burger")
        menu.removeItem("Pizza")
        self.assertEqual(menu.getItems(), ["Burger"])
        
    def test_remove_nonexistent_item(self):
        menu = Menu()
        menu.addItem("Pizza")
        result = menu.removeItem("Pasta")
        self.assertEqual(result, "No such dish in menu")
        self.assertEqual(menu.getItems(), ["Pizza"])
        
if __name__ == '__main__':
    unittest.main()
