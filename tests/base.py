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

    SHARE_API_SUCCESS_CODE = 200  # share api has different code

    def setUp(self):
        self.username = NEXTCLOUD_USERNAME
        self.nxc = NextCloud(NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, js=True)

    def create_new_user(self, username_prefix, password=None):
        """ Helper method to create new user """
        new_user_username = username_prefix + self.get_random_string(length=4)
        user_password = password or self.get_random_string(length=8)
        res = self.nxc.add_user(new_user_username, user_password)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        return new_user_username

    def delete_user(self, username):
        """ Helper method to delete user by username """
        res = self.nxc.delete_user(username)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE

    def clear(self, nxc=None, user_ids=None, group_ids=None, share_ids=None, group_folder_ids=None):
        """
        Delete created objects during tests

        Args:
            nxc (NextCloud object): (optional) Nextcloud instance, if not given - self.nxc is used
            user_ids (list): list of user ids
            group_ids (list): list of group ids
            share_ids (list): list of shares ids

        Returns:

        """
        nxc = nxc or self.nxc
        if share_ids:
            for share_id in share_ids:
                res = nxc.delete_share(share_id)
                assert res['ocs']['meta']['statuscode'] == self.SHARE_API_SUCCESS_CODE
        if group_ids:
            for group_id in group_ids:
                res = nxc.delete_group(group_id)
                assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        if user_ids:
            for user_id in user_ids:
                res = nxc.delete_user(user_id)
                assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        if group_folder_ids:
            for group_folder_id in group_folder_ids:
                res = nxc.delete_group_folder(group_folder_id)
                assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE

    def get_random_string(self, length=6):
        """ Helper method to get random string with set length  """
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
