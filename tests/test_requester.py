from unittest import TestCase

from nextcloud.requester import Requester, NextCloudConnectionError


class TestRequester(TestCase):

    def test_wrong_url(self):
        wrong_url = 'http://wrong-url.wrong'
        req = Requester(wrong_url, 'user', 'password', json_output=False)
        req.API_URL = '/wrong'
        exception_raised = False
        try:
            req.get('')
        except NextCloudConnectionError as e:
            exception_raised = True
            assert wrong_url in str(e)
        assert exception_raised

