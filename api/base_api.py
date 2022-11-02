from requests import Session


class BaseApi:
    def __init__(self, base_url: str, session: Session = Session()):
        self.base_url: str = base_url
        self.session: Session = session

    def _get(self, url: str = '/') -> dict:
        for _ in range(0, 100):
            try:
                return self.session.get(url=f'{self.base_url}/{url}', verify=False).json()
            except Exception as e:
                print('Unexpected error:', e)
                return {}

    def _post(self, data: dict = None, url: str = '/', files: dict = None, auth: tuple = None, headers: dict = None) -> dict | str:
        for _ in range(0, 100):
            if data is None:
                data: dict = {}
            if files is None:
                files: dict = {}
            if headers is None:
                headers: dict = {}
            try:
                is_json = isinstance(data, dict)
                response = self.session.post(
                    url=f'{self.base_url}/{url}',
                    json=data if is_json else None,
                    data=None if is_json else data,
                    files=files,
                    verify=False,
                    auth=auth,
                    headers=headers
                )
                try:
                    if response.content != '':
                        return response.json()
                    return response.text
                except Exception as ex:
                    print('Unexpected error:', ex)
                    return response.text
            except Exception as ex:
                print('Unexpected error:', ex)

    def _put(self, data: dict = None, url: str = '/', files: dict = None, auth: tuple = None, headers: dict = None) -> dict | str:
        for _ in range(0, 100):
            if data is None:
                data: dict = {}
            if files is None:
                files: dict = {}
            if headers is None:
                headers: dict = {}
            try:
                is_json = isinstance(data, dict)
                response = self.session.put(
                    url=f'{self.base_url}/{url}',
                    json=data if is_json else None,
                    data=None if is_json else data,
                    files=files,
                    verify=False,
                    auth=auth,
                    headers=headers
                )
                try:
                    if response.content != '':
                        return response.json()
                    return response.text
                except Exception as ex:
                    print('Unexpected error:', ex)
                    return response.text
            except Exception as ex:
                print('Unexpected error:', ex)

    def _patch(self, data: dict = None, url: str = '/', files: dict = None, auth: tuple = None, headers: dict = None) -> dict | str:
        for _ in range(0, 100):
            if data is None:
                data: dict = {}
            if files is None:
                files: dict = {}
            if headers is None:
                headers: dict = {}
            try:
                is_json = isinstance(data, dict)
                response = self.session.patch(
                    url=f'{self.base_url}/{url}',
                    json=data if is_json else None,
                    data=None if is_json else data,
                    files=files,
                    verify=False,
                    auth=auth,
                    headers=headers
                )
                try:
                    if response.content != '':
                        return response.json()
                    return response.text
                except Exception as ex:
                    print('Unexpected error:', ex)
                    return response.text
            except Exception as ex:
                print('Unexpected error:', ex)

    def _delete(self, data: dict = None, url: str = '/', files: dict = None, auth: tuple = None, headers: dict = None) -> dict | str:
        for _ in range(0, 100):
            if data is None:
                data: dict = {}
            if files is None:
                files: dict = {}
            if headers is None:
                headers: dict = {}
            try:
                is_json = isinstance(data, dict)
                response = self.session.delete(
                    url=f'{self.base_url}/{url}',
                    json=data if is_json else None,
                    data=None if is_json else data,
                    files=files,
                    verify=False,
                    auth=auth,
                    headers=headers
                )
                try:
                    if response.content != '':
                        return response.json()
                    return response.text
                except Exception as ex:
                    print('Unexpected error:', ex)
                    return response.text
            except Exception as ex:
                print('Unexpected error:', ex)
