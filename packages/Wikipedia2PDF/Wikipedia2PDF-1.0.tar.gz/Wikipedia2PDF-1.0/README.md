# Wikipedia2PDF
Convert any Wikipedia article into PDF.

## Getting Started
### Prerequisites
- Python 3.6+

## Installation
- First, please make sure that the latest `pip` version is installed in your working environment.
```
python -m pip install --upgrade pip
```

- Then you can install Wikipedia2PDF using a simple `pip install` command.
```
python -m pip install --upgrade Wikipedia2PDF
```

## Example

```py
from Wikipedia2PDF import Wikipedia2PDF

# without specifying a filename 
Wikipedia2PDF("https://en.wikipedia.org/wiki/Microsoft_Windows")
# output: Microsoft Windows.pdf

# with specifying a filename 
Wikipedia2PDF("https://en.wikipedia.org/wiki/Apple", filename="Apple.pdf")
# output: Apple.pdf
```

## License
This Python package is distributed under the [MIT License](https://mit-license.org/).
