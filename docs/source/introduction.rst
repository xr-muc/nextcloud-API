Introduction
============

Nextcloud-API is Python (2 and 3) wrapper for NextCloud's API. With it you can manage your
NextCloud instances from Python scripts.

If you have any question, remark or if you find a bug, don't hesitate to
`open an issue <https://github.com/EnterpriseyIntranet/nextcloud-API/issues>`_.




Quick start
-----------

First, create your NextCloud instance:

.. code-block:: python

    from NextCloud import NextCloud

    nxc = NextCloud.NextCloud("url", "user id", "password", js=True)

Then you can work with NextCloud objects:

.. code-block:: python

    nxc.get_users()
    nxc.add_user("new_user_username", "new_user_password321_123")
    nxc.add_group("new_group_name")
    nxc.add_to_group("new_user_username", "new_group_name")

Download and install
--------------------

TBD

License
-------

Nextcloud-API is licensed under the GNU General Public License v3.0.


What's next ?
-------------

Check :doc:`examples` and :doc:`modules`.



