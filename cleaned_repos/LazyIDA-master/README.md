# LazyIDA
Make your IDA Lazy!

# Install
1. put `LazyIDA.py` into `plugins` folder under your IDA Pro installation path.

# Features
  - Remove function return type in Hex-Rays
  - Convert data into different formats, output will also be automatically copied to the clipboard
  - Scan for format string vulnerabilities
  - Jump to vtable functions by double clicking
  - Lazy shortcuts:
    - Disasm Window: 
      - `w`: Copy address of current line into clipboard
    - Hex-rays Window: 
      - `w`: Copy address of current item into clipboard
      - `c`: Copy name of current item into clipboard
      - `v`: Remove return type of current item