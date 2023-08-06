from dataclasses import dataclass
from pprint import pprint


@dataclass
class mollusc_response:
    response: dict
    raw_response: str = ""
    status_code: int = 0
    server_error: str = ""
    server_used: str = ""

    def get_answers(self):
        return self._get_data_from_response("Answer")

    def get_additional(self):
        return self._get_data_from_response("Additional")

    def _get_data_from_response(self, location):
        data_list = []
        if location in self.response.keys():
            for answer in self.response[location]:
                data_list.append(answer["data"])
        return data_list

    def is_blocked_by_server(self):
        answers = self.get_answers()

        if "0.0.0.0" in answers:
            return True
        if "::" in answers:
            return True

        additional = self.get_additional()
        for additional_record in additional:
            if "EDE: 17 (Filtered)" in additional_record:
                return True

        return False
