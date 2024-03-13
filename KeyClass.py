class Key:
    __doc__ = "class for keeping an algorythm key"

    key: int = None

    def __init__(self, key: int):
        self.key = key

    def manage_keys(self):
        print(" 1 - change your key, 2 - see your key")
        choice: int = int(input())
        if choice == 1:
            print("Enter the previous key ->")
            if int(input()) == self.key:
                print("Enter new Key ->")
                self.key = int(input())
            else:
                print("wrong key")
        else:
            if choice == 2:
                print("Your key = ", self.key)
