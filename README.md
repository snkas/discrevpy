# discrevpy: minimalist discrete event simulator

[![build](https://github.com/snkas/discrevpy/workflows/build/badge.svg)](https://github.com/snkas/discrevpy/actions?query=workflow%3Abuild+branch%3Amaster)
[![codecov](https://codecov.io/gh/snkas/discrevpy/branch/master/graph/badge.svg)](https://codecov.io/gh/snkas/discrevpy) 
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**discrevpy** is a minimalist discrete event simulator in Python. It makes use of function/method
callbacks in its event execution. The discrevpy simulator does not implement any message passing
and is thus exclusively single-threaded.


## Installation

**Python version: 3.7+**

```bash
python3 -m pip install discrevpy
```


## Getting started

**Example usage:**

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

**Documentation:**

https://snkas.github.io/discrevpy/

**Next steps:**

* [View more examples](https://snkas.github.io/discrevpy/examples.html)
* [Explore the API](https://snkas.github.io/discrevpy/api_reference.html)
* [Learn more about discrete event simulation](https://snkas.github.io/discrevpy/what_is_discrete_event_simulation.html)
* [Read some tips to help you speed up your simulations](https://snkas.github.io/discrevpy/practical_tips.html)
* [Understand better the memory usage overhead of discrevpy](https://snkas.github.io/discrevpy/memory_usage.html)


## Development

**Requirements:**
* pytest (`python3 -m pip install pytest`)
* coverage (`python3 -m pip install coverage`)
* pylint (`python3 -m pip install pylint`)
* sphinx (`python3 -m pip install sphinx`)
* furo (`python3 -m pip install furo`)

**Install latest development version:**
1. Clone the GitHub repository:
   ```bash
   git clone git@github.com:snkas/discrevpy.git
   ```
2. Install locally using `pip`:
   ```bash
   cd discrevpy
   python3 -m pip install .
   ```

**Run tests:**
```bash
python3 -m pytest
```

**Calculate coverage (outputs `.coverage`, `coverage.xml` and `htmlcov/`):**
```bash
python3 -m coverage run --branch --omit="tests/*" -m pytest
python3 -m coverage xml
python3 -m coverage html
```

**Pylint check:**
```bash
python3 -m pylint discrevpy/*.py
```

**Generate documentation (outputs HTML at `docs/`):**
```bash
cd docsrc
make html
```
