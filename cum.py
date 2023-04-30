"""
CUM - Cpu Usage of Method
"""
import sys


def get_header():
    return ["seq", "level", "name", "hits", "time", "percent", "average_time",
            "average_percent", "total_time",
            "total_percent", "invocation_time", "invocation_percent"]


def reconciliate(parent, children):
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
        parent.invocation_time = parent.total_time
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
            elements what level are higher or equals to the CURRENT CALCULATING LEVEL
            will be counted, that means, a previous lower level element is also counted
            for example:
            for parent with level 1, children in [4, 3, 4]
            the leading 4 is counted since CURRENT CALCULATING LEVEL is 4
            3 is counted since CURRENT CALCULATING LEVEL is 3
            the tailing 4 is skipped since CURRENT CALCULATING LEVEL is 3
            '''
            n = reconciliate(c, children[i + 1:])
            reconciliated = True
            if c.level <= calculating_level:
                if c.invocation_time is not None:
                    time = time + c.invocation_time
            '''
            n is the start of next iteration, so we set i to n - 1
            '''
            i = i + n
        i = i + 1
    if reconciliated:
        parent.invocation_time = time
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

    def get_values(self):
        return [
            self.seq,
            self.level,
            self.name,
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

    def __str__(self):
        return f"{self.level} - {self.name}"

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
