import argparse
import json
import re
import sys
from typing import TextIO

from . import REQUEST_LINE_RE, VALUES_LINE_RE, CLOSING_LINE_RE


# Setup argparse
argparser = argparse.ArgumentParser(
    description="Translate a CiviProxy logfile into JSON format. ")
argparser.add_argument("-f",
                       "--logfile",
                       help="CiviProxy logfile",
                       type=argparse.FileType("r", encoding="UTF-8"),
                       default=(None if sys.stdin.isatty() else sys.stdin))
argparser.add_argument("-i",
                       "--indent",
                       help="number of spaces to indent JSON output",
                       type=int,
                       default=4)


def main():
    args = argparser.parse_args()

    # Print info if no logfile is specified or passed via stdin
    if not args.logfile:
        print("Please specify a path to a CiviProxy logfile")
        sys.exit()

    # Parse logfile and print it to console
    print(json.dumps(translate_logfile(args.logfile), indent=args.indent))


def translate_logfile(logfile: TextIO) -> list:
    json_ = []
    with logfile as file:
        array = {}
        for line in file:
            request_line = re.search(REQUEST_LINE_RE, line)
            values_line = re.search(VALUES_LINE_RE, line)
            close_line = re.search(CLOSING_LINE_RE, line)
            if request_line:
                array["date"] = request_line.group("date")
                array["time"] = request_line.group("time")
                array["source"] = request_line.group("source")
            elif values_line:
                if values_line.group("key") == "json":
                    array["values"] = json.loads(values_line.group("value"))
                else:
                    array[values_line.group("key")] = values_line.group("value")
            elif close_line:
                if array:
                    json_.append(array)
                    array = {}
    return json_


if __name__ == "__main__":
    main()
