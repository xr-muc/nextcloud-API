from nextcloud.base import WithRequester


class Group(WithRequester):
    API_URL = "/ocs/v1.php/cloud/groups"
    SUCCESS_CODE = 100

    def get_groups(self, search=None, limit=None, offset=None):
        """
        Retrieve a list of groups from the Nextcloud server

        :param search: string, optional search string
        :param limit: int, optional limit value
        :param offset: int, optional offset value
        :return:
        """
        params = {
            'search': search,
            'limit': limit,
            'offset': offset
        }
        return self.requester.get(params=params)

    def add_group(self, gid):
        """
        Add a new group

        :param gid: str, group name
        :return:
        """
        msg = {"groupid": gid}
        return self.requester.post("", msg)

    def get_group(self, gid):
        """
        Retrieve a list of group members

        :param gid: str, group name
        :return:
        """
        return self.requester.get("{gid}".format(gid=gid))

    def get_subadmins(self, gid):
        """
        List subadmins of the group

        :param gid: str, group name
        :return:
        """
        return self.requester.get("{gid}/subadmins".format(gid=gid))

    def delete_group(self, gid):
        """
        Remove a group

        :param gid: str, group name
        :return:
        """
        return self.requester.delete("{gid}".format(gid=gid))
