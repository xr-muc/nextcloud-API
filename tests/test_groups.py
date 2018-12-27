from .base import BaseTestCase


class TestGroups(BaseTestCase):

    def setUp(self):
        super(TestGroups, self).setUp()
        self.user_username = self.create_new_user('user_group_')
        # create group
        self.group_name = self.get_random_string(length=4) + "_test_groups"
        self.nxc.add_group(self.group_name)

    def tearDown(self):
        self.delete_user(self.user_username)
        self.nxc.delete_group(self.group_name)

    def test_get_groups(self):
        res = self.nxc.get_groups()
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        assert len(res['ocs']['data']['groups']) > 0
        # test search argument
        res = self.nxc.get_groups(search=self.group_name)
        groups = res['ocs']['data']['groups']
        assert [self.group_name, "everyone"] == groups or [self.group_name] == groups
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

    def test_delete_group(self):
        group_name = self.get_random_string(length=4) + "_test_delete"
        self.nxc.add_group(group_name)
        res = self.nxc.delete_group(group_name)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        res = self.nxc.get_group(group_name)
        assert res['ocs']['meta']['statuscode'] == self.NOT_FOUND_CODE

    def test_group_subadmins(self):
        self.nxc.create_subadmin(self.user_username, self.group_name)
        res = self.nxc.get_subadmins(self.group_name)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        assert res['ocs']['data'] == [self.user_username]
