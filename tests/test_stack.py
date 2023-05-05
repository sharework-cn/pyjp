import unittest
from pyjp import stack


class NumericDropListener:
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


class NumericCalcListener:
    def __init__(self):
        self.list_parent = []
        self.list_children = []

    def listen(self, parent, children):
        self.list_parent.append(parent)
        self.list_children.append(children)

    def get_recent_elements(self):
        e = [list(self.list_parent), list(self.list_children)]
        self.reset()
        return e

    def get_length(self):
        return len(self.list_parent)

    def reset(self):
        self.list_parent.clear()
        self.list_children.clear()

    def __str__(self):
        texts = []
        for i in range(0, len(self.list_parent)):
            if self.list_parent[i] is None:
                p = 0
            else:
                p = self.list_parent[i]
            texts.append(f'{p}({",".join(map(str, self.list_children[i]))})')
        return "|".join(texts)


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
        lo = NumericDropListener()
        lc = NumericCalcListener()
        s = stack.Stack(lo.listen, lc.listen)
        s.push(1)
        self.assertEqual("", str(lo))
        self.assertEqual("0()", str(lc))
        s.push(1)
        self.assertEqual("", str(lo))
        self.assertEqual("0()|1()", str(lc))
        s.push(2)
        s.push(2)
        self.assertEqual("", str(lo))
        self.assertEqual("0()|1()|1()|2()", str(lc))
        s.push(3)
        self.assertEqual("", str(lo))
        self.assertEqual("0()|1()|1()|2()|2()", str(lc))
        s.push(5)
        self.assertEqual("0()|1()|1()|2()|2()|3()", str(lc))
        s.push(1)
        self.assertEqual("0()|1()|1()|2()|2()|3()|1(2,2,3,5)", str(lc))
        self.assertEqual("2,2,3,5", str(lo))
        lo.reset()
        lc.reset()
        s.push(4)
        self.assertEqual("1()", str(lc))
        s.push(1)
        self.assertEqual("4", str(lo))
        self.assertEqual("1()|1(4)", str(lc))

        lo.reset()
        lc.reset()
        s.flush()
        self.assertEqual("1,1,1,1", str(lo))
        self.assertEqual("0(1,1,1,1)", str(lc))

    def test_irregular_steps(self):
        lo = NumericDropListener()
        lc = NumericCalcListener()
        s = stack.Stack(lo.listen, lc.listen)
        s.push(4)
        self.assertEqual("", str(lo))
        self.assertEqual("0()", str(lc))
        s.push(1)
        self.assertEqual("4", str(lo))
        self.assertEqual("0()|0(4)", str(lc))


