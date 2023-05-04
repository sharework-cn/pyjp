import re
from os import path
from cum import _get_header
from csv import writer as csv_writer
from html_parser import parse
import click


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
        print(".", end="")
        self.events = self.events + 1


class CsvWriter:
    def __init__(self, f):
        self.writer = csv_writer(f, dialect="excel")
        self.write_header = True

    def listen(self, cum):
        if self.write_header:
            self.writer.writerow(_get_header())
            self.write_header = False
        self.writer.writerow(cum.get_values())


# Press the green button in the gutter to run the script.
@click.command()
@click.argument("source",
                required=True,
                type=click.Path(exists=True))
@click.option("-d", "--destination",
              type=str,
              help="The file name to be parsed, default to the source_file.csv with the same folder")
@click.option("-p", "--pattern",
              type=str,
              help="""The regex pattern to extract information from the line text, supported
               named variables are: time, percentage, average_time, events, method""")
@click.option("--decode",
              type=str,
              default="utf-8",
              show_default=True,
              help="Decode used to read the file")
@click.option("--overwrite",
              "overwrite",
              flag_value=True,
              type=bool,
              default=False,
              help="Overwrite an exist file, default is False")
@click.option("--interval", "progress_interval",
              type=click.IntRange(2, 50000),
              default=2000,
              help="The interval to print in progress message")
def process(source,
            destination=None,
            pattern=None,
            decode="utf-8",
            overwrite=False,
            progress_interval=2000):
    """
    A tool to parse the exported HTML JProfile report, it adds level and invocation time of
    children methods, which is useful to get the elapsed time by the calling method itself.
    """
    if destination is None:
        destination = path.join(path.dirname(source), path.basename(source) + ".csv")
    write_mode = "x"
    if overwrite:
        write_mode = "w"
    if pattern is None:
        pattern = r'(?P<percentage>\d+(?:\.\d+)?)%\s*-\s*(?P<time>\d{1,3}(?:,\d{3})*|\d+)\s*ms\s*(?P<method>.*)'
    else:
        pattern = re.compile(pattern)
    source_file = open(source, 'r', encoding=decode)
    output_file = open(destination, write_mode, newline='')
    writer = CsvWriter(output_file)
    exception = None
    print("Parsing", end="")
    try:
        parse(source_file,
              writer.listen,
              decode=decode,
              pattern=pattern,
              counter_listener=ConsoleCounterListener().listen,
              counter_interval=progress_interval)
    except Exception as e:
        exception = e
    source_file.close()
    output_file.close()
    if exception is not None:
        raise exception
    else:
        print("Done!")


if __name__ == '__main__':
    process()
