# Print Loader

[![PyPI - Version](https://img.shields.io/pypi/v/print-loader.svg)](https://pypi.org/project/print-loader)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/print-loader.svg)](https://pypi.org/project/print-loader)

-----

**Table of Contents**

- [Installation](#installation)
- [Introduction](#introduction)
- [License](#license)

## Installation

```console
pip install print-loader
```

## Introduction
Sometimes you want to put an indefinite loader for a set of statements to see
the progress in terminal. This package tries to solve that exact problem.

## Examples

```python
from print_loader import printl
import time

with printl("Sleeping"):
    time.sleep(3)

with printl("Sleeping", update_every=0.1):
    time.sleep(3)

with printl("Sleeping", update_every=0.1, loading_chars=["-", "|"]):
    time.sleep(3)

with open("large_file.txt", "w") as fp, printl("Writing to file"):
    for i in range(50000):
        fp.write(str(i) * 30000 + "\n")
```

## License

`print-loader` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
