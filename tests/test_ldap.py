from .base import BaseTestCase


class TestUserLDAP(BaseTestCase):

    SUCCESS_CODE = 200

    def setUp(self):
        super(TestUserLDAP, self).setUp()
        self.nxc.enable_app('user_ldap')

    def test_crud_ldap_config(self):
        res = self.nxc.create_ldap_config()
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        config_id = res['ocs']['data']['configID']

        # test get config by id
        res = self.nxc.get_ldap_config(config_id)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        config_data = res['ocs']['data']

        # test edit config
        param_to_change = "ldapPagingSize"
        old_param_value = config_data[param_to_change]
        new_param_value = 777
        assert old_param_value != new_param_value
        res = self.nxc.edit_ldap_config(config_id, data={param_to_change: new_param_value})
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        new_config_data = self.nxc.get_ldap_config(config_id)['ocs']['data']
        assert str(new_config_data[param_to_change]) == str(new_param_value)

        # test showPassword param
        ldap_password_param = "ldapAgentPassword"
        ldap_password_value = "test_password"
        self.nxc.edit_ldap_config(config_id, {ldap_password_param: ldap_password_value})
        config_data_without_password = self.nxc.get_ldap_config(config_id)['ocs']['data']
        assert config_data_without_password[ldap_password_param] == "***"
        config_data_with_password = self.nxc.get_ldap_config(config_id, show_password=1)['ocs']['data']
        assert config_data_with_password[ldap_password_param] == ldap_password_value

        # test delete config
        res = self.nxc.delete_ldap_config(config_id)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        res = self.nxc.get_ldap_config(config_id)
        assert res['ocs']['meta']['statuscode'] == self.NOT_FOUND_CODE
