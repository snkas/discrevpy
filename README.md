# discrevpy: minimalist discrete event simulator

[![build](https://github.com/snkas/discrevpy/workflows/build/badge.svg)](https://github.com/snkas/discrevpy/actions?query=workflow%3Abuild+branch%3Amaster)
[![codecov](https://codecov.io/gh/snkas/discrevpy/branch/master/graph/badge.svg)](https://codecov.io/gh/snkas/discrevpy) 
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/snkas/discrevpy/blob/master/LICENSE)
[![GitHub release version](https://img.shields.io/github/v/release/snkas/discrevpy)](https://github.com/snkas/discrevpy/releases)
[![PyPI version](https://img.shields.io/pypi/v/discrevpy?color=blue)](https://pypi.org/project/discrevpy/)

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

* [View some short examples](https://snkas.github.io/discrevpy/short_examples.html)
* [View more in-depth longer examples](https://snkas.github.io/discrevpy/long_examples.html)
* [Explore the API](https://snkas.github.io/discrevpy/api_reference.html)
* [Learn more about discrete event simulation](https://snkas.github.io/discrevpy/what_is_discrete_event_simulation.html)
* [Read some tips to help you speed up your simulations](https://snkas.github.io/discrevpy/practical_tips.html)
* [Understand better the memory usage overhead of discrevpy](https://snkas.github.io/discrevpy/memory_usage.html)

**Development:**

* [Read the module development instructions](https://snkas.github.io/discrevpy/development.html)
* [Browse the GitHub repository](https://github.com/snkas/discrevpy)
* [View the MIT license](https://github.com/snkas/discrevpy/blob/master/LICENSE)
