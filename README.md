A tool to automatically rename .something files to their .something_else 
counterparts, based on filename similarity.

Originally concieved to bulk rename subtitle files with one naming pattern to 
the correspondent video files (which followed a different naming pattern).

Screenshot (text too large to fit github preview thingy):
![Screenshot](https://raw.github.com/a442/nwRename/master/screenshot.png "Screenshot")

```
usage: python nwRename.py [-h] [--no-backup] [-e [EXTENSION]] [dir]

Auto rename files based on similarity.

assumes:
        There are only files of two different 3-letter extensions in the folder.

positional arguments:
  dir              The directory where the files are (default is the dir from
                   which this file was called. Use only absolute paths.)

optional arguments:
  -h, --help       show this help message and exit
  --no-backup, -n  Don't backup the files before renaming (only the ones with
                   the provided extension are renamed).
  -e [EXTENSION]   File extension. Default is .srt.
```

This software comes with ABSOLUTELY NO WARRANTY.

For copying see LICENSE.
