import unittest
from copy import copy

import cum


def create_cums():
    cums = []
    for i in range(0, 9):
        cums.append(cum.Cum(seq=0, level=i, total_time=i))
    return cums


class TestingCase(unittest.TestCase):
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

    def test_reconciliate_1(self):
        parent = cum.Cum(0, 0, "ROOT")
        arr = create_cums()
        '''
        it is expected that all the elements be taken account
        '''
        cums = [copy(arr[5]),
                copy(arr[1]),
                copy(arr[2]),
                copy(arr[3]),
                copy(arr[3]),
                copy(arr[2]),
                copy(arr[1]),
                copy(arr[1]),
                cum.Cum(0, 0, "BROTHER"),
                copy(arr[1])]
        next_pos = cum._reconciliate(parent, cums)
        self.assertEqual(3, cums[3].invocation_time)
        self.assertEqual(6, cums[2].invocation_time)
        self.assertEqual(8, cums[1].invocation_time)
        self.assertEqual(15, parent.invocation_time)
        self.assertEqual(8, next_pos)

