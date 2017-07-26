```
usage: flatmove.py [-h] [-y] [-m] [-d] source [destiny]

Move all files (including files in subfolders) from a path to another

positional arguments:
  source       all files under this path will be moved
  destiny      files will be moved here if specified (else will use the same
               source instead)

optional arguments:
  -h, --help   show this help message and exit
  -y, --year   use the modified year of the file as subfolder
  -m, --month  use the modified month of the file as subfolder
  -d, --day    use the modified day of the file as subfolder
```
