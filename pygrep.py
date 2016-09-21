#! venv/bin/python3
import argparse
import logging
import logging.config
import os
import re

import settings

# ANSI escape code for bold green
COLOR_START = '\033[1;92m'
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


def color_wrap(s):
    return COLOR_START + s + COLOR_END


def search(target, pattern):
    if os.path.isdir(target):
        # recursive directory search
        for (this_dir, sub_dirs, files) in os.walk(target):
            logging.debug('this dir: %s sub_dirs: %s files: %s',
                          this_dir, ' '.join(sub_dirs), ' '.join(files))
            for f in files:
                if f.startswith('#') or f.endswith('~'):
                    continue
                if '.CCACHE' in this_dir or 'venv' in this_dir:
                    continue
                full_path = os.path.join(this_dir, f)
                yield from search(full_path, pattern)
    else:
        # single file case
        fp = open(target)
        for (linenum, line) in enumerate(fp):
            match = pattern.findall(line)
            if match:
                yield (target, linenum, line)
        fp.close()


def display_matches(matches, pattern):
    for (file, linenum, line) in matches:
        colored_line = re.sub(pattern, color_wrap('\\1'), line)
        print(file + ":" + str(linenum) + " :: " + colored_line)


if __name__ == '__main__':
    init_logging()
    args = parse_args()
    pattern = re.compile(r'(' + args.query + ')')
    matches = search(args.target, pattern)
    display_matches(matches, pattern)
