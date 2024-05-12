class RealEstateProperty:
    def __init__(self, address, price, description, num_rooms, repair_needed):
        self.price = price
        self.address = address
        self.interested_clients = []
        self.owner = None

    def __str__(self):
        return self.address

    def add_interested_client(self, client):
        self.interested_clients.append(client)

    def transfer_ownership(self, new_owner):
        self.owner = new_owner
        print(f"Собственность на объекте недвижимости {self.address} передана новому владельцу {new_owner}.")
