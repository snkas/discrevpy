# discrevpy: minimalist discrete event simulator

[![build](https://github.com/snkas/discrevpy/workflows/build/badge.svg)](https://github.com/snkas/discrevpy/actions?query=workflow%3Abuild+branch%3Amaster)
[![codecov](https://codecov.io/gh/snkas/discrevpy/branch/master/graph/badge.svg)](https://codecov.io/gh/snkas/discrevpy) 
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**discrevpy** is a minimalist discrete event simulator in Python. It makes use of function/method
callbacks in its event execution. The discrevpy simulator does not implement any message passing
and is thus exclusively single-threaded.


## Installation

**Requirements**
* Python 3.7+
* (optional) pytest (`python3 -m pip install pytest`)
* (optional) coverage (`python3 -m pip install coverage`)
* (optional) pylint (`python3 -m pip install pylint`)
* (optional) sphinx (`python3 -m pip install sphinx`)

**Option 1**

```bash
python3 -m pip install git+https://github.com/snkas/discrevpy.git@v0.2.6
```

**Option 2**

Clone/download this Git repository. Then, execute the following to install the package locally:

```bash
cd /path/to/discrevpy
python3 -m pip install .
```


## Getting started

* **Example usage:**

  ```python
  from discrevpy import simulator
  
  def something(value):
      print("t=" + str(simulator.now()) + ": something() with value " + str(value))
    
  simulator.ready()
  simulator.schedule(44, something, "ABC")
  simulator.schedule(967, something, "XYZ")
  simulator.end(10000)
  simulator.run()
  simulator.reset()
  ```


## Development

Run tests:
```bash
python3 -m pytest
```

Calculate coverage (outputs `.coverage`, `coverage.xml` and `htmlcov/`):
```bash
python3 -m coverage run --branch --omit="tests/*" -m pytest
python3 -m coverage xml
python3 -m coverage html
```

Pylint check:
```bash
python3 -m pylint discrevpy/*.py
```

Generate documentation (index output at `docsrc/build/html/index.html`):
```bash
cd docsrc
make html
```
