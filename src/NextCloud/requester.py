import requests


class Requester(object):
    def __init__(self, endpoint, user, passwd, json_output=False):
        self.query_components = []

        self.json_output = json_output

        self.base_url = endpoint
        # GroupFolders.url = endpoint + "/ocs/v2.php/apps/groupfolders/folders"

        self.h_get = {"OCS-APIRequest": "true"}
        self.h_post = {"OCS-APIRequest": "true",
                       "Content-Type": "application/x-www-form-urlencoded"}
        self.auth_pk = (user, passwd)
        self.API_URL = None

    def rtn(self, resp):
        if self.json_output:
            return resp.json()
        else:
            return resp.content.decode("UTF-8")

    def get(self, url="", params=None):
        url = self.get_full_url(url)
        res = requests.get(url, auth=self.auth_pk, headers=self.h_get, params=params)
        return self.rtn(res)

    def post(self, url="", data=None):
        url = self.get_full_url(url)
        res = requests.post(url, auth=self.auth_pk, data=data, headers=self.h_post)
        return self.rtn(res)

    def put(self, url="", data=None):
        url = self.get_full_url(url)
        res = requests.put(url, auth=self.auth_pk, data=data, headers=self.h_post)
        return self.rtn(res)

    def delete(self, url="", data=None):
        url = self.get_full_url(url)
        res = requests.delete(url, auth=self.auth_pk, data=data, headers=self.h_post)
        return self.rtn(res)

    def get_full_url(self, additional_url=""):
        """
        Build full url for request to NextCloud api

        Construct url from self.base_url, self.API_URL, additional_url (if given), add format=json param if self.json

        :param additional_url: str
            add to url after api_url
        :return: str
        """
        if additional_url and not str(additional_url).startswith("/"):
            additional_url = "/{}".format(additional_url)

        if self.json_output:
            self.query_components.append("format=json")

        ret = "{base_url}{api_url}{additional_url}".format(
            base_url=self.base_url, api_url=self.API_URL, additional_url=additional_url)

        if self.json_output:
            ret += "?format=json"
        return ret
