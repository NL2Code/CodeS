# heartrate

This library offers a simple real time visualisation of the execution of a Python program:

The numbers on the left are how many times each line has been hit. The bars show the lines that have been hit recently - longer bars mean more hits, lighter colours mean more recent.

Calls that are currently being executed are highlighted thanks to the `executing` library.

## Usage

```python
import heartrate; heartrate.trace(browser=True)
```

This will:

 - Start tracing your program
 - Start a server in a thread
 - Open a browser window displaying the visualisation of the file where `trace()` was called.

In the file view, the stacktrace is at the bottom. In the stacktrace, you can click on stack entries for files that are being traced to open the visualisation for that file at that line.

`trace` only traces the thread where it is called. To trace multiple threads, you must call it in each thread, with a different port each time.