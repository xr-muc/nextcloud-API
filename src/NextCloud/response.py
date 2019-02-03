
class NextCloudResponse(object):

    def __init__(self, response, json_output=True, data=None):
        self.raw = response
        if not data:
            self.data = response.json() if json_output else response.content.decode("UTF-8")
        else:
            self.data = data


class WebDAVResponse(NextCloudResponse):
    """ Response class for WebDAV api methods """

    def __init__(self, response, data=None):
        super(WebDAVResponse, self).__init__(response=response, data=data, json_output=False)


class OCSResponse(NextCloudResponse):
    """ Response class for OCS api methods """

    def __init__(self, response, json_output=True, data=None):
        self.raw = response
        if json_output:
            self.full_data = response.json()
            self.meta = self.full_data['ocs']['meta']
            self.status_code = self.full_data['ocs']['meta']['statuscode']
            self.data = self.full_data['ocs']['data']
        else:
            self.data = response.content.decode("UTF-8")

    def __repr__(self):
        return "<OCSResponse: ocs_status_code={}>".format(getattr(self, 'status_code', None))
