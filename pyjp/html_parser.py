import re
from lxml import html
from lxml.etree import XPath
from lxml.cssselect import CSSSelector
from pyjp.cum import Cum, _reconciliate
from pyjp import stack


class TrIterator:

    def __init__(self, source, decode="utf-8"):
        self.source = source
        self.decode = decode
        self.buffer = ""

    def __iter__(self):
        return self

    def __next__(self):
        start_pos = -1
        end_pos = -1
        data = None
        bytes_to_skip = 0
        while start_pos < 0 or end_pos < 0:
            if start_pos >= 0:
                pos = self.buffer.find("</tr>", bytes_to_skip)
                if pos >= 0:
                    end_pos = pos + bytes_to_skip
                    data = self.buffer[start_pos:end_pos + 5]
                    self.buffer = self.buffer[end_pos + 5:]
                else:
                    bytes_to_skip = len(self.buffer)
                    try:
                        line = next(self.source)
                        if isinstance(line, str):
                            self.buffer += line
                        else:
                            if line is not None:
                                self.buffer += line.decode(self.decode)
                    except StopIteration:
                        data = self.buffer
                        self.buffer = ""
                        pass
            else:
                pos = self.buffer.find("<tr")
                if pos >= 0:
                    start_pos = pos
                    if self.buffer[pos:pos + 5] == "<tr/>":
                        data = "<tr/>"
                        self.buffer = self.buffer[pos + 5:]
                        break
                else:
                    try:
                        line = next(self.source)
                        if isinstance(line, str):
                            self.buffer = line
                        else:
                            if line is not None:
                                self.buffer = line.decode(self.decode)
                            else:
                                self.buffer = ""
                    except StopIteration as e:
                        raise e
        tr = None
        try:
            tr = html.fromstring(data)
        except Exception:
            pass
        return tr


def _parse_tr(tr,
              pattern=r'(?P<percentage>\d+(?:\.\d+)?)%\s*-\s*(?P<time>\d{1,3}(?:,\d{3})*|\d+)\s*ms\s*(?P<method>.*)'):
    images = tr.cssselect("img")
    level = 0
    for img in images:
        height = img.get("height")
        if height is not None and height == "18":
            level = level + 1
    ngs_selector = CSSSelector(':not(:empty)')
    ngs_elements = ngs_selector(tr)
    ngs_xpath = XPath('text()')
    text = ""
    for e in ngs_elements:
        ngs = ngs_xpath(e)
        if ngs:
            text += "".join(ngs)
    cum = Cum(level=level)
    match = re.search(pattern, text)
    try:
        cum.total_time = int(match.group('time').replace(',', ''))
        cum.total_percent = float(match.group('percentage'))
        cum.name = match.group('method').strip()
        cum.hits = int(match.group('events').replace(',', ''))
        cum.average_time = int(match.group('average_time').replace(',', ''))
    except Exception:
        pass
    return cum


def parse(source,
          listener,
          pattern=r'(?P<percentage>\d+(?:\.\d+)?)%\s*-\s*(?P<time>\d{1,3}(?:,\d{3})*|\d+)\s*ms\s*(?P<method>.*)',
          decode="utf-8",
          counter_interval=5000,
          counter_listener=None):
    trs = TrIterator(source, decode=decode)
    s = stack.Stack(listener, _reconciliate)
    count = 0
    for tr in trs:
        if tr is not None:
            valign = tr.get("valign")
            if valign is not None and valign == "top":
                cum = _parse_tr(tr, pattern)
                if cum is not None and cum.is_valid():
                    count = count + 1
                    cum.seq = count
                    s.push(cum)
                    if count % counter_interval == 0:
                        if counter_listener is not None:
                            counter_listener(count)
    s.flush()

