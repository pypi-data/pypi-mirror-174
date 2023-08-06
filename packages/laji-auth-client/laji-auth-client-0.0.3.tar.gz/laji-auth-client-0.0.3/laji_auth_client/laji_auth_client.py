import requests
import json


class LajiAuthClient(object):
    def __init__(self, laji_auth_url, system_id):
        self.laji_auth_url = laji_auth_url
        self.system_id = system_id

    def get_login_url(self, redirect_method=None, next_url=None):
        login_url = '{}/login?target={}'.format(
            self.laji_auth_url,
            self.system_id,
            redirect_method
        )
        if redirect_method is not None:
            login_url += '&redirectMethod={}'.format(redirect_method)
        if next_url is not None:
            login_url += '&next={}'.format(next_url)
        return login_url

    def get_authentication_info(self, token):
        url = '{}/token/{}'.format(self.laji_auth_url, token)
        response = requests.get(url)

        if response.ok:
            content = json.loads(response.content.decode('utf-8'))
            if content['target'] == self.system_id:
                return content

        return None

    def log_out(self, token):
        url = '{}/token/{}'.format(self.laji_auth_url, token)
        response = requests.delete(url)
        return response.ok
