import pickle
from RealEstateAgency import RealEstateAgency
from RealEstateProperty import RealEstateProperty
from Agent import Agent
from Client import Client
from Document import Document
from Deal import Deal

def create_client():
    name = input("Введите имя клиента: ")
    return Client(name)

def create_agent():
    name = input("Введите имя агента: ")
    return Agent(name)

def create_property():
    address = input("Введите адрес недвижимости: ")
    price = float(input("Введите цену недвижимости: "))
    description = input("Введите описание недвижимости: ")
    bedrooms = int(input("Введите количество спален: "))
    is_sold = input("Недвижимость продана (да/нет): ").lower() == 'да'
    return RealEstateProperty(address, price, description, bedrooms, is_sold)

def create_deal(properties, clients, agents):
    print("\nВыберите недвижимость для сделки:")
    for i, property_ in enumerate(properties, 1):
        print(f"{i}. {property_}")
    property_index = int(input("Введите номер недвижимости: ")) - 1

    print("\nВыберите клиента для сделки:")
    for i, client in enumerate(clients, 1):
        print(f"{i}. {client.name}")
    client_index = int(input("Введите номер клиента: ")) - 1

    print("\nВыберите агента для сделки:")
    for i, agent in enumerate(agents, 1):
        print(f"{i}. {agent.name}")
    agent_index = int(input("Введите номер агента: ")) - 1

    documents = [Document("Договор купли-продажи", "...")]
    return Deal(properties[property_index], clients[client_index], agents[agent_index], documents)

def save_data(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_data(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def main():
    clients = load_data('clients.pkl')
    agents = load_data('agents.pkl')
    properties = load_data('properties.pkl')

    if not clients:
        clients.append(create_client())
    if not agents:
        agents.append(create_agent())
    if not properties:
        properties.append(create_property())

    deals = []
    while True:
        print("\nМеню:")
        print("1. Создать клиента")
        print("2. Создать агента")
        print("3. Создать недвижимость")
        print("4. Создать сделку")
        print("5. Завершить ввод и вывести информацию")
        choice = input("Выберите действие: ")

        if choice == '1':
            clients.append(create_client())
        elif choice == '2':
            agents.append(create_agent())
        elif choice == '3':
            properties.append(create_property())
        elif choice == '4':
            if clients and agents and properties:
                deals.append(create_deal(properties, clients, agents))
            else:
                print("Сначала необходимо создать как минимум одного клиента, агента и недвижимость.")
        elif choice == '5':
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

    # Инициализация агентства по недвижимости
    agency = RealEstateAgency()

    # Добавление клиентов, агентов, объектов недвижимости и сделок в агентство
    for client in clients:
        agency.add_client(client)
    for agent in agents:
        agency.add_agent(agent)
    for property_ in properties:
        agency.add_property(property_)
    for deal in deals:
        agency.add_deal(deal)

    # Вывод информации о клиентах и сделках в консоль
    print("\nИнформация о клиентах:")
    for client in clients:
        print(f"Клиент: {client.name}")

    print("\nИнформация о сделках:")
    for i, deal in enumerate(deals, 1):
        print(f"Сделка {i}: {deal}")

    # Сохранение данных
    save_data(clients, 'clients.pkl')
    save_data(agents, 'agents.pkl')
    save_data(properties, 'properties.pkl')
    save_data(deals, 'deals.pkl')

    print("Программа завершена.")

if __name__ == "__main__":
    main()
