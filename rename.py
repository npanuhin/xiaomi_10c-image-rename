from collections.abc import Iterator
from itertools import count
import os
import re


with open('regex.txt', 'r', encoding='utf-8') as file:
    regex = file.read().strip()

assert os.path.isfile('path.txt'), 'Create a file "path.txt" with the path to the desired folder for processing'
with open('path.txt', 'r', encoding='utf-8') as file:
    PATH = file.read().strip()


def mkpath(*paths: str) -> str:
    return os.path.normpath(os.path.join(PATH, *paths))


def additional() -> Iterator[str]:
    yield ''
    for i in count(start=1):
        yield f'_{i}'


print(f'Processing {PATH}...')

for path, folders, files in os.walk(mkpath()):
    for filename in files:
        match = re.fullmatch(regex, filename, re.IGNORECASE | re.VERBOSE | re.MULTILINE)
        if not match:
            print(f'Filename {filename} was not recognized')
            continue

        for suffix in additional():
            new_filename = (
                f"{match['year']}-{match['month']}-{match['day']}"
                f"_"
                f"{match['hour']}.{match['minutes']}.{match['seconds']}"
                f"{suffix}"
                f"{match['extention']}"
            )
            if not os.path.isfile(mkpath(path, new_filename)):
                # print(f'Renaming {mkpath(path, filename)} to {mkpath(path, new_filename)}')
                os.rename(mkpath(path, filename), mkpath(path, new_filename))
                break
            # else:
            #     print(f'Cannot rename {mkpath(path, filename)} to {mkpath(path, new_filename)}, attempting new suffix')

    assert len(os.listdir(mkpath(path))) == len(files) + len(folders)

print('Completed')
