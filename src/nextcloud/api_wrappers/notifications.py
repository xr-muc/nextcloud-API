# -*- coding: utf-8 -*-
from nextcloud.base import WithRequester


class Notifications(WithRequester):
    API_URL = "/ocs/v2.php/apps/notifications/api/v2/notifications"
    SUCCESS_CODE = 200

    def get_notifications(self):
        """ Get list of notifications for a logged in user """
        return self.requester.get()

    def get_notification(self, notification_id):
        """
        Get single notification by id for a user

        Args:
            notification_id (int): Notification id

        Returns:

        """
        return self.requester.get(url=notification_id)

    def delete_notification(self, notification_id):
        """
        Delete single notification by id for a user

        Args:
            notification_id (int): Notification id

        Returns:

        """
        return self.requester.delete(url=notification_id)

    def delete_all_notifications(self):
        """ Delete all notification for a logged in user

        Notes:
            This endpoint was added for Nextcloud 14
        """
        return self.requester.delete()
