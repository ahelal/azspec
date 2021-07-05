# azspec

Python AZ CLI based testing support library. This library helps you test your Azure resources. azspec is a helper library to run 
along your favorite python testing framework i.e. pytest, expects, unittest, ...

## Account

The account object is equivalent of running `az account show`


## AzVersion

## Resource

## Resources

## Examples

```python
# Python example using unit test
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
```

```python
# python example using mamba and expect
from mamba import description, it
from expects import expect, equal, be_true, match, have_len
from azspec.az import Resource, Resources

akss = Resources(args="aks", cache=True, cache_ttl=100)
aks = Resource(args="aks", name="domaks", resource_group='aks_test', cache=True, cache_ttl=200)

with description('AKS deployed') as self:
    with it('Exits and only one is deployed'):
        expect(akss.count).to(equal(1))
        expect(aks.exists).to(be_true)

    with it('Uses System assigned identity'):
        expect(aks.content['identity']['type']).to(equal('SystemAssigned'))

    with it('k8s version is 1.20.*'):
        expect(aks.content['kubernetesVersion']).to(match("1.20.*"))

    with it('Should use the free aks in eastus2'):
        expect(aks.content['location']).to(equal('eastus2'))
        expect(aks.content['sku']['name']).to(equal('Basic'))

    with it('Should have one node pool'):
        expect(aks.content['agentPoolProfiles']).to(have_len(1))
```

## CDF

TODO
