# MOSS Python Client

A simple Python script for submitting source files to the MOSS (Measure Of Software Similarity) server for plagiarism and similarity checking.

This client connects to the MOSS server, uploads one or more source files, and returns the result URL provided by the server.

## Features

* Supports multiple programming languages accepted by MOSS
* Uploads submission files and optional base files
* Checks that files exist, are readable, and appear to be text files
* Lets you configure match limits, result display size, comments, server, and port
* Supports directory mode and experimental mode flags

## Requirements

* Python 3
* Network access to `moss.stanford.edu`
* A valid MOSS user ID

## Setup

1. Save the script as `moss.py`
2. Open the file and replace:

```python
userid = "your_userid"
```

with your actual MOSS user ID.

## Usage

```bash
python moss.py [-x] [-l language] [-d] [-b basefile1] ... [-b basefilen] [-m #] [-c "string"] file1 file2 file3 ...
```

## Arguments

### Positional arguments

* `file1 file2 file3 ...`
  One or more files to submit to MOSS.

### Options

* `-l language`
  Sets the programming language for all submitted files.
  Default: `c`

* `-b basefile`
  Adds a base file. Base files are treated as common code and excluded from similarity comparisons.

* `-m #`
  Sets the maximum number of times a passage may appear before it is ignored.
  Default: `10`

* `-c "string"`
  Adds a comment string to the submission.

* `-n #`
  Sets the number of matching results to show.
  Default: `250`

* `-d`
  Enables directory mode.

* `-x`
  Enables experimental server mode.

* `-s server`
  Overrides the default server.
  Default: `moss.stanford.edu`

* `-p port`
  Overrides the default port.
  Default: `7690`

## Supported Languages

The script currently accepts the following language values:

* `c`
* `cc`
* `java`
* `ml`
* `pascal`
* `ada`
* `lisp`
* `scheme`
* `haskell`
* `fortran`
* `ascii`
* `vhdl`
* `perl`
* `matlab`
* `python`
* `mips`
* `prolog`
* `spice`
* `vb`
* `csharp`
* `modula2`
* `a8086`
* `javascript`
* `plsql`
* `verilog`

## Examples

### Submit Python files

```bash
python moss.py -l python student1.py student2.py student3.py
```

### Submit Java files with a base file

```bash
python moss.py -l java -b starter_code.java A.java B.java C.java
```

### Submit files with a comment and custom match limit

```bash
python moss.py -l c -m 20 -c "CS101 Assignment 3" main1.c main2.c
```

### Use a custom server and port

```bash
python moss.py -s moss.stanford.edu -p 7690 -l python app.py test.py
```

## How It Works

The script performs the following steps:

1. Parses command-line options
2. Verifies that all base files and input files exist and are readable
3. Connects to the MOSS server
4. Sends the MOSS protocol handshake
5. Uploads base files first
6. Uploads submission files
7. Sends the query request
8. Prints the server response, usually a results URL

## Output

A successful run typically looks like this:

```text
Checking files . . .
OK
Uploading file1.py ...done.
Uploading file2.py ...done.
Query submitted. Waiting for the server's response.

http://moss.stanford.edu/results/...
```

## Notes

* All files are uploaded using the same language specified by `-l`.
* Base files are uploaded with file ID `0`.
* Submission files are uploaded with incrementing file IDs starting from `1`.
* Filenames are sanitized by replacing spaces with underscores before upload.
* The script reads files as text, so binary files are not supported.

## Error Handling

The script exits with an error message if:

* No input files are provided
* A file does not exist
* A file is not readable
* A file cannot be read as text
* The server cannot be reached
* An invalid language is rejected by the server
* A file upload fails

## Limitations

* The script does not validate the language locally before contacting the server
* It assumes uploaded files can be read as UTF-8 compatible text
* It does not retry failed network connections
* It does not provide progress reporting beyond per-file upload messages

## License

This project is released under **The Unlicense**.

You are free to use, modify, publish, compile, sell, or distribute this software, in source code or binary form, for any purpose, commercial or non-commercial.

For more information, see the `LICENSE` file or visit [The Unlicense](https://unlicense.org) website.
