import enum

import requests


class Req():
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


class GroupFolders():
    API_URL = "/apps/groupfolders/folders"

    def getGroupFolders(self):
        return self.get()

    def createGroupFolder(self, mountpoint):
        return self.post("", {"mountpoint": mountpoint})

    def deleteGroupFolder(self, fid):
        return self.delete(fid)

    def giveAccessToGroupFolder(self, fid, gid):
        url = "/".join(fid, gid)
        return self.post(url)

    def deleteAccessToGroupFolder(self, fid, gid):
        url = "/".join(fid, gid)
        return self.delete(url)

    def setAccessToGroupFolder(self, fid, gid, permissions):
        url = "/".join(fid, gid)
        return self.post(url, {"permissions": permissions})

    def setQuotaOfGroupFolder(self, fid, quota):
        url = "/".join(fid, "quota")
        return self.post(url, {"quota": quota})

    def renameGroupFolder(self, fid, mountpoint):
        url = "/".join(fid, "mountpoint")
        return self.post(url, {"mountpoint": mountpoint})


class Share():
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

    def getShares(self):
        self.get(self.get_local_url())

    def getSharesFromPath(self, path, reshares=None, subfiles=None):
        url = self.get_local_url(path)

        if reshares is not None:
            self.query_components.append("reshares=true")

        if subfiles is not None:
            self.query_components.append("subfiles=true")

        return self.get(url)

    def getShareInfo(self, sid):
        self.get(self.get_local_url(sid))

    def createShare(
            self, path, shareType, shareWith=None, publicUpload=None, password=None,
            permissions=None):
        url = self.get_local_url()
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
        return self.post(url, msg)

    def deleteShare(self, sid):
        return self.delete(self.get_local_url(sid))

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
        url = self.get_local_url(sid)
        return self.put(url, msg)

    def listAcceptedFederatedCloudShares(self):
        url = self.get_federated_url()
        return self.get(url)

    def getKnownFederatedCloudShare(self, sid):
        url = self.get_federated_url(sid)
        return self.get(url)

    def deleteAcceptedFederatedCloudShare(self, sid):
        url = self.get_federated_url(sid)
        return self.delete(url)

    def listPendingFederatedCloudShares(self, sid):
        url = self.get_federated_url("pending")
        return self.get(url)

    def acceptPendingFederatedCloudShare(self, sid):
        url = self.get_federated_url("pending/{sid}".format(sid=sid))
        return self.post(url)

    def declinePendingFederatedCloudShare(self, sid):
        url = self.get_federated_url("pending/{sid}".format(sid=sid))
        return self.delete(url)


class Apps():
    API_URL = "/ocs/v1.php/cloud/apps"

    def getApps(self, filter=None):
        if filter is True:
            self.query_components.append("filter=enabled")
        elif filter is False:
            self.query_components.append("filter=disabled")
        return self.get()

    def getApp(self, aid):
        return self.get(aid)

    def enableApp(self, aid):
        return self.post(aid)

    def disableApp(self, aid):
        return self.delete(aid)


class Group():
    API_URL = "/ocs/v1.php/cloud/groups"

    def getGroups(self, search=None, limit=None, offset=None):
        if search is not None or limit is not None or offset is not None:
            if search is not None:
                self.query_components.append("search=%s" % search)
            if limit is not None:
                self.query_components.append("limit=%s" % limit)
            if offset is not None:
                self.query_components.append("offset=%s" % offset)
        return self.get()

    def addGroup(self, gid):
        msg = {"groupid": gid}
        return self.post("", msg)

    def getGroup(self, gid):
        return self.get("{gid}".format(gid=gid))

    def getSubAdmins(self, gid):
        return self.get("{gid}/subadmins".format(gid=gid))

    def deleteGroup(self, gid):
        return self.delete("{gid}".format(gid=gid))


class User():
    API_URL = "/ocs/v1.php/cloud/users"

    def addUser(self, uid, passwd):
        msg = {'userid': uid, 'password': passwd}
        return self.post("", msg)

    def getUsers(self, search=None, limit=None, offset=None):
        if search is not None or limit is not None or offset is not None:
            if search is not None:
                self.query_components.append("search=%s" % search)
            if limit is not None:
                self.query_components.append("limit=%s" % limit)
            if offset is not None:
                self.query_components.append("offset=%s" % offset)
        return self.get()

    def getUser(self, uid):
        return self.get("{uid}".format(uid=uid))

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
        return self.put(url, msg)

    def disableUser(self, uid):
        return self.put("{uid}/disable".format(uid=uid))

    def enableUser(self, uid):
        return self.put("{uid}/enable".format(uid=uid))

    def deleteUser(self, uid):
        return self.delete("{uid}".format(uid=uid))

    def addToGroup(self, uid, gid):
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.post(url, msg)

    def removeFromGroup(self, uid, gid):
        url = "{uid}/groups".format(uid=uid)
        msg = {'groupid': gid}
        return self.delete(url, msg)

    def createSubAdmin(self, uid, gid):
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.post(url, msg)

    def removeSubAdmin(self, uid, gid):
        url = "{uid}/subadmins".format(uid=uid)
        msg = {'groupid': gid}
        return self.delete(url, msg)

    def getSubAdminGroups(self, uid):
        url = "{uid}/subadmins".format(uid=uid)
        return self.get(url)

    def resendWelcomeMail(self, uid):
        url = "{uid}/welcome".format(uid=uid)
        return self.post(url)


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


class NextCloud(Req, User, Group, Apps, Share, GroupFolders):

    def __init__(self, endpoint, user, passwd, js=False):
        self.query_components = []

        self.to_json = js

        self.base_url = endpoint
        # GroupFolders.url = endpoint + "/ocs/v2.php/apps/groupfolders/folders"

        self.h_get = {"OCS-APIRequest": "true"}
        self.h_post = {"OCS-APIRequest": "true",
                       "Content-Type": "application/x-www-form-urlencoded"}
        self.auth_pk = (user, passwd)
