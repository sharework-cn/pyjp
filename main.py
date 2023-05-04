from bs4 import BeautifulSoup
import sys
import logging
from csv import writer as csv_writer
from html_parser import parse


def parse_line(line):
    txt = ""
    level = 0
    for td in line.find_all("td"):
        for e in td.contents:
            # the image in the line with 18 pixes width and height can be counted into the hierarchical level
            if str(type(e)) == "<class 'bs4.element.Tag'>" and e.name == "img" \
                    and e["height"] == "18":
                level = level + 1
                # Ignore strings before the last image
                txt = ""
            # the string to be parsed
            if str(type(e)) == "<class 'bs4.element.NavigableString'>":
                txt = txt + e.text
    sections = txt.strip().split("-")

    if len(sections) >= 2:
        return [level,
                get_percent(sections[0]),
                get_total_time(sections[1]),
                get_time(sections[1]),
                get_events(sections[1]),
                get_method(sections[1])]
    else:
        return []


def get_header():
    return ["level", "percent", "total", "current", "events", "method"]


def get_percent(s):
    v = None
    try:
        v = float(s.replace("%", "").strip())
    except Exception as e:
        pass
    return v


def get_total_time(s):
    v = None
    try:
        v = int(s.split(" ms ")[0].replace(",",""))
    except Exception as e:
        pass
    return v


def get_time(s):
    """
    v = s.split("[")[1]
    v = v.replace("ms", "").replace("]", "")
    return int(v)
    """
    return None


def get_events(s):
    """
    v = s.split("evt.")[0]
    v = v.replace(",", "")
    return int(v)
    """
    return None


def get_method(s):
    v = None
    try:
        v = s.split("ms")[1].strip()
    except Exception as e:
        pass
    return v


class CsvWriter:
    def __init__(self, f):
        self.writer = csv_writer(f, dialect="excel")
        self.write_header = True

    def listen(self, cum):
        if self.write_header:
            self.writer.writerow(get_header())
            self.write_header = False
        self.writer.writerow(cum.get_values())


class ConsoleWriter:

    def __init__(self):
        self.count = 0

    def listen(self, cum):
        print(str(cum))
        self.count = self.count + 1


class ConsoleCounterListener:

    def __init__(self):
        self.events = 0

    def listen(self, count):
        print(f"{count} lines written")
        self.events = self.events + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error("Usage: script <input file> <output file>!")
        exit(1)

    source_file = open(sys.argv[1], 'r', encoding='utf-8')
    output_file = open(sys.argv[2], 'w', newline='')
    writer = CsvWriter(output_file)
    exception = None
    try:
        parse(source_file,
              writer.listen,
              decode="utf-8",
              counter_listener=ConsoleCounterListener().listen,
              counter_interval=5000)
    except Exception as e:
        exception = e
    source_file.close()
    output_file.close()
    if exception is not None:
        raise exception
