# xlsx2csv

> xlsx to csv converter

Converts xlsx files to csv format.
Handles large XLSX files. Fast and easy to use.

**Usage:**
```
 xlsx2csv.py [-h] [-v] [-a] [-c OUTPUTENCODING] [-s SHEETID]
                   [-n SHEETNAME] [-d DELIMITER] [-l LINETERMINATOR]
                   [-f DATEFORMAT] [--floatformat FLOATFORMAT]
                   [-i] [-e] [-p SHEETDELIMITER]
                   [--hyperlinks]
                   [-I INCLUDE_SHEET_PATTERN [INCLUDE_SHEET_PATTERN ...]]
                   [-E EXCLUDE_SHEET_PATTERN [EXCLUDE_SHEET_PATTERN ...]] [-m]
                   xlsxfile [outfile]
```
**positional arguments:**
```
  xlsxfile              xlsx file path, use '-' to read from STDIN
  outfile               output csv file path, or directory if -s 0 is specified
```


Usage with folder containing multiple `xlxs` files:
```
    python xlsx2csv.py /path/to/input/dir /path/to/output/dir
```
will output each file in the input dir converted to `.csv` in the output dir. If omitting the output dir it will output the converted files in the input dir

Usage from within Python:
```
  from xlsx2csv import Xlsx2csv
  Xlsx2csv("myfile.xlsx", outputencoding="utf-8").convert("myfile.csv")
