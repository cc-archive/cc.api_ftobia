
from cc.api.tests import *

class TestRoot(TestController):

    def test_trivial(self):
        res = self.app.get('/')
        assert res is not None
