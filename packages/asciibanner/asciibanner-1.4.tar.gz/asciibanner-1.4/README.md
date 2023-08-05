# Asciibanner

<p align="center">
  Asciibanner a python script that allow you to do ASCII-Art with symbols
  <br>
  <img alt="PyPI" src="https://img.shields.io/pypi/v/asciibanner">
  <br>
</p>

## Features

 - [x] Ascii-Art with multiples build-in symbols 
   - [x] `#`
   - [x] `?`
   - [x] `/`
   - [x] `!`
 - [x] Ascii-Art with custom symbols
 - [ ] Ascii-Art of animals

## Installation

You can now install it from pypi (latest version is <img alt="PyPI" src="https://img.shields.io/pypi/v/asciibanner">) with this command:

```bash
python3 -m pip install asciibanner
pip3 install asciibanner
```

## Usage

```python
import asciibanner
print(asciibanner.art_slash("Exemple"))
print(asciibanner.art_sharp("Exemple"))
print(asciibanner.art_interogation("Exemple"))
print(asciibanner.art_custom("Exemple", "-"))
# or 
from asciibanner import *
print(art_slash("Exemple"))
print(art_sharp("Exemple"))
print(art_interogation("Exemple"))
print(art_custom("Exemple", "-"))
```

## Contributing

Pull requests are welcome. Feel free to open an issue if you want to add other features.