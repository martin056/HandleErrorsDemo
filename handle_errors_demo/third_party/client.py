import time


class ThirdPartyClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_data_method(self):
        time.sleep(3)

        raise PermissionError("403: Permission Denied.")
