import os
from unittest import TestCase

from NextCloud import NextCloud

NEXTCLOUD_URL = "http://{}:80".format(os.environ['NEXTCLOUD_HOST'])
NEXTCLOUD_USERNAME = os.environ.get('NEXTCLOUD_USERNAME')
NEXTCLOUD_PASSWORD = os.environ.get('NEXTCLOUD_PASSWORD')


class BaseTestCase(TestCase):

    def setUp(self):
        self.username = NEXTCLOUD_USERNAME
        self.nxc = NextCloud(NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, js=True)
