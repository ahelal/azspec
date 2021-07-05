''' Basic CLI v2'''


from azspec.basic import BasicAZ


class Resource(BasicAZ):
    ''' Single Resource '''

    def __init__(self, args, name=None, resource_group=None, extra_args=None, **kwargs):
        BasicAZ.__init__(self, subcommand="show", args=args, name=name, resource_group=resource_group, extra_args=extra_args, **kwargs)


class Resources(BasicAZ):
    ''' List Resources '''

    def __init__(self, args, name=None, resource_group=None, extra_args=None, **kwargs):
        BasicAZ.__init__(self, subcommand="list", args=args, name=name, resource_group=resource_group, extra_args=extra_args, **kwargs)

    @property
    def exists(self):
        ''' Did return any resources '''
        return len(self.content) > 0 and self.success

    @property
    def count(self):
        ''' Number of resources returned '''
        return len(self.content)


class Account(BasicAZ):
    ''' Az Account list '''

    def __init__(self, cli_path="az", refresh=False, disabled=False, cache=False, cache_dir=None, cache_ttl=30):
        extra_args = []
        if disabled:
            extra_args += ["--all"]
        if refresh:
            extra_args += ["--refresh"]
        BasicAZ.__init__(self, subcommand=["account", "list"], cli_path=cli_path, extra_args=extra_args, cache=cache, cache_dir=cache_dir, cache_ttl=cache_ttl)

    @property
    def exists(self):
        ''' Did account return any accounts '''
        return len(self.content) > 0 and self.success

    @property
    def count(self):
        ''' Number of resources returned '''
        return len(self.content)
    # TODO get do some helper getters (default, tenet, subscription map)


class AzVersion(BasicAZ):
    ''' Az CLI version '''

    def __init__(self, cli_path="az", cache=False, cache_dir=None, cache_ttl=300):
        BasicAZ.__init__(self, subcommand=["account", "list"], cli_path=cli_path, cache=cache, cache_dir=cache_dir, cache_ttl=cache_ttl)

    @property
    def cli(self):
        ''' cli version '''
        if self.exists:
            return self.content["azure-cli"]
        return None

    @property
    def core(self):
        ''' cli core version '''
        if self.exists:
            return self.content["azure-cli-core"]
        return None

    @property
    def extensions(self):
        ''' cli extensions version '''
        if self.exists:
            return self.content["extensions"]
        return None
