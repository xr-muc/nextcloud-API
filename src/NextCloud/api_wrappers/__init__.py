from .activity import Activity
from .apps import Apps
from .capabilities import Capabilities
from .federated_cloudshares import FederatedCloudShare
from .group import Group
from .group_folders import GroupFolders
from .notifications import Notifications
from .share import Share
from .user import User
from .user_ldap import UserLDAP
from .webdav import WebDAV

OCS_API_CLASSES = [Activity, Apps, Capabilities, FederatedCloudShare, Group, GroupFolders,
                   Notifications, Share, User, UserLDAP]

WEBDAV_CLASS = WebDAV
