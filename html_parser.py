import io
from lxml import etree, html
from cum import Cum, get_header
import stack


class TrExtractor:

    def __init__(self, source):
        self.source = source
        self.buffer = ""

    def __iter__(self):
        return self

    def __next__(self):
        tr_start_tag_pos = -1
        tr_end_tag_pos = -1
        data = None
        skip_bytes_for_end_tag = 0
        while tr_start_tag_pos < 0 and tr_end_tag_pos < 0:
            if tr_start_tag_pos >= 0:
                pos = self.buffer[skip_bytes_for_end_tag:].find("</tr>")
                if pos >= 0:
                    tr_end_tag_pos = pos + skip_bytes_for_end_tag
                    data = self.buffer[tr_start_tag_pos:tr_end_tag_pos + 5]
                    self.buffer = self.buffer[tr_end_tag_pos + 5:]
                else:
                    skip_bytes_for_end_tag = len(self.buffer)
                    try:
                        self.buffer += next(self.source)
                    except StopIteration:
                        data = self.buffer
                        self.buffer = ""
                        pass
            else:
                pos = self.buffer.find("<tr")
                if pos >= 0:
                    tr_start_tag_pos = pos
                else:
                    try:
                        self.buffer = next(self.source)
                    except StopIteration as e:
                        raise e
        return data


def parse_tr(text):
    h = None
    try:
        h = html.fromstring(text)
    except etree.ParserError:
        pass
    if h is None:
        return None
    tree = html.parse(h)
    images = tree.xpath("//img")
    level = 0
    for img in images:
        height = img.get("height")
        if height is not None and height == "18":
            level = level + 1
    return Cum(level=level)


def parse(source, listener, counter_interval=5000, counter_listener=None):
    trs = TrExtractor(source)
    s = stack.Stack(listener)
    count = 0
    for tp in trs:
        tr = tp[1]
        valign = tr.get("valign")
        if valign is not None and valign == "top":
            cum = parse_tr(tr.text)
            if cum is not None and cum.is_valid():
                count = count + 1
                s.push(cum)
                if count % counter_interval == 0:
                    if counter_listener is not None:
                        counter_listener(count)
        tr.clear()
        while tr.getprevious() is not None:
            del tr.getparent()[0]
