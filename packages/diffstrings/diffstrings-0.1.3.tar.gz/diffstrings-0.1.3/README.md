# diffstrings

[![Test](https://github.com/Uguudei/diffstrings/actions/workflows/test.yml/badge.svg)](https://github.com/Uguudei/diffstrings/actions/workflows/test.yml)
[![Publish to PyPI](https://github.com/Uguudei/diffstrings/actions/workflows/publish.yml/badge.svg)](https://github.com/Uguudei/diffstrings/actions/workflows/publish.yml)
[![Publish to TestPyPI](https://github.com/Uguudei/diffstrings/actions/workflows/publish-testpypi.yml/badge.svg)](https://github.com/Uguudei/diffstrings/actions/workflows/publish-testpypi.yml)
[![PyPi Version](https://img.shields.io/pypi/v/diffstrings?color=blue)](https://pypi.org/project/diffstrings/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/diffstrings)](https://pypi.org/project/diffstrings/)
[![License](https://img.shields.io/github/license/Uguudei/diffstrings)](https://github.com/Uguudei/diffstrings/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Show difference of strings in color. It works on both terminal and ipython.

It extends difflib.SequenceMatcher class and provides a direct function too.

## Installation

```python
pip install diffstrings
```

## API

### Example Result

![Colored diff strings](https://user-images.githubusercontent.com/1560166/199187551-fa54c4cc-11eb-40bc-8c09-f227979dd4e2.png)

Color explanation:

- Green: to add
- Yellow: to replace. (Remove yellow colored then add with green colored strings)
- Red: to be removed

### Example texts

```bash
# Truth text to compare with
truth = """Lorem ipsum dolor sit amet,consectetur adipiscing elit,  sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.f"""

# Supposedly wrong text to compare
predict = """Lorem furio dlfgor sit amet, consectetur apiscbgfing elit, sed do eiusmod tempor inciddfbunt ut labore et ddslore magna aliqua. Ut enim ad minim veniam, quis nostrud exercsfsation ullamco laboris assi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in volbcvbte velit esse cilldm doldsre eu fugiat nulla pafdgatur. Excepteur sint occaecat cupidatat non pident, sunt in culpa qui asafficia desert mollit anim id est lfdgarum."""
```

### Using class

```bash
from diffstrings import SequenceMatcher

s = SequenceMatcher(None, predict, truth, autojunk=False)
print(s.diff_strings())
print(s.diff_strings(True))
```

### Using function

```bash
from diffstrings import diff_strings

print(diff_strings(predict, truth))
print(diff_strings(predict, truth, show_change_on_seq2=True))
```
