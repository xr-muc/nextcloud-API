from .base import BaseTestCase, NEXTCLOUD_VERSION


class TestCapabilities(BaseTestCase):

    def test_get_capabilities(self):
        res = self.nxc.get_capabilities()
        assert res.status_code == self.SUCCESS_CODE
        assert str(res.data['version']['major']) == NEXTCLOUD_VERSION
