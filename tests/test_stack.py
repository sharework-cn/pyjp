import unittest
import stack


class NumericListener:
    def __init__(self):
        self.list = []

    def listen(self, v):
        self.list.append(v)

    def get_recent_elements(self):
        e = list(self.list)
        self.list.clear()
        return e

    def reset(self):
        self.list.clear()

    def __str__(self):
        return ",".join(map(str, self.list))


class TestingCase(unittest.TestCase):

    def test_get_gt_position(self):
        arr1 = [1, 2, 3, 4, 4, 4, 5, 9, 9, 11, 12]
        arr2 = []
        arr3 = [1]
        arr4 = [1, 1, 1]
        pos = stack.get_gt_position(arr1, 4)
        self.assertEqual(5, pos)
        pos = stack.get_gt_position(arr1, 3)
        self.assertEqual(2, pos)
        pos = stack.get_gt_position(arr1, 10)
        self.assertEqual(8, pos)
        pos = stack.get_gt_position(arr1, 13)
        self.assertEqual(10, pos)
        pos = stack.get_gt_position(arr1, 0)
        self.assertEqual(-1, pos)
        pos = stack.get_gt_position(arr2, 4)
        self.assertEqual(-1, pos)
        pos = stack.get_gt_position(arr3, 1)
        self.assertEqual(0, pos)
        pos = stack.get_gt_position(arr3, 2)
        self.assertEqual(0, pos)
        pos = stack.get_gt_position(arr4, 1)
        self.assertEqual(2, pos)
        pos = stack.get_gt_position(arr4, 0)
        self.assertEqual(-1, pos)
        pos = stack.get_gt_position(arr4, 2)
        self.assertEqual(2, pos)

    def test_normal_steps(self):
        lo = NumericListener()
        listener = lo.listen
        s = stack.Stack(listener)
        s.push(1)
        self.assertEqual("", str(lo))
        s.push(1)
        self.assertEqual("", str(lo))
        s.push(2)
        s.push(2)
        self.assertEqual("", str(lo))
        s.push(3)
        self.assertEqual("", str(lo))
        s.push(5)
        s.push(1)
        self.assertEqual("2,2,3,5", str(lo))
        lo.reset()
        s.push(4)
        s.push(1)
        self.assertEqual("4", str(lo))
        lo.reset()
        s.flush()
        self.assertEqual("1,1,1,1", str(lo))

    def test_irregular_steps(self):
        lo = NumericListener()
        listener = lo.listen
        s = stack.Stack(listener)
        s.push(4)
        self.assertEqual("", str(lo))
        s.push(1)
        self.assertEqual("4", str(lo))


