from .base import BaseTestCase


class TestActivities(BaseTestCase):

    SUCCESS_CODE = 200

    def test_get_filter_activities(self):
        res = self.nxc.get_activities()
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE

        # test limit
        res = self.nxc.get_activities(limit=1)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        assert len(res['ocs']['data']) <= 1

        # test ascending sorting
        res = self.nxc.get_activities(sort="asc")
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        data = res['ocs']['data']
        for num in range(1, len(data)):
            assert data[num - 1]['activity_id'] <= data[num]['activity_id']

        # test descending sorting
        res = self.nxc.get_activities(sort="asc")
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        data = res['ocs']['data']
        for num in range(1, len(data)):
            assert data[num - 1]['activity_id'] >= data[num]['activity_id']

        # TODO: add tests for since parameter, if WebDAV Directory API will be implemented and it will be possible
        #  to make files manipulation to create activities from api
