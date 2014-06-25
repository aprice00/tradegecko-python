import requests
import json


class TGRequestFailure(Exception):
    pass


class ApiEndpoint(object):

    def __init__(self, base_data, access_token):
        self.base_data = base_data
        self.access_token = access_token
        self.header = {
            'Authorization': 'Bearer ' + self.access_token,
            'content-type': 'application/json'
        }
        self.rsp = None
        self.json = None
        self.base_uri = 'https://api.tradegecko.com/'
        self.uri = ''
        self.required_fields = []
        self._data_name = ''

    def _validate_post_data(self, data):
        for k in self.required_fields:
            if k not in data.keys():
                return False
        return True

    def _send_request(self, method, uri, data=None, params=None):
        self.rsp = requests.request(method, uri, data=data, headers=self.header, params=params)
        return self.rsp.status_code

    def _build_data(self, data):
        return json.dumps({self._data_name: data})

    # all records
    def all(self, page=1):
        params = {'page': page}
        if self._send_request('GET', self.uri, params=params) == 200:
            return self.rsp.json()
        else:
            return False

    # retrieve a specific record
    def get(self, pk):
        uri = self.uri + str(pk)
        if self._send_request('GET', uri) == 200:
            return self.rsp.json()
        else:
            return False

    # delete a specific record
    def delete(self, pk):
        uri = self.uri + str(pk)
        if self._send_request('DELETE', uri) == 204:
            return self.rsp
        else:
            return False

    # create a new record
    def create(self, data):
        data = self._build_data(data)

        if self._send_request('POST', self.uri, data=data) == 201:
            return self.rsp.json()[self._data_name]['id']
        else:
            raise TGRequestFailure("Creation Failed")

    # update a specific record
    def update(self, pk, data):
        uri = self.uri + str(pk)
        data = self._build_data(data)

        if self._send_request('PUT', uri, data=data) == 204:
            return True
        else:
            raise TGRequestFailure("Update Failed")