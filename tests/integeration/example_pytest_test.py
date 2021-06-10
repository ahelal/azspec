''' example '''
from azspec.az import Resource, Resources
import unittest

class TestStringMethods(unittest.TestCase):
    aks = None
    akss = None

    @classmethod
    def setUpClass(cls):
        cls.akss = Resources(args="aks", cache=True, cache_ttl=100)
        cls.aks = Resource(args="aks", name="domaks", resource_group='aks_test', cache=True, cache_ttl=200)        

    def test_only_one_aks(self):
        self.assertEqual(self.akss.count, 1)
        self.assertTrue(self.akss.exists)
    
    def test_system_msi(self):
        self.assertEqual(self.aks.content['identity']['type'], 'SystemAssigned')

    def test_aks_version_1_20(self):
        self.assertRegex(self.aks.content['kubernetesVersion'], "1.20.*")
    
    def test_aks_sku(self):
        self.assertEqual(self.aks.content['location'], 'eastus2')
        self.assertEqual(self.aks.content['sku']['name'], 'Basic')

    def test_aks_node_pool(self):
        self.assertEqual(len(self.aks.content['agentPoolProfiles']), 1)
