import requests


class HTTP:
    @classmethod
    def get(cls, url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return r.text if return_json else {}
        return r.json() if return_json else r.text

