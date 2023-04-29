def get_gt_position(arr, x):
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
    def __init__(self, listener):
        self.list = []
        self.listener = listener

    def register_listener(self, listener):
        self.listener = listener

    def push(self, v):
        index = get_gt_position(self.list, v)
        for i in range(index + 1, len(self.list)):
            if self.listener is not None:
                self.listener(self.list[i])
        del self.list[index + 1:]
        self.list.append(v)

    def flush(self):
        for c in self.list:
            if self.listener is not None:
                self.listener(c)
        self.list = []
