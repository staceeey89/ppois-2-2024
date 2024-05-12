from Document import Document

class RealEstateAgency:
    def __init__(self):
        self.agents = []
        self.clients = []
        self.properties = []
        self.documents = []
        self.deals = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_client(self, client):
        self.clients.append(client)

    def add_property(self, property):
        self.properties.append(property)

    def add_document(self, document):
        self.documents.append(document)

    def add_deal(self, deal):
        self.deals.append(deal)

    def search_properties(self, criteria):
        matching_properties = []
        for property in self.properties:
            is_match = True
            for key, value in criteria.items():
                if getattr(property, key) != value:
                    is_match = False
                    break
            if is_match:
                matching_properties.append(property)
        return matching_properties

    def schedule_viewing(self, deal, client):
        property = deal.property
        property.add_interested_client(client)
        print(f"Клиент {client} запросил просмотр объекта недвижимости {property}. Уведомление агенту {deal.agent}.")

    def assess_market_value(self, property):
        price_per_room = 50000
        repair_factor = 1.0
        if property.repair_needed:
            repair_factor = 0.8
        market_value = price_per_room * property.num_rooms * repair_factor
        return market_value

    def finalize_deal(self, deal):
        self.deals.append(deal)
        print(f"Сделка {deal} успешно заключена! Уведомление агенту {deal.agent} и клиенту {deal.client}.")

        for document in deal.documents:
            prepared_document = self.prepare_document(document)
            deal.client.receive_document(prepared_document)

        deal.property.transfer_ownership(deal.client)
        deal.agent.receive_commission(deal.property.price)

    def prepare_documents(self):
        # Подготавливаем документы для сделки
        documents = [Document("Договор купли-продажи", "..."), Document("Право собственности", "...")]
        return documents

    def prepare_document(self, document):
        # Подготавливаем документ (например, заполняем его содержимое)
        prepared_document = Document(document.name, "Заполнение содержимого")
        prepared_document.sign()
        return prepared_document

    def set_agent_for_property(self, property, agent):
        property.agent = agent

    def set_documents_for_property(self, property, documents):
        property.documents = documents
