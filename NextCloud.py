import enum

import requests


PUBLIC_API_NAME_CLASS_MAP = dict()


class Req():
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

    def get(self, ur=""):
        ur = self.get_full_url(ur)
        res = requests.get(ur, auth=self.auth_pk, headers=self.h_get)
        return self.rtn(res)

    def post(self, ur="", dt=None):
        ur = self.get_full_url(ur)
        if dt is None:
            res = requests.post(ur, auth=self.auth_pk, headers=self.h_post)
        else:
            res = requests.post(ur, auth=self.auth_pk,
                                data=dt, headers=self.h_post)
        return self.rtn(res)

    def put(self, ur="", dt=None):
        ur = self.get_full_url(ur)
        if dt is None:
            res = requests.put(ur, auth=self.auth_pk, headers=self.h_post)
        else:
            res = requests.put(ur, auth=self.auth_pk,
                               data=dt, headers=self.h_post)
        return self.rtn(res)

    def delete(self, ur="", dt=None):
        ur = self.get_full_url(ur)
        if dt is None:
            res = requests.delete(ur, auth=self.auth_pk, headers=self.h_post)
        else:
            res = requests.delete(ur, auth=self.auth_pk,
                                  data=dt, headers=self.h_post)
        return self.rtn(res)

    def get_full_url(self, additional_url=""):
        if additional_url and not additional_url.startswith("/"):
            additional_url = "/" + additional_url

        if self.to_json:
            self.query_components.append("format=json")

        ret = "{base_url}/{api_url}{additional_url}".format(
            base_url=self.base_url, api_url=self.API_URL, additional_url=additional_url)
        if self.query_components:
            ret = "{url}?{query}".format(
                url=ret, query="&".join(self.query_components))

        self.query_components = []
        return ret


def nextcloud_method(method_to_wrap):
    class_name = method_to_wrap.__qualname__.split(".", 1)[0]
    PUBLIC_API_NAME_CLASS_MAP[method_to_wrap.__name__] = class_name
    return method_to_wrap


