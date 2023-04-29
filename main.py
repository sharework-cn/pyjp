from bs4 import BeautifulSoup
import sys
import logging
import csv


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error("Usage: script <input file> <output file>!")
        exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), features='html.parser')
        with open(sys.argv[2], 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect="excel")
            writer.writerow(get_header())
            cnt = 0
            for tr in soup.find_all("tr"):
                if tr.attrs.get("valign") == "top":
                    result = parse_line(tr)
                    if len(result) > 0:
                        writer.writerow(result)
                cnt = cnt + 1
                if cnt % 5000 == 0:
                    print(str(cnt) + " lines read")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
