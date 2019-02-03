
class NextCloudResponse(object):

    def __init__(self, response, json_output=True, data=None):
        self.raw = response
        if not data:
            self.data = response.json() if json_output else response.content.decode("UTF-8")
        else:
            self.data = data


class WebDAVResponse(NextCloudResponse):
    def __init__(self, response, data=None):
        super(WebDAVResponse, self).__init__(response=response, data=data, json_output=False)
