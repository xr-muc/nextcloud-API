from .base import BaseTestCase


class TestUsers(BaseTestCase):

    def create_new_user(self, username_prefix):
        """ Helper method to create new user """
        new_user_username = username_prefix + self.get_random_string(length=4)
        res = self.nxc.add_user(new_user_username, self.get_random_string(length=8))
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        return new_user_username

    def delete_user(self, username):
        """ Helper method to delete user by username """
        res = self.nxc.delete_user(username)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE

    def test_get_users(self):
        res = self.nxc.get_users()
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        assert len(res['ocs']['data']['users']) > 0
        # test search argument
        res = self.nxc.get_users(search=self.username)
        users = res['ocs']['data']['users']
        assert all([self.username in user for user in users])
        # test limit argument
        res = self.nxc.get_users(limit=0)
        assert len(res['ocs']['data']['users']) == 0

    def test_get_user(self):
        res = self.nxc.get_user(self.username)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        user = res['ocs']['data']
        assert user['id'] == self.username
        assert user['enabled']

    def test_add_user(self):
        new_user_username = self.get_random_string(length=4) + "test_add"
        res = self.nxc.add_user(new_user_username, self.get_random_string(length=8))
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        added_user = self.nxc.get_user(new_user_username)['ocs']['data']
        assert added_user['id'] == new_user_username and added_user['enabled']
        # adding same user will fail
        res = self.nxc.add_user(new_user_username, "test_password_123")
        assert res['ocs']['meta']['statuscode'] == self.USERNAME_ALREADY_EXISTS_CODE

    def test_disable_enable_user(self):
        new_user_username = self.get_random_string(length=4) + "test_enable"
        self.nxc.add_user(new_user_username, self.get_random_string(length=8))
        user = self.nxc.get_user(new_user_username)['ocs']['data']
        assert user['enabled']
        self.nxc.disable_user(new_user_username)
        user = self.nxc.get_user(new_user_username)['ocs']['data']
        assert not user['enabled']
        self.nxc.enable_user(new_user_username)
        user = self.nxc.get_user(new_user_username)['ocs']['data']
        assert user['enabled']

    def test_delete_user(self):
        new_user_username = self.get_random_string(length=4) + "test_enable"
        self.nxc.add_user(new_user_username, self.get_random_string(length=8))
        res = self.nxc.delete_user(new_user_username)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        user_res = self.nxc.get_user(new_user_username)
        assert user_res['ocs']['meta']['statuscode'] == self.NOT_FOUND_CODE

    def test_edit_user(self):
        new_user_username = self.create_new_user("edit_user")
        new_user_values = {
            "email": "test@test.test",
            # "quota": "100MB", FIXME: only admins (of a group?) can edit quota
            "phone": "+380999999999",
            "address": "World!",
            "website": "example.com",
            "twitter": "@twitter_account",
            "displayname": "test user!",
            "password": self.get_random_string(length=10)
        }
        for key, value in new_user_values.items():
            res = self.nxc.edit_user(new_user_username, key, value)
            assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE

    def test_resend_welcome_mail(self):
        # TODO: add mock of SMTP data to test this method
        pass


