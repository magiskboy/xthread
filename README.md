<p align="center">
  <img width="420px" src="https://i.ibb.co/0BPYdRk/xthread.png" alt='xthread'>
</p>
<p align="center">
    <em>Threading for human.</em>
</p>
<p align="center">
    <a href="https://github.com/magiskboy/xthread/actions">
        <img src="https://github.com/magiskboy/xthread/actions/workflows/test-suite.yml/badge.svg" alt="Build Status">
    </a>
    <a href="https://app.codecov.io/gh/magiskboy/xthread">
        <img src="https://img.shields.io/codecov/c/github/magiskboy/xthread" alt="Code coverage">
    </a>
    <a href="https://pypi.org/project/xthread/">
        <img src="https://img.shields.io/pypi/dd/xthread" alt="Download PyPi">
    </a>
    <a href="https://github.com/magiskboy/xthread/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/magiskboy/xthread" alt="MIT">
    </a>
    <a href="https://pypi.org/project/xthread/">
        <img src="https://img.shields.io/pypi/pyversions/xthread" alt="Py version">
    </a>
    <a href="https://pypi.org/project/xthread/">
        <img src="https://img.shields.io/pypi/v/xthread" alt="PyPi version">
    </a>
</p>


## Features

Some of main features:

- Support pause/unpause
- Support termination thread non-preemtively

## Installation

You can install xthread from PyPi

```bash
$ pip install xthread
```

## Usage

```python
import time
from xthread import Thread

def target(executor):
    print("Running...")
    time.sleep(1)

thread = Thread(target)

# Running...
# Running...

thread.pause()

thread.unpause()

# Running...
# Running...

thread.stop()
```
