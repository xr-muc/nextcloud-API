from NextCloud.base import WithRequester


class UserLDAP(WithRequester):
    API_URL = "/ocs/v2.php/apps/user_ldap/api/v1/config"

    def create_ldap_config(self):
        """ Create a new and empty LDAP configuration """
        return self.requester.post()

    def get_ldap_config(self, config_id, show_password=None):
        """
        Get all keys and values of the specified LDAP configuration

        Args:
            config_id (str): User LDAP config id
            show_password (int): 0 or 1 whether to return the password in clear text (default 0)

        Returns:

        """
        params = dict(showPassword=show_password)
        return self.requester.get(config_id, params=params)

    def edit_ldap_config(self, config_id, data):
        """
        Update a configuration with the provided values

        You can find list of all config keys in get_ldap_config method response or in Nextcloud docs

        Args:
            config_id (str): User LDAP config id
            data (dict): config values to update

        Returns:

        """
        # TODO: refactor to provide methods for configuration s.a. edit_ldap_password and get_ldap_password
        prepared_data = {'configData[{}]'.format(key): value for key, value in data.items()}
        return self.requester.put(config_id, data=prepared_data)

    def delete_ldap_config(self, config_id):
        """
        Delete a given LDAP configuration

        Args:
            config_id (str): User LDAP config id

        Returns:

        """
        return self.requester.delete(config_id)
