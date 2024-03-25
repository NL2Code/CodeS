# Flameshow

Flameshow is a terminal Flamegraph viewer.

## Features

- Renders Flamegraphs in your terminal
- Supports zooming in and displaying percentages
- Keyboard input is prioritized
- All operations can also be performed using the mouse.
- Can switch to different sample types

## Usage

View golang's goroutine dump:

```shell
$ curl http://localhost:9100/debug/pprof/goroutine -o goroutine.out
$ flameshow goroutine.out
```

After entering the TUI, the available actions are listed on Footer:

- <kbd>q</kbd> for quit
- <kbd>j</kbd> <kbd>i</kbd> <kbd>j</kbd> <kbd>k</kbd> or <kbd>←</kbd>
  <kbd>↓</kbd> <kbd>↑</kbd> <kbd>→</kbd> for moving around, and <kbd>Enter</kbd>
  for zoom in, then <kbd>Esc</kbd> for zoom out.
- You can also use a mouse, hover on a span will show it details, and click will
  zoom it.

## Supported Formats

As far as I know, there is no standard specification for profiles. Different
languages or tools might generate varying profile formats. I'm actively working
on supporting more formats. Admittedly, I might not be familiar with every tool
and its specific format. So, if you'd like Flameshow to integrate with a tool
you love, please feel free to reach out and submit an issue.

- Golang pprof
- [Brendan Gregg's Flamegraph](https://www.brendangregg.com/flamegraphs.html)