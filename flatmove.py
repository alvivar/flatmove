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


TODO
    - Handle files with the same name into the same folder exception
"""

import argparse
import os
import time


def flatmove(source,
             destiny,
             *,
             year=False,
             month=False,
             day=False,
             remove_empty_dirs=True):
    """
    Moves files (including files in subdirectories) from source to destiny. It
    can also create subfolders based on the modified time of the file and
    remove empty dirs.
    """

    for root, dirs, files in os.walk(source, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Date folder creation
            y, m, d, *_ = time.gmtime(os.path.getmtime(file_path))
            date = f"{y if year else ''} "
            f"{m if month else ''} "
            f"{d if day else '' }"

            date_path = os.path.join(destiny, date.strip())
            if not os.path.exists(date_path):
                os.makedirs(date_path)

            # File to date folder
            file_date_path = os.path.join(date_path, file_name)
            if file_date_path != file_path:
                os.rename(file_path, file_date_path)

        # Removing leftovers
        if remove_empty_dirs:
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
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

    args = parser.parse_args()

    flatmove(
        args.source,
        args.source if args.destiny is None else args.destiny,
        year=args.year,
        month=args.month,
        day=args.day)
