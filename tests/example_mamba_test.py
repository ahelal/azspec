''' example '''
from mamba import description, it  # ,context
from expects import expect, equal, be_true, match, have_len
from azspec.az import Resource, Resources
# Account, AzVersion

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

# with it('node pool')
# A = Resource(args=["network", "vnet"], name="vnet01", resource_group='api')
# A = Resources(args=["network", "vnet", "subnet"], resource_group='api', extra_args=["--vnet-name", "vnet01"])
