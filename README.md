# PYJP - A tool for JProfiler analyze
## Introduction
`pyjp` is a tool that analyzes JProfiler HTML reports. It generates additional 
information, including:
- **level**: the level of each method in the invocation chain
- **invocation time**: the total time spent in any direct children methods

The level of a method indicates its depth in the call stack, with higher-level methods having lower levels. 
By providing this information, `pyjp` allows users to better understand the performance of 
various methods in their application and identify performance bottlenecks and optimization opportunities.

For example, suppose the invocation chain listed below:


| Seq | Level | total_time | formular of invocation_time       | invocation time | time(elapsed by method itself) 
|:-:|:-----:|-----------:|-----------------------------------|----------------:|-------------------------------:|
| 1   |   3   |     30,000 | seq1.total_time                   |          30,000 |                              0 |
| 2   |   1   |    300,000 | seq3.total_time                   |         200,000 |                         10,000 |
|3|3|200,000| seq4.total_time + seq6.total_time |         150,000 |                         50,000 |
|4|4|30,000| seq5.total_time                   |          20,000 |                         10,000 |
|5|5|20,000| seq5.total_time                   |20,000|0|
|6|4|120,000| seq7.total_time                   |70,000|50,000|
|7|7|70,000| seq8.total_time                   |60,000|10,000|
|8|8|10,000| seq8.total_time                   |10,000|0|

The invocation time for a method is calculated by adding up the total time spent in each direct 
child method. Once we have the invocation time, we can calculate the running time of the method itself. In this way, we can better understand the performance of a given method and its overall impact on the application.
## How to use
1. Install by `pip` or download it from GitHub and manually install:
```commandline
pip install pyjp
```
or download from https://github.com/sharework-cn/pyjp/releases, and then use `pip` to install

2. Run `pyjp --help` for the instruction:
```commandline
pyjp --help
Usage: pyjp [OPTIONS] SOURCE

  A tool to parse the exported HTML JProfile report, it adds level and
  invocation time of children methods, which is useful to get the elapsed time
  by the calling method itself.

Options:
  -d, --destination TEXT    The output file name, default to the source_file.csv
                            with the same folder
  -p, --pattern TEXT        The regex pattern to extract information from the
                            line text, supported named variables are: time,
                            percentage, average_time, events, method
  --decode TEXT             Decode used to read the file  [default: utf-8]
  --overwrite               Overwrite an exist file, default is False
  --interval INTEGER RANGE  The interval to print in progress message
                            [2<=x<=50000]
  --help                    Show this message and exit.
```