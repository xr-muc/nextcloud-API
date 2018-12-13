import os
import random
import string
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

    def get_random_string(self, length=6):
        """ Helper method to get random string with set length  """
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
