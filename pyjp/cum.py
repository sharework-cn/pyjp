"""
CUM - Cpu Usage of Method
"""
import sys


def _get_header():
    return ["seq", "level", "name", "parent_method", "hits", "time", "percent", "average_time",
            "average_percent", "total_time",
            "total_percent", "invocation_time", "invocation_percent"]


def _reconciliate(parent, children):
    """
    Calculate the total invocation time of a parent method. It adds up the total_times
    of all its children methods. It's important to note that if a child CUM (CPU Usage of Method)
    has children of its own, the calculation will iterate into those as well.

    In cases where the parent is omitted, the calculation will be triggered for all
    the children CUMs.
    """
    calculating_level = sys.maxsize
    time = 0
    parent_level = 0
    i = 0
    reconciliated = False
    if parent is not None:
        '''
        by default, the invocation time is total time, but is can be overriden by
        the sum of children's invocation time
        '''
        if not parent.calculated:
            # print(f'{parent.seq} - {parent.level} - {parent.total_time}')
            parent.invocation_time = parent.total_time
            parent.time = parent.total_time
        parent_level = parent.level

    while True:
        if i >= len(children):
            break
        c = children[i]
        # stop processing before a brother or parent
        if c.level <= parent_level:
            break
        else:
            '''
            calculating_level is the level of nearest descendant
            who is the highest level(lower number)
            '''
            if c.level <= calculating_level:
                calculating_level = c.level
            '''
            All elements that are at the same level or greater than the CURRENT CALCULATING LEVEL will be counted, 
            which means that any previously greater level elements will also be included in the count.
            for example:
            for parent with level 1, children in [4, 3, 4]
            the leading 4 is counted since CURRENT CALCULATING LEVEL is 4
            3 is counted since CURRENT CALCULATING LEVEL is 3
            the tailing 4 is skipped since CURRENT CALCULATING LEVEL is 3
            '''
            n = _reconciliate(c, children[i + 1:])
            reconciliated = True
            if c.level <= calculating_level:
                if c.total_time is not None:
                    time = time + c.total_time
            '''
            n is the start of next iteration, so we set i to n - 1
            '''
            i = i + n
        i = i + 1
    if reconciliated and parent is not None:
        # print(f'{parent.seq} - {parent.level} - {time} / {parent.total_time}')
        parent.invocation_time = time
        if parent.total_time is not None:
            parent.time = parent.total_time - parent.invocation_time
        parent.higher_level_method = True
        parent.calculated = True
    return i


class Cum:
    def __init__(self,
                 seq=0,
                 level=0,
                 name="",
                 hits=None,
                 time=None,
                 percent=None,
                 average_time=None,
                 average_percent=None,
                 total_time=None,
                 total_percent=None,
                 invocation_time=None,
                 invocation_percent=None):
        self.seq = seq
        self.level = level
        self.name = name
        self.hits = hits
        self.time = time
        self.percent = percent
        self.average_time = average_time
        self.average_percent = average_percent
        self.total_time = total_time
        self.total_percent = total_percent
        self.invocation_time = invocation_time
        self.invocation_percent = invocation_percent
        self.calculated = False
        self.higher_level_method = False

    def get_values(self):
        return [
            self.seq,
            self.level,
            self.name,
            self.higher_level_method,
            self.hits,
            self.time,
            self.percent,
            self.average_time,
            self.average_percent,
            self.total_time,
            self.total_percent,
            self.invocation_time,
            self.invocation_percent
        ]

    def is_valid(self):
        return self.level > 0 and len(self.name) > 0

    def __str__(self):
        lowest_flag = ""
        if self.higher_level_method:
            lowest_flag = "*"
        return f"{self.seq} - {self.level} - {self.total_percent}% - {self.time}/{self.invocation_time}/{self.total_time} ms - {self.name}{lowest_flag}"

    def __lt__(self, other):
        return self.level < other.level

    def __eq__(self, other):
        return self.level == other.level

    def __le__(self, other):
        return self.level <= other.level

    def __ne__(self, other):
        return self.level != other.level

    def __gt__(self, other):
        return self.level > other.level

    def __ge__(self, other):
        return self.level >= other.level
