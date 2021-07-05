''' Base class '''

import os
import json
import base64
from datetime import datetime
from azspec.utils import run_command, convert_to_list_if_need, get_value


# pylint: disable=R0902
class BasicAZ():
    ''' Basic spec CLI interface '''
    def __init__(self, subcommand, args=None, name=None, resource_group=None, extra_args=None, **kwargs):
        ''' kwargs options:
                cli_path
                subscription
                cache
        '''
        subscription = kwargs.get("subscription", None)
        self.content = {}
        self.cache = kwargs.get("cache", None)
        self.cache_dir = kwargs.get("cache_dir", None)
        self.cache_ttl = get_value("AZSPEC_CACHE_TTL", "cache_ttl", kwargs, default=120)
        self.az_cli = get_value("AZSPEC_CLI_PATH", "cli_path", kwargs, default="az")
        self.cmd = convert_to_list_if_need(args)
        self.cmd += convert_to_list_if_need(subcommand)
        if subscription:
            self.cmd += ["--subscription", subscription]
        if name:
            self.cmd += ["--name", name]
        if resource_group:
            self.cmd += ["--resource-group", resource_group]
        if extra_args:
            self.cmd += convert_to_list_if_need(extra_args)
        self.cmd += ["-o", "json"]
        self._setup_cache()
        if self._fetch_from_cache():
            return
        # failed or missed cache or no cache enabled just run
        self._run()

    def _setup_cache(self):
        if not self.cache:
            return
        if not self.cache_dir:
            self.cache_dir = ".az_spec_tmp"
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
        if not os.path.exists(self.cache_dir):
            raise ValueError('AZ spec Cache dir does not exist {self.cache_dir}')
        self.encoded_file = str(base64.urlsafe_b64encode("".join(self.cmd).encode("utf-8")), "utf-8")
        self.encoded_file = os.path.join(self.cache_dir, self.encoded_file)

    def _run(self):
        self.stdout, self.stderr, self.return_code = run_command(self.az_cli, args=self.cmd, interactive=False, cwd=None, allow_non_zero_return=True)
        try:
            self.content = json.loads(self.stdout)
        except json.decoder.JSONDecodeError as error:
            print(f"warning json decoded error {str(error)}")
            return
        if not self.cache:
            return
        with open(self.encoded_file, 'w') as outfile:
            json.dump(
                {
                    "ts": datetime.now().timestamp(),
                    "cmd": self.cmd,
                    "content": self.content,
                    "stdout": self.stdout,
                    "stderr": self.stderr,
                    "return_code": self.return_code,
                }, outfile)

    def _fetch_from_cache(self):
        if not self.cache:
            return False
        try:
            with open(self.encoded_file, 'r') as jsonfile:
                data = json.load(jsonfile)
                ts_file = data['ts']
                ts_now = datetime.now().timestamp()
                if self.cache_ttl < (ts_now - ts_file):
                    print("warning Cache miss")
                    # cache miss
                    return False
                self.content = data['content']
                self.stdout = data['stdout']
                self.stderr = data['stderr']
                self.return_code = data['return_code']
                return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError as error:
            print(f"warning json load error {self.encoded_file}", str(error))
            return False

    @property
    def success(self):
        ''' Was the operation successful '''
        return self.return_code == 0

    @property
    def exists(self):
        ''' Resource exists '''
        return len(self.stdout) > 0 and self.success
