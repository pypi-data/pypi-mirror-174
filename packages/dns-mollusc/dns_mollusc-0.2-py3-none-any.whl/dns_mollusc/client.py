from .response import mollusc_response
import requests
from time import time, sleep


class mollusc_client(object):
    def __init__(
        self,
        server="https://security.cloudflare-dns.com/dns-query?",
        max_qps=100,
    ):
        self.server = server
        self.max_qps = max_qps

        self.client = requests.session()
        self.last_query_time = 0

    def query(self, query_input, query_type="A"):
        self._backoff()

        query_params = {
            "name": query_input,
            "type": query_type,
            "ct": "application/dns-json",
        }

        code = 0
        server_error = ""
        raw_result = ""
        parsed_result = {}

        try:
            request_result = self.client.get(
                self.server,
                params=query_params,
                headers={"accept": "application/dns-json"},
            )
            code = request_result.status_code
            raw_result = request_result.text
            parsed_result = request_result.json()
        except Exception as e:
            server_error = e

        return mollusc_response(
            parsed_result, raw_result, code, server_error, self.server
        )

    def _backoff(self):
        now = time()
        backoff_for = (1 / self.max_qps) - (now - self.last_query_time)

        if backoff_for > 0:
            sleep(backoff_for)

        self.last_query_time = now
