```
usage: flatmove.py [-h] [-y] [-m] [-d] [-b BATCH] source [destiny]

Moves all files (including files in subfolders) from a path to another
(without the subfolders)

positional arguments:
  source                all files under this path will be moved
  destiny               files will be moved here if specified (else will use
                        the source instead)

optional arguments:
  -h, --help            show this help message and exit
  -y, --year            use the modified year of the file as subfolder
  -m, --month           use the modified month of the file as subfolder
  -d, --day             use the modified day of the file as subfolder
  -b BATCH, --batch BATCH
                        Subdivide files in quantities inside enumerated
                        subfolders
```

I use this tool to organize my photos, downloads, single files, etc, into subfolders based on their modified time.

For **example**, this will gather all files inside /photos and organize them in subfolders by year and month, removing empty folders at the end.
```
python flatmove.py -ym /photos
```

*Warning*: Be cautious about using this on files that depend on his folder structure, it could get messy :)
