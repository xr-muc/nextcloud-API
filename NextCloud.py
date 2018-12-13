import enum

import requests


PUBLIC_API_NAME_CLASS_MAP = dict()


class Requester(object):
    def __init__(self, endpoint, user, passwd, js=False):
        self.query_components = []

        self.to_json = js

        self.base_url = endpoint
        # GroupFolders.url = endpoint + "/ocs/v2.php/apps/groupfolders/folders"

        self.h_get = {"OCS-APIRequest": "true"}
        self.h_post = {"OCS-APIRequest": "true",
                       "Content-Type": "application/x-www-form-urlencoded"}
        self.auth_pk = (user, passwd)
        self.API_URL = None

    def rtn(self, resp):
        if self.to_json:
            return resp.json()
        else:
            return resp.content.decode("UTF-8")

    def get(self, url="", params=None):
        url = self.get_full_url(url)
        res = requests.get(url, auth=self.auth_pk, headers=self.h_get, params=params)
        return self.rtn(res)

    def post(self, url="", data=None):
        url = self.get_full_url(url)
        res = requests.post(url, auth=self.auth_pk, data=data, headers=self.h_post)
        return self.rtn(res)

    def put(self, url="", data=None):
        url = self.get_full_url(url)
        res = requests.put(url, auth=self.auth_pk, data=data, headers=self.h_post)
        return self.rtn(res)

    def delete(self, url="", data=None):
        url = self.get_full_url(url)
        res = requests.delete(url, auth=self.auth_pk, data=data, headers=self.h_post)
        return self.rtn(res)

    def get_full_url(self, additional_url=""):
        """
        Build full url for request to NextCloud api

        Construct url from self.base_url, self.API_URL, additional_url (if given), add format=json param if self.json

        :param additional_url: str
            add to url after api_url
        :return: str
        """
        if additional_url and not additional_url.startswith("/"):
            additional_url = "/" + additional_url

        if self.to_json:
            self.query_components.append("format=json")

        ret = "{base_url}/{api_url}{additional_url}".format(
            base_url=self.base_url, api_url=self.API_URL, additional_url=additional_url)

        if self.to_json:
            ret += "?format=json"
        return ret


def nextcloud_method(method_to_wrap):
    class_name = method_to_wrap.__qualname__.split(".", 1)[0]
    PUBLIC_API_NAME_CLASS_MAP[method_to_wrap.__name__] = class_name
    return method_to_wrap


class NextCloud(object):

    def __init__(self, endpoint, user, passwd, js=False):
        self.query_components = []

        requester = Requester(endpoint, user, passwd, js)

        self.functionality = {
            "Apps": Apps(requester),
            "Group": Group(requester),
            "GroupFolders": GroupFolders(requester),
            "Share": Share(requester),
            "User": User(requester),
        }

        for name, location in PUBLIC_API_NAME_CLASS_MAP.items():
            setattr(self, name, getattr(self.functionality[location], name))

        self.to_json = js

        self.base_url = endpoint
        # GroupFolders.url = endpoint + "/ocs/v2.php/apps/groupfolders/folders"

        self.h_get = {"OCS-APIRequest": "true"}
        self.h_post = {"OCS-APIRequest": "true",
                       "Content-Type": "application/x-www-form-urlencoded"}
        self.auth_pk = (user, passwd)


class WithRequester(object):
    def __init__(self, requester):
        self.requester = requester
        self.requester.API_URL = self.API_URL


class GroupFolders(WithRequester):
    API_URL = "/apps/groupfolders/folders"

    @nextcloud_method
    def get_group_folders(self):
        return self.requester.get()

    @nextcloud_method
    def create_group_folder(self, mountpoint):
        # FIXME: doesn't work
        return self.requester.post("", {"mountpoint": mountpoint})

    @nextcloud_method
    def delete_group_folder(self, fid):
        return self.requester.delete(fid)

    @nextcloud_method
    def grant_access_to_group_folder(self, fid, gid):
        url = "/".join(fid, gid)  # FIXME: doesn't work
        return self.requester.post(url)

    @nextcloud_method
    def revoke_access_to_group_folder(self, fid, gid):
        url = "/".join(fid, gid)  # FIXME: doesn't work
        return self.requester.delete(url)

    @nextcloud_method
    def set_access_to_group_folder(self, fid, gid, permissions):
        url = "/".join(fid, gid)  # FIXME: doesn't work
        return self.requester.post(url, {"permissions": permissions})

    @nextcloud_method
    def set_quota_of_group_folder(self, fid, quota):
        url = "/".join(fid, "quota")  # FIXME: doesn't work
        return self.requester.post(url, {"quota": quota})

    @nextcloud_method
    def rename_group_folder(self, fid, mountpoint):
        url = "/".join(fid, "mountpoint") # FIXME: doesn't work
        return self.requester.post(url, {"mountpoint": mountpoint})


