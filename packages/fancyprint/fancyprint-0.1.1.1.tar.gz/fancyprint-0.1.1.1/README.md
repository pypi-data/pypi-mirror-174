<h1 align="center">Fancy Print</h1>
<h3 align="center">An aesthetic replacement to print()</h3>

<hr>

<h6 align="center"><b>Development Status:</b> Early Development/Usable</h6>
<p align="center">
  <a href="https://pypi.org/project/fancyprint/">
	<img src="https://img.shields.io/pypi/v/fancyprint?color=blue&label=PyPI&logo=python&logoColor=white&style=for-the-badge" alt="PyPI">
  </a>
</p>

# About

FancyPrint is a python package, making it easier for developers to get beautiful CLI with responsiveness in regards to terminal size.

# Usage

## Installing FancyPrint

To install fancyprint use the following command:
```bash
pip install fancyprint
```
This will install all dependencies needed as well.

## Getting Started

To start using Fancy Print, first import it.
```python
import fancyprint
```
This will import all the necessary functions required.

### Basics

#### Printing

The ``pretty_print()`` function is for printing text to the terminal. There are two ways one can use it, and they can be
used interchangeably:
- Using presets (recommended)
- Using keyword arguments

##### Using Presets
Presets allow you to customize the printer and the separator, and they can be *local* presets or *global* presets.
Presets are local when they are created for one part only(i.e Printer) and are global when they can be used anywhere
(both in the Separator and the Printer). 

###### Using Local Presets
There are two types of local presets you can use:
- PrinterPreset
- SeparatorPreset

**PrinterPreset**
<br>
<br>
The ``PrinterPreset`` is used to customize the ``pretty_print()`` function. To use it, you need to import it first.
Here is an example of declaring a ``PrinterPreset``:
```python
from src.fancyprint.ftypes import PrinterPreset
from src.fancyprint.ftypes import Color

my_custom_printer_preset = PrinterPreset(
    delimiter_left="<",
    delimiter_left_color=Color.RED,
    
    delimiter_right=">",
    delimiter_right_color=Color.RED,
    
    delimiter_space_amount=10,
    delimiter_space_symbol=" ",
    
    hyphenation=False
)
```
Here's the preset in action:
```python
[...]
pretty_print("Hi, this is some text", )
```