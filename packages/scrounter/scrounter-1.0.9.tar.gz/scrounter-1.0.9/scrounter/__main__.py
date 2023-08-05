#!/usr/bin/env python3

from scrounter.src.reader import Reader
from scrounter.src.writer import Writer
from argparse import ArgumentParser

writer: Writer = Writer()


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default='.\\', dest='path', help='the path')
    parser.add_argument('-i', '--init', dest='init', action='store_true', help='create a .counterignore file')
    parser.add_argument('-b', '--blank', dest='blank_lines', action='store_false', help='count blank lines')
    parser.add_argument('-v', '--version', dest='version', action='store_true', help='check version')
    args = parser.parse_args()

    path = args.path

    if args.version:
        print('1.0.9')
        exit()

    if args.init:
        writer.create_ignore_file(path)
        exit()

    blank_lines = args.blank_lines
    reader: Reader = Reader(blank_lines)
    total_lines = reader.open_input_path(path)
    print(f'Lines: {total_lines}')


if __name__ == '__main__':
    main()
