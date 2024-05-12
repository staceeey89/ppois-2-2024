import unittest
from RealEstateAgency import RealEstateAgency
from RealEstateProperty import RealEstateProperty
from Agent import Agent
from Client import Client
from Document import Document
from Deal import Deal

class TestRealEstateAgency(unittest.TestCase):
    def setUp(self):
        self.agency = RealEstateAgency()
        self.agent = Agent("maks")
        self.client = Client("Alice")
        self.property = RealEstateProperty("123 Kirova St", 200000, "Beautiful house", 3, False)
        self.document = Document("Test Document", "Test Content")

    def test_add_agent(self):
        self.agency.add_agent(self.agent)
        self.assertIn(self.agent, self.agency.agents)

    def test_add_client(self):
        self.agency.add_client(self.client)
        self.assertIn(self.client, self.agency.clients)

    def test_add_property(self):
        self.agency.add_property(self.property)
        self.assertIn(self.property, self.agency.properties)

    def test_search_properties(self):
        self.agency.add_property(self.property)
        criteria = {'address': '123 Kirova St', 'price': 200000}
        found_properties = self.agency.search_properties(criteria)
        self.assertIn(self.property, found_properties)

    def test_schedule_viewing(self):
        self.agency.add_property(self.property)
        deal = Deal(self.property, self.client, self.agent, [self.document])
        self.agency.schedule_viewing(deal, self.client)
        self.assertIn(self.client, self.property.interested_clients)

    def test_finalize_deal(self):
        self.agency.add_property(self.property)
        deal = Deal(self.property, self.client, self.agent, [self.document])
        self.agency.finalize_deal(deal)
        self.assertIn(deal, self.agency.deals)
        self.assertEqual(self.client, self.property.owner)

    def test_prepare_document(self):
        prepared_document = self.agency.prepare_document(self.document)
        self.assertTrue(prepared_document.signed)

if __name__ == '__main__':
    unittest.main()
