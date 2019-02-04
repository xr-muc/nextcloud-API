from .requester import Requester, WebDAVRequester
from .api_wrappers import API_CLASSES, WEBDAV_CLASS


class NextCloud(object):

    def __init__(self, endpoint, user, password, json_output=True):
        self.query_components = []

        requester = Requester(endpoint, user, password, json_output)
        webdav_requester = WebDAVRequester(endpoint, user, password)

        self.functionality_classes = [api_class(requester) for api_class in API_CLASSES]
        self.functionality_classes.append(WEBDAV_CLASS(webdav_requester, json_output=json_output))

        for functionality_class in self.functionality_classes:
            for potential_method in dir(functionality_class):
                if potential_method.startswith('_') or not callable(getattr(functionality_class, potential_method)):
                    continue
                setattr(self, potential_method, getattr(functionality_class, potential_method))