class Share(WithRequester):
    API_URL = "/ocs/v2.php/apps/files_sharing/api/v1"
    LOCAL = "shares"
    FEDERATED = "remote_shares"

    def get_local_url(self, additional_url=""):
        if additional_url:
            return "/".join(self.LOCAL, additional_url)
        return self.LOCAL

    def get_federated_url(self, additional_url=""):
        if additional_url:
            return "/".join(self.FEDERATED, additional_url)
        return self.LOCAL

    @nextcloud_method
    def get_shares(self):
        self.requester.get(self.requester.get_local_url())

    @nextcloud_method
    def get_shares_from_path(self, path, reshares=None, subfiles=None):
        url = self.requester.get_local_url(path)

        if reshares is not None:
            self.query_components.append("reshares=true")

        if subfiles is not None:
            self.query_components.append("subfiles=true")

        return self.requester.get(url)

    @nextcloud_method
    def get_share_info(self, sid):
        self.requester.get(self.requester.get_local_url(sid))

    @nextcloud_method
    def create_share(
            self, path, shareType, shareWith=None, publicUpload=None,
            password=None, permissions=None):
        url = self.requester.get_local_url()
        if publicUpload:
            publicUpload = "true"
        if (path is None or not isinstance(shareType, int)) or (shareType in [0, 1] and shareWith is None):
            return False
        msg = {"path": path, "shareType": shareType}
        if shareType in [0, 1]:
            msg["shareWith"] = shareWith
        if publicUpload:
            msg["publicUpload"] = publicUpload
        if shareType == 3 and password is not None:
            msg["password"] = str(password)
        if permissions is not None:
            msg["permissions"] = permissions
        return self.requester.post(url, msg)

    @nextcloud_method
    def delete_share(self, sid):
        return self.requester.delete(self.requester.get_local_url(sid))

    @nextcloud_method
    def update_share(self, sid, permissions=None, password=None, publicUpload=None, expireDate=""):
        msg = {}
        if permissions:
            msg["permissions"] = permissions
        if password is not None:
            msg["password"] = str(password)
        if publicUpload:
            msg["publicUpload"] = "true"
        if publicUpload is False:
            msg["publicUpload"] = "false"
        if expireDate:
            msg["expireDate"] = expireDate
        url = self.requester.get_local_url(sid)
        return self.requester.put(url, msg)

    @nextcloud_method
    def list_accepted_federated_cloudshares(self):
        # FIXME: doesn't work
        url = self.requester.get_federated_url()
        return self.requester.get(url)

    @nextcloud_method
    def get_known_federated_cloudshare(self, sid):
        url = self.requester.get_federated_url(sid)
        return self.requester.get(url)

    @nextcloud_method
    def delete_accepted_federated_cloudshare(self, sid):
        url = self.requester.get_federated_url(sid)
        return self.requester.delete(url)

    @nextcloud_method
    def list_pending_federated_cloudshares(self, sid):
        url = self.requester.get_federated_url("pending")
        return self.requester.get(url)

    @nextcloud_method
    def accept_pending_federated_cloudshare(self, sid):
        url = self.requester.get_federated_url("pending/{sid}".format(sid=sid))
        return self.requester.post(url)

    @nextcloud_method
    def decline_pending_federated_cloudshare(self, sid):
        url = self.requester.get_federated_url("pending/{sid}".format(sid=sid))
        return self.requester.delete(url)


class Apps(WithRequester):
    API_URL = "/ocs/v1.php/cloud/apps"

    @nextcloud_method
    def get_apps(self, filter=None):
        if filter is True:
            self.query_components.append("filter=enabled")
        elif filter is False:
            self.query_components.append("filter=disabled")
        return self.requester.get()

    @nextcloud_method
    def get_app(self, aid):
        return self.requester.get(aid)

    @nextcloud_method
    def enable_app(self, aid):
        return self.requester.post(aid)

    @nextcloud_method
    def disable_app(self, aid):
        return self.requester.delete(aid)


