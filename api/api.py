from requests import get, post, put, delete
from core.helpers import get_settings


class API:
    def _base_url(self, environment):
        return get_settings(environment)['API_URL']

    def get_data(self, environment):
        return get(url=f'{self._base_url(environment)}/foo/bar')

    def send_data(self, environment, data):
        return post(url=f'{self._base_url(environment)}/foo/bar', data=data)

    def edit_data(self, environment, data):
        return put(url=f'{self._base_url(environment)}/foo/bar', data=data)

    def delete_data(self, environment):
        return delete(url=f'{self._base_url(environment)}/foo/bar')
