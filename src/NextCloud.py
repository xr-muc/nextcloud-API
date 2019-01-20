from .requester import Requester
from .api_wrappers import API_CLASSES


class NextCloud(object):

    def __init__(self, endpoint, user, password, js=False):
        self.query_components = []

        requester = Requester(endpoint, user, password, js)

        self.functionality_classes = [api_class(requester) for api_class in API_CLASSES]

        for functionality_class in self.functionality_classes:
            for each in dir(functionality_class):
                if each.startswith('_') or not callable(getattr(functionality_class, each)):
                    continue
                setattr(self, each, getattr(functionality_class, each))
