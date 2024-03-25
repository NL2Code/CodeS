# online-judge-tools/oj

`oj` is a command to help solving problems on various online judges. This command automates downloading sample cases, generating additional test cases, testing for your code, and submitting it.

## Features

-   Download sample cases
-   Download system test cases
-   Login
-   Submit your code
-   Test your code
-   Test your code for reactive problems
-   Generate input files from generators
-   Generate output files from input and reference implementation

For the detailed documentation, read [docs/getting-started.md](https://github.com/online-judge-tools/oj/blob/master/docs/getting-started.md).

Many online judges (Codeforces, AtCoder, HackerRank, etc.) are supported.

## How to use

```console
$ oj download [--system] URL
$ oj login URL
$ oj submit [URL] FILE
$ oj test [-c COMMAND] [TEST...]
$ oj test-reactive [-c COMMAND] JUDGE_COMMAND
$ oj generate-input GENERATOR_COMMAND
$ oj generate-output [-c COMMAND] [TEST...]
```

For details, see `$ oj --help`.
