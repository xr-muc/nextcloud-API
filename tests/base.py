import os
from unittest import TestCase

from NextCloud import NextCloud

NEXTCLOUD_URL = "http://{}:80".format(os.environ['NEXTCLOUD_HOST'])
NEXTCLOUD_USERNAME = os.environ.get('NEXTCLOUD_USERNAME')
NEXTCLOUD_PASSWORD = os.environ.get('NEXTCLOUD_PASSWORD')


class BaseTestCase(TestCase):

    SUCCESS_CODE = 100
    INVALID_INPUT_CODE = 101
    USERNAME_ALREADY_EXISTS_CODE = 102
    UNKNOWN_ERROR_CODE = 103
    NOT_FOUND_CODE = 404

    def setUp(self):
        self.username = NEXTCLOUD_USERNAME
        self.nxc = NextCloud(NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, js=True)
