from .base import BaseTestCase


class TestUsers(BaseTestCase):

    def test_getUsers(self):
        users = self.nxc.getUsers()['ocs']['data']['users']
        assert users == [self.username]

