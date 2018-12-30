Examples
========

Users API methods
-----------------

.. code-block:: python

    # get all users
    nxc.get_users()

    # add new user
    nxc.add_user("user_username", "new_user_password321_123")

    # get user by user id
    nxc.get_user("user_username")

    # edit user
    nxc.edit_user("user_username", "phone", "123456789")

    # disable user by user id
    nxc.disable_user("user_username")

    # enable user by user id
    nxc.enable_user("user_username")

    # delete user by user id
    nxc.delete_user("user_username")

    # add user to group by user id and group id
    nxc.add_to_group("user_username", "group_id")

    # remove user from group id
    nxc.remove_from_group("user_username", "group_id")

    # make user subadmin for group
    nxc.create_subadmin("user_username", "group_id")

    # remove user from gorup subadmins
    nxc.remove_subadmin("user_username", "group_id")

    # get groups in which user is subadmin
    nxc.get_subadmin_groups("user_username")

    # trigger welcome email for user again
    nxc.resend_welcome_mail("user_username")


