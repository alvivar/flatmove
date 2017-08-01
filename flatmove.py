"""
usage: flatmove.py [-h] [-y] [-m] [-d] source [destiny]

Moves all files (including files in subfolders) from a path to another
(without the subfolders)

positional arguments:
  source       all files under this path will be moved
  destiny      files will be moved here if specified (else will use the source
               instead)

optional arguments:
  -h, --help   show this help message and exit
  -y, --year   use the modified year of the file as subfolder
  -m, --month  use the modified month of the file as subfolder
  -d, --day    use the modified day of the file as subfolder


I use this tool to organize my photos, downloads, single files, etc, into
subfolders based on their modified time.

For example, this will gather all files inside /photos and organize them in
subfolders by year and month, removing empty folders at the end.

python flatmove.py -ym /photos

*Warning*: Be cautious about using this on files that depend on his folder
structure, it could get messy :)


TODO
    -n --nested Generate folders inside folders
"""

import argparse
import os
import re
import time


def move_file(source, destiny):
    """
    Moves or renames a file from source to destiny, if the file already exists
    a '_' is appended before the extension.
    """

    try:
        os.rename(source, destiny)
    except FileExistsError:
        base = os.path.basename(destiny)
        name, ext = os.path.splitext(destiny)
        alt_destiny = os.path.join(base, name + '_' + ext)
        move_file(source, alt_destiny)


def flatmove(source,
             destiny,
             *,
             year=False,
             month=False,
             day=False,
             batch=0,
             remove_empty_dirs=True):
    """
    Moves files (including files in subdirectories) from source to destiny. It
    can also create subfolders based on the modified time of the file and
    remove empty directories.
    """

    all_date_paths = []
    for root, dirs, files in os.walk(source, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Date folder creation
            y, m, d, *_ = time.gmtime(os.path.getmtime(file_path))
            y = y if year else ''
            m = m if month else ''
            d = d if day else ''
            date = re.sub(" +", " ", f"{y} {m} {d}").strip()

            date_path = os.path.join(destiny, date.strip())
            if not os.path.exists(date_path):
                os.makedirs(date_path)

            # File to date folder
            file_date_path = os.path.join(date_path, file_name)
            if file_date_path != file_path:
                all_date_paths.append(date_path)
                move_file(file_path, file_date_path)

        if remove_empty_dirs:
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

    # Batchefy
    if batch > 0:
        for date_path in list(set(all_date_paths)):
            batchefy(date_path, date_path, size=batch, remove_empty_dirs=False)


def batchefy(source, destiny, *, size=10, remove_empty_dirs=True):
    """
    Moves files (including files in subdirectories) from source to destiny,
    subdividing files in quantities inside enumerated subfolders and removing
    empty directories.
    """

    # 0 batches doesn't make sense
    if size < 1:
        return

    # All
    files = []
    dirs = []
    for root, ds, fs in os.walk(source, topdown=False):
        for file_name in fs:
            files.append(os.path.join(root, file_name))
        for dir_name in ds:
            dirs.append(os.path.join(root, dir_name))

    # Move each file to their enumerated folder
    batches = [files[i:i + size] for i in range(0, len(files), size)]
    for i, b in enumerate(batches):
        dir_name = str(i + 1)

        dir_path = os.path.join(destiny, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for file_path in b:
            file_dir_path = os.path.join(dir_path, os.path.basename(file_path))
            if file_dir_path != file_path:
                move_file(file_path, file_dir_path)

    if remove_empty_dirs:
        for dir_path in dirs:
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Moves all files (including files in subfolders) "
        "from a path to another (without the subfolders)")

    parser.add_argument(
        "source", help="all files under this path will be moved")
    parser.add_argument(
        "destiny",
        help="files will be moved here if specified "
        "(else will use the source instead)",
        nargs='?',
        default=None)
    parser.add_argument(
        "-y",
        "--year",
        help="use the modified year of the file as subfolder",
        action="store_true")
    parser.add_argument(
        "-m",
        "--month",
        help="use the modified month of the file as subfolder",
        action='store_true')
    parser.add_argument(
        "-d",
        "--day",
        help="use the modified day of the file as subfolder",
        action='store_true')
    parser.add_argument(
        "-b",
        "--batch",
        help="Subdivide files in quantities inside enumerated subfolders",
        action='store',
        type=int,
        default=0)

    args = parser.parse_args()

    flatmove(
        args.source,
        args.source if args.destiny is None else args.destiny,
        year=args.year,
        month=args.month,
        day=args.day,
        batch=args.batch)
