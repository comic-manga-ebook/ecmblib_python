> [!WARNING]
> This project is still under developement, so please don't use it atm

 
### Homepage: [https://comic-manga-ebook.github.io](https://comic-manga-ebook.github.io)

## About this repository:

This is the python-library you can use for your project to build `*`.ecmb - files without caring about the internals of the file-format.
You can't do anything wrong with this, coz if you do a mistake (eg. passing a boolean to set_summary()) an ecmbException will be raised. After the creation the file will be automatic validated. 

Published under [MIT License](https://choosealicense.com/licenses/mit/)

**Copyright:**

Copyright (c) 2023 Clemens K. (https://github.com/metacreature)

**If you like it I would be happy if you  [donate on checkya](https://checkya.com/1hhp2cpit9eha/payme)**

# Using the library

### Installation
- download and install Python3 (>=3.11) [https://www.python.org/downloads/](https://www.python.org/downloads/)
- open the console and then
    - run `pip install ecmblib`
 
### Trying out examples
- download and install Python3 (>=3.11) [https://www.python.org/downloads/](https://www.python.org/downloads/)
- download and install Git [https://git-scm.com/downloads](https://git-scm.com/downloads)´
- open the git-console and then
    - clone this repositiory `git clone git@github.com:metacreature/ecmblib_python.git`
    - go to the project-folder `cd ecmblib_python/`
    - run `pip install -r requirements.txt`
    - go to the example-folder `cd examples/advanced_book/`
    - run `python advanced_book.py`
The examples are working even if you didn't install the library via pip, but coz of the relative import type-hinting is not working.
If you want to use type-hinting you have to install the library first and then change the import of ecmblib at the top of the examples.

### Documentation:
[https://comic-manga-ebook.github.io/ecmblib](https://comic-manga-ebook.github.io/ecmblib)
