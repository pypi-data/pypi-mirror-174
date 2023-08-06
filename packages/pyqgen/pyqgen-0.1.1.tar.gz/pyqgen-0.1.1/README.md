# PyQGen

- Author: Giuseppe Lipari
- Email : giuseppe.lipari@univ-lille.fr

PyQGen is a command line script to generate a randomized list of
questions taken from a orgmode file. It can be used to prepare exams
for large classes. 

What you need in addition to PyQGen : 
- Emacs with org-mode;
- A LaTeX environment.

## Overview 

The original list of questions must be redacted according to the
[org-mode](https://orgmode.org/) format. The first level heading in
this file represent *groups of questions*; the second level headings
represent the questions ; deeper level headings represent solutions. 

An example of database of questions is available HERE.

PyQGen produces an org-mode file which contains the exams. This can
later be transformed into a PDF file via LaTeX.

## Installing 

I recommend installing PyQGen using a virtual environnement and pip. 
For example : 
```sh
virtualenv pyqgenenv
source ./pyqgenenv/bin/activate
pip install pyqgen
```

PyQGen depends on
[orgparse](https://orgparse.readthedocs.io/en/latest/) to parse the
org-mode file, pip automatically takes care of the dependency.

## Command line options 

The command is : 
```sh
pyqgen [OPTIONS] output
```

where `output` the generated file that contains the exams. The
following options are possible :

- `-h`, `--help`  shows the help message
- `-d DB`, `--db DB` specifies an input file. By default, this is
  equal to file `db.org`.
- `-t TITLE`, `--title TITLE` Specifies the title of each exam sheet
  (default: "Examen")
- `-i IFILE`, `--ifile IFILE` Text file containing the instructions to be 
  printed on each exam (default: none)
- `-n NCOPIES`, `--ncopies NCOPIES` Number of exams to generate (default: 1)
- `-g [NG ...]`, `--ng [NG ...]` Number of questions per group
  (default: [1, 1, 1]). Therefore, the default assumes that the input
  file defines 3 question groupes, and for each exam it will randomly
  select one question per group.  Make sure that you specify at least
  one number per each group (see example below).
- `-e HEADER`, `--header HEADER` Org-mode file header. This is used to
  personnalize the output style. Typically, you can specify the size
  of the sheet (using the latex package geometry), the font, the font
  size, etc.

## Full example 

TODO 

