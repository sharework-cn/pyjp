import unittest
import cum


class TestingCase(unittest.TestCase):

    def test_for(self):


    def test_comparison(self):
        cum0 = cum.Cum(0, 0, "0")
        cum1 = cum.Cum(1, 1, "1")
        cum2 = cum.Cum(2, 2, "2")
        cumx = cum.Cum(1, 1, "1")
        self.assertTrue(cum0 < cum1)
        self.assertTrue(cum0 <= cum1)
        self.assertTrue(cum0 != cum1)
        self.assertTrue(cumx <= cum1)
        self.assertTrue(cumx == cum1)
        self.assertTrue(cum1 < cum2)
        self.assertTrue(cum1 <= cum2)

