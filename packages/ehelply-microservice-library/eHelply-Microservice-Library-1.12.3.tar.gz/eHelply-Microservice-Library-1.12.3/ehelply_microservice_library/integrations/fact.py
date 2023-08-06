from ehelply_bootstrapper.integrations.integration import Integration
import threading
from ehelply_logger.Logger import Logger

import requests
import time

from typing import List

from pydantic import BaseModel
from ehelply_bootstrapper.utils.environment import Environment

from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.utils.cryptography import Encryption


class FactBase(BaseModel):
    name: str
    data: dict


def get_fact(fact_name: str):
    from ehelply_bootstrapper.utils.state import State
    fact: Fact = State.integrations.get("fact")
    return fact.facts[fact_name]


def get_fact_stage(fact_name: str):
    return get_fact(fact_name)


def get_fact_endpoint(fact_name: str):
    return get_fact(fact_name)['endpoint']


class Fact(Integration):
    def __init__(self, service_gatekeeper_key: str, logger: Logger, fact_names: List[str] = None) -> None:
        super().__init__("fact")
        self.fact_names = []
        if fact_names:
            self.fact_names = fact_names
        self.facts = {}
        self.logger = logger.spinoff()
        self.thread: FactThread = None
        self.fact_query_delay_minutes: int = 20
        self.enc: Encryption = Encryption([service_gatekeeper_key.encode(Encryption.STRING_ENCODING)])
        self.requests: requests.Session = requests.Session()

    def init(self):
        secret_token: str = State.config.m2m.auth.secret_key
        access_token: str = State.config.m2m.auth.access_key

        if len(secret_token) == 0 or len(access_token) == 0:
            State.logger.warning("SDK (M2M) credentials are not set. Check the m2m.yaml config")

        secret_token = self.enc.decrypt_str(secret_token.encode(Encryption.STRING_ENCODING))
        access_token = self.enc.decrypt_str(access_token.encode(Encryption.STRING_ENCODING))
        self.requests.headers.update({
            'X-Secret-Token': secret_token,
            'X-Access-Token': access_token,
            'Ehelply-Project': 'ehelply-cloud'
        })

        # Initial load to prevent race conditions
        self._query()
        self.thread = FactThread(self).start()

    def load(self):
        pass

    def _query(self):
        State.logger.info("  -> Fetching Latest Facts")
        for fact_name in self.fact_names:
            State.logger.debug("     * " + State.config.facts.endpoint + "/facts/" + fact_name)
            response = self.requests.get(State.config.facts.endpoint + "/facts/" + fact_name)
            try:
                if response.status_code == 200:
                    self.facts[fact_name] = response.json()['data']
                else:
                    State.logger.warning(f"Fact not found: {fact_name}")
            except:
                raise Exception(
                    "Communication with ehelply-facts failed. There are several possible reasons for this: incorrect fact name or you're sending the request from an IP address that has not been whitelisted.")

    def refresh(self):
        self._query()

    def run(self):
        while True:
            time.sleep(self.fact_query_delay_minutes * 60)
            self._query()

    def push_fact(self, fact: FactBase):
        response = self.requests.post(State.config.facts.endpoint + "/facts", json={"fact": fact.dict()})
        return response


class FactThread(threading.Thread):
    def __init__(self, fact: Fact):
        super().__init__()
        self.fact: Fact = fact
        self.daemon = True

    def run(self) -> None:
        self.fact.run()