class Group(WithRequester):
    API_URL = "/ocs/v1.php/cloud/groups"

    @nextcloud_method
    def get_groups(self, search=None, limit=None, offset=None):
        if search is not None or limit is not None or offset is not None:
            if search is not None:
                self.query_components.append("search=%s" % search)
            if limit is not None:
                self.query_components.append("limit=%s" % limit)
            if offset is not None:
                self.query_components.append("offset=%s" % offset)
        return self.requester.get()

    @nextcloud_method
    def add_group(self, gid):
        msg = {"groupid": gid}
        return self.requester.post("", msg)

    @nextcloud_method
    def get_group(self, gid):
        return self.requester.get("{gid}".format(gid=gid))

    @nextcloud_method
    def get_subadmins(self, gid):
        return self.requester.get("{gid}/subadmins".format(gid=gid))

    @nextcloud_method
    def delete_group(self, gid):
        return self.requester.delete("{gid}".format(gid=gid))


class User(WithRequester):
    API_URL = "/ocs/v1.php/cloud/users"

    @nextcloud_method
    def add_user(self, uid, passwd):
        """
        Create a new user on the Nextcloud server

        :param uid: str, uid of new user
        :param passwd: str, password of new user
        :return:
        """
        msg = {'userid': uid, 'password': passwd}
        return self.requester.post("", msg)

    @nextcloud_method
    def get_users(self, search=None, limit=None, offset=None):
        """
        Retrieve a list of users from the Nextcloud server

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

    @nextcloud_method
    def get_user(self, uid):
        """
        Retrieve information about a single user

        :param uid: str, uid of user
        :return:
        """
        return self.requester.get("{uid}".format(uid=uid))

    @nextcloud_method
    def edit_user(self, uid, what, value):
        what_to_key_map = dict(
            email="email", quota="quote", phone="phone", address="address", website="website",
            twitter="twitter", displayname="displayname", password="password",
        )
        assert what in what_to_key_map, (
            "You have chosen to edit user's '{what}', but you can choose only from: {choices}"
            .format(what=what, choices=", ".join(what_to_key_map.keys()))
        )

        url = "{uid}".format(uid=uid)
        msg = dict(
            key=what_to_key_map[what],
            value=value,
        )
        return self.requester.put(url, msg)

    @nextcloud_method
    def disable_user(self, uid):
        """
        Disable a user on the Nextcloud server so that the user cannot login anymore

        :param uid: str, uid of user
        :return:
        """
        return self.requester.put("{uid}/disable".format(uid=uid))

    @nextcloud_method
    def enable_user(self, uid):
        """
        Enable a user on the Nextcloud server so that the user can login again

        :param uid: str, uid of user
        :return:
        """
        return self.requester.put("{uid}/enable".format(uid=uid))

    @nextcloud_method
    def delete_user(self, uid):
        """
        Delete a user from the Nextcloud server

        :param uid: str, uid of user
        :return:
        """
        return self.requester.delete("{uid}".format(uid=uid))

    @nextcloud_method
    def add_to_group(self, uid, gid):
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.post(url, msg)

    @nextcloud_method
    def remove_from_group(self, uid, gid):
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.delete(url, msg)

    @nextcloud_method
    def create_subadmin(self, uid, gid):
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.post(url, msg)

    @nextcloud_method
    def remove_subadmin(self, uid, gid):
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.delete(url, msg)

    @nextcloud_method
    def get_subadmin_groups(self, uid):
        url = "{uid}/subadmins".format(uid=uid)
        return self.requester.get(url)

    @nextcloud_method
    def resend_welcome_mail(self, uid):
        url = "{uid}/welcome".format(uid=uid)
        return self.requester.post(url)


class OCSCode(enum.IntEnum):
    OK = 100
    SERVER_ERROR = 996
    NOT_AUTHORIZED = 997
    NOT_FOUND = 998
    UNKNOWN_ERROR = 999


class ShareType(enum.IntEnum):
    USER = 0
    GROUP = 1
    PUBLIClINK = 3
    FEDERATED_CLOUD_SHARE = 6


class Permission(enum.IntEnum):
    READ = 1
    UPDATE = 2
    CREATE = 4
    DELETE = 8
    SHARE = 16
    ALL = 31


QUOTE_UNLIMITED = -3


def datttetime_to_expireDate(date):
    return date.strftime("%Y-%m-%d")