class NextCloud(object):

    def __init__(self, endpoint, user, passwd, js=False):
        self.query_components = []

        requester = Req(endpoint, user, passwd, js)

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
    def getGroupFolders(self):
        return self.requester.get()

    @nextcloud_method
    def createGroupFolder(self, mountpoint):
        return self.requester.post("", {"mountpoint": mountpoint})

    @nextcloud_method
    def deleteGroupFolder(self, fid):
        return self.requester.delete(fid)

    @nextcloud_method
    def giveAccessToGroupFolder(self, fid, gid):
        url = "/".join(fid, gid)
        return self.requester.post(url)

    @nextcloud_method
    def deleteAccessToGroupFolder(self, fid, gid):
        url = "/".join(fid, gid)
        return self.requester.delete(url)

    @nextcloud_method
    def setAccessToGroupFolder(self, fid, gid, permissions):
        url = "/".join(fid, gid)
        return self.requester.post(url, {"permissions": permissions})

    @nextcloud_method
    def setQuotaOfGroupFolder(self, fid, quota):
        url = "/".join(fid, "quota")
        return self.requester.post(url, {"quota": quota})

    @nextcloud_method
    def renameGroupFolder(self, fid, mountpoint):
        url = "/".join(fid, "mountpoint")
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
    def getShares(self):
        self.requester.get(self.requester.get_local_url())

    @nextcloud_method
    def getSharesFromPath(self, path, reshares=None, subfiles=None):
        url = self.requester.get_local_url(path)

        if reshares is not None:
            self.query_components.append("reshares=true")

        if subfiles is not None:
            self.query_components.append("subfiles=true")

        return self.requester.get(url)

    @nextcloud_method
    def getShareInfo(self, sid):
        self.requester.get(self.requester.get_local_url(sid))

    @nextcloud_method
    def createShare(
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
    def deleteShare(self, sid):
        return self.requester.delete(self.requester.get_local_url(sid))

    @nextcloud_method
    def updateShare(self, sid, permissions=None, password=None, publicUpload=None, expireDate=""):
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
    def listAcceptedFederatedCloudShares(self):
        url = self.requester.get_federated_url()
        return self.requester.get(url)

    @nextcloud_method
    def getKnownFederatedCloudShare(self, sid):
        url = self.requester.get_federated_url(sid)
        return self.requester.get(url)

    @nextcloud_method
    def deleteAcceptedFederatedCloudShare(self, sid):
        url = self.requester.get_federated_url(sid)
        return self.requester.delete(url)

    @nextcloud_method
    def listPendingFederatedCloudShares(self, sid):
        url = self.requester.get_federated_url("pending")
        return self.requester.get(url)

    @nextcloud_method
    def acceptPendingFederatedCloudShare(self, sid):
        url = self.requester.get_federated_url("pending/{sid}".format(sid=sid))
        return self.requester.post(url)

    @nextcloud_method
    def declinePendingFederatedCloudShare(self, sid):
        url = self.requester.get_federated_url("pending/{sid}".format(sid=sid))
        return self.requester.delete(url)


class Apps(WithRequester):
    API_URL = "/ocs/v1.php/cloud/apps"

    @nextcloud_method
    def getApps(self, filter=None):
        if filter is True:
            self.query_components.append("filter=enabled")
        elif filter is False:
            self.query_components.append("filter=disabled")
        return self.requester.get()

    @nextcloud_method
    def getApp(self, aid):
        return self.requester.get(aid)

    @nextcloud_method
    def enableApp(self, aid):
        return self.requester.post(aid)

    @nextcloud_method
    def disableApp(self, aid):
        return self.requester.delete(aid)


class Group(WithRequester):
    API_URL = "/ocs/v1.php/cloud/groups"

    @nextcloud_method
    def getGroups(self, search=None, limit=None, offset=None):
        if search is not None or limit is not None or offset is not None:
            if search is not None:
                self.query_components.append("search=%s" % search)
            if limit is not None:
                self.query_components.append("limit=%s" % limit)
            if offset is not None:
                self.query_components.append("offset=%s" % offset)
        return self.requester.get()

    @nextcloud_method
    def addGroup(self, gid):
        msg = {"groupid": gid}
        return self.requester.post("", msg)

    @nextcloud_method
    def getGroup(self, gid):
        return self.requester.get("{gid}".format(gid=gid))

    @nextcloud_method
    def getSubAdmins(self, gid):
        return self.requester.get("{gid}/subadmins".format(gid=gid))

    @nextcloud_method
    def deleteGroup(self, gid):
        return self.requester.delete("{gid}".format(gid=gid))


class User(WithRequester):
    API_URL = "/ocs/v1.php/cloud/users"

    @nextcloud_method
    def addUser(self, uid, passwd):
        msg = {'userid': uid, 'password': passwd}
        return self.requester.post("", msg)

    @nextcloud_method
    def getUsers(self, search=None, limit=None, offset=None):
        if search is not None or limit is not None or offset is not None:
            if search is not None:
                self.query_components.append("search=%s" % search)
            if limit is not None:
                self.query_components.append("limit=%s" % limit)
            if offset is not None:
                self.query_components.append("offset=%s" % offset)
        return self.requester.get()

    @nextcloud_method
    def getUser(self, uid):
        return self.requester.get("{uid}".format(uid=uid))

    @nextcloud_method
    def editUser(self, uid, what, value):
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
    def disableUser(self, uid):
        return self.requester.put("{uid}/disable".format(uid=uid))

    @nextcloud_method
    def enableUser(self, uid):
        return self.requester.put("{uid}/enable".format(uid=uid))

    @nextcloud_method
    def deleteUser(self, uid):
        return self.requester.delete("{uid}".format(uid=uid))

    @nextcloud_method
    def addToGroup(self, uid, gid):
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.post(url, msg)

    @nextcloud_method
    def removeFromGroup(self, uid, gid):
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.delete(url, msg)

    @nextcloud_method
    def createSubAdmin(self, uid, gid):
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.post(url, msg)

    @nextcloud_method
    def removeSubAdmin(self, uid, gid):
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.requester.delete(url, msg)

    @nextcloud_method
    def getSubAdminGroups(self, uid):
        url = "{uid}/subadmins".format(uid=uid)
        return self.requester.get(url)

    @nextcloud_method
    def resendWelcomeMail(self, uid):
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
