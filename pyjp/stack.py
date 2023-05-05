def get_gt_position(arr, x):
    """
    Get the nearest LESS THAN EQUALS element in an ordered array, returns the MOST RIGHT
    index of an element which is less than or equals to the given value.

    Returns -1 when a valid element can not be found in the array

    For example, in the array [1, 2, 2, 2, 9], the MOST RIGHT position to match value 2 is 3
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        v = arr[mid]
        if v <= x:
            left = mid + 1
        else:
            right = mid - 1
    return right


class Stack:
    def __init__(self, drop_listener, calc_listener):
        self.list = []
        self.drop_listener = drop_listener
        self.calc_listener = calc_listener

    def register_drop_listener(self, listener):
        self.drop_listener = listener

    def register_calc_listener(self, listener):
        self.calc_listener = listener

    def push(self, v):
        index = get_gt_position(self.list, v)
        parent = None
        if index >= 0:
            parent = self.list[index]
        children = self.list[index + 1:]
        if self.calc_listener is not None:
            self.calc_listener(parent, children)
        for i in range(index + 1, len(self.list)):
            if self.drop_listener is not None:
                self.drop_listener(self.list[i])
        del self.list[index + 1:]
        self.list.append(v)

    def flush(self):
        if self.calc_listener is not None:
            self.calc_listener(None, self.list)
        for c in self.list:
            if self.drop_listener is not None:
                self.drop_listener(c)
        self.list = []
