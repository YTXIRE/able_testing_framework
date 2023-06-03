from requests import Session


class BaseApi:
    def __init__(self, api_base_url: str, session: Session = Session()):
        self.api_base_url: str = api_base_url
        self.session: Session = session

    def get(self, url: str = '/') -> dict:
        try:
            return self.session.get(url=f'{self.api_base_url}/{url}', verify=False).json()
        except Exception as _ex:
            print('Unexpected error:', _ex)
            return {}

    def post(
        self,
        data: dict = None,
        url: str = '/',
        files: dict = None,
        auth: tuple = None,
        headers: dict = None
    ) -> dict | str:
        if data is None:
            data: dict = {}
        if files is None:
            files: dict = {}
        if headers is None:
            headers: dict = {}
        try:
            is_json = isinstance(data, dict)
            response = self.session.post(
                url=f'{self.api_base_url}/{url}',
                json=data if is_json else None,
                data=None if is_json else data,
                files=files,
                verify=False,
                auth=auth,
                headers=headers,
            )
            try:
                if response.content != '':
                    return response.json()
                return response.text
            except Exception as _ex:
                print('Unexpected error:', _ex)
                return response.text
        except Exception as _ex:
            print('Unexpected error:', _ex)

    def put(
        self,
        data: dict = None,
        url: str = '/',
        files: dict = None,
        auth: tuple = None,
        headers: dict = None
    ) -> dict | str:
        if data is None:
            data: dict = {}
        if files is None:
            files: dict = {}
        if headers is None:
            headers: dict = {}
        try:
            is_json = isinstance(data, dict)
            response = self.session.put(
                url=f'{self.api_base_url}/{url}',
                json=data if is_json else None,
                data=None if is_json else data,
                files=files,
                verify=False,
                auth=auth,
                headers=headers,
            )
            try:
                if response.content != '':
                    return response.json()
                return response.text
            except Exception as _ex:
                print('Unexpected error:', _ex)
                return response.text
        except Exception as _ex:
            print('Unexpected error:', _ex)

    def patch(
        self,
        data: dict = None,
        url: str = '/',
        files: dict = None,
        auth: tuple = None,
        headers: dict = None
    ) -> dict | str:
        if data is None:
            data: dict = {}
        if files is None:
            files: dict = {}
        if headers is None:
            headers: dict = {}
        try:
            is_json = isinstance(data, dict)
            response = self.session.patch(
                url=f'{self.api_base_url}/{url}',
                json=data if is_json else None,
                data=None if is_json else data,
                files=files,
                verify=False,
                auth=auth,
                headers=headers,
            )
            try:
                if response.content != '':
                    return response.json()
                return response.text
            except Exception as _ex:
                print('Unexpected error:', _ex)
                return response.text
        except Exception as _ex:
            print('Unexpected error:', _ex)

    def head(
        self,
        data: dict = None,
        url: str = '/',
        files: dict = None,
        auth: tuple = None,
        headers: dict = None
    ) -> dict | str:
        if data is None:
            data: dict = {}
        if files is None:
            files: dict = {}
        if headers is None:
            headers: dict = {}
        try:
            is_json = isinstance(data, dict)
            response = self.session.head(
                url=f'{self.api_base_url}/{url}',
                json=data if is_json else None,
                data=None if is_json else data,
                files=files,
                verify=False,
                auth=auth,
                headers=headers,
            )
            try:
                if response.content != '':
                    return response.json()
                return response.text
            except Exception as _ex:
                print('Unexpected error:', _ex)
                return response.text
        except Exception as _ex:
            print('Unexpected error:', _ex)

    def options(
        self,
        data: dict = None,
        url: str = '/',
        files: dict = None,
        auth: tuple = None,
        headers: dict = None
    ) -> dict | str:
        if data is None:
            data: dict = {}
        if files is None:
            files: dict = {}
        if headers is None:
            headers: dict = {}
        try:
            is_json = isinstance(data, dict)
            response = self.session.options(
                url=f'{self.api_base_url}/{url}',
                json=data if is_json else None,
                data=None if is_json else data,
                files=files,
                verify=False,
                auth=auth,
                headers=headers,
            )
            try:
                if response.content != '':
                    return response.json()
                return response.text
            except Exception as _ex:
                print('Unexpected error:', _ex)
                return response.text
        except Exception as _ex:
            print('Unexpected error:', _ex)

    def delete(self, url: str = '/') -> dict:
        try:
            return self.session.delete(url=f'{self.api_base_url}/{url}', verify=False).json()
        except Exception as _ex:
            print('Unexpected error:', _ex)
            return {}
