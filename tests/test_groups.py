from .base import BaseTestCase


class TestUsers(BaseTestCase):

    def test_get_groups(self):
        res = self.nxc.get_groups()
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        assert len(res['ocs']['data']['groups']) > 0
        # test search argument
        res = self.nxc.get_groups(search="admin")
        groups = res['ocs']['data']['groups']
        assert all(["admin" in group for group in groups])
        # test limit argument
        res = self.nxc.get_groups(limit=0)
        assert len(res['ocs']['data']['groups']) == 0

    def test_add_get_group(self):
        group_name = self.get_random_string(length=4) + "_test_add"
        res = self.nxc.add_group(group_name)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        # get single group
        res = self.nxc.get_group(group_name)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        # assuming logged in user is admin
        res = self.nxc.get_group("admin")
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        group_users = res['ocs']['data']['users']
        assert self.username in group_users
