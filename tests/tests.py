import sys
import os
from os.path import dirname, abspath
import unittest

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from NextCloud import NextCloud



NEXTCLOUD_URL = "http://{}".format(os.environ['NEXTCLOUD_HOST'])
NEXTCLOUD_USERNAME = os.environ.get('NEXTCLOUD_USERNAME')
NEXTCLOUD_PASSWORD = os.environ.get('NEXTCLOUD_PASSWORD')


class TestUsersApi(unittest.TestCase):

    def setUp(self):
        self.nxc = NextCloud(NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, js=True)

    def test_getUsers(self):
        users = self.nxc.getUsers()['ocs']['data']['users']
        self.assertEqual(users, [NEXTCLOUD_USERNAME])


if __name__ == '__main__':
    unittest.main()
