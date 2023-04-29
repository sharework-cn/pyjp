"""
CUM - Cpu Usage of Method
"""
import sys


def get_header():
    return ["seq", "level", "name", "hits", "time", "percent", "average_time",
            "average_percent", "total_time",
            "total_percent", "invocation_time", "invocation_percent"]


def reconciliate(parent, children):
    parent_level = parent.level
    calculating_level = sys.maxsize
    time = 0
    for i in range(0, len(children)):
        c = children[i]
        if c.level <= parent_level:
            return i
        else:
            if c.level <= calculating_level:
                calculating_level = c.level
                n = reconciliate(c, children[i + 1:])
                if c.total_time is not None:
                    time = time + c.total_time
                    i = n
            if c.level == calculating_level:
                if c.total_time is not None:
                    time = time + c.total_time
    if parent.invocation_time is None:
        parent.invocation_time = 0
    parent.invocation_time = parent.invocation_time + time
        else:
            if c.level == calculating_level:
                total = total + c.total_time
        
            
    for c in children:
        if c.level == children_level


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
