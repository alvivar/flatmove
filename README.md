```
usage: flatmove.py [-h] [-y] [-m] [-d] source [destiny]

Move all files (including files in subfolders) from a path to another (without
the subfolders)

positional arguments:
  source       all files under this path will be moved
  destiny      files will be moved here if specified (else will also use the
               source instead)

optional arguments:
  -h, --help   show this help message and exit
  -y, --year   use the modified year of the file as subfolder
  -m, --month  use the modified month of the file as subfolder
  -d, --day    use the modified day of the file as subfolder
```

I use this tool to organize photos, downloads, single files, etc, into folders based on their modified time.

For **example**, this will gather all files inside /photos and organize them in subfolders by year and month, removing empty folders at the end.
```
python flatmove.py -ym /photos
```

*Warning*: Don't use this on files that depend on his directory structure, it could get messy :P I'll support this feature later though!
