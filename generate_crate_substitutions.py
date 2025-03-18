#!/usr/bin/env python3

import os


def parse_sec_list(sec_list):
    sections = []
    for entry in sec_list.split(','):
        entry = entry.strip()
        if '-' in entry:
            start_str, end_str = entry.split('-', 1)
            start = int(start_str)
            end = int(end_str)
            sections.extend(range(start, end + 1))
        else:
            num = int(entry)
            sections.append(num)
    unique_sorted = sorted(set(sections))
    return [f"{num:02d}" for num in unique_sorted]


if __name__ == '__main__':
    sec_list = os.getenv('SEC_LIST', default='01-20')

    sections = parse_sec_list(sec_list)

    with open('db/crates.substitutions', 'w') as f:
        f.write('file "db/sector.db"\n')

        f.write('{pattern {SEC}\n')
        for sec in sections:
            f.write(f'{{{sec}}}\n')
        f.write('}\n')
