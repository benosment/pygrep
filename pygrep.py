#! venv/bin/python3
import re
import argparse
import logging
import logging.config
import os

import settings

COLOR_START = '\033[92m'
COLOR_END = '\033[0m'


def parse_args():
    # build the command line parser
    parser = argparse.ArgumentParser(description='grep-like search tool')
    parser.add_argument('query', action='store', help='query to search')
    parser.add_argument('target', action='store', help='file or directory to search')
    parser.add_argument('--debug', action='store_true', help='enable debugging')
    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('args: %s' % repr(args))
    return args


def init_logging():
    logging.config.dictConfig(settings.LOGGING)


def search(target, pattern):
    logging.debug('target: %s' % target)
    if os.path.isdir(target):
        # recursive directory search
        for element in os.listdir(target):
            search(element, pattern)
    else:
        # single file case
        fp = open(target)
        for (linenum, line) in enumerate(fp):
            match = pattern.findall(line)
            if match:
                colored_line = re.sub(pattern, COLOR_START + '\\1' + COLOR_END, line)
                print(target + ":" + str(linenum) + " :: " + colored_line)


if __name__ == '__main__':
    init_logging()
    args = parse_args()
    query = r'(' + args.query + ')'
    search(args.target, re.compile(query))
