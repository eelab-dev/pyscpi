# pyscpi

[![PyPI version](https://badge.fury.io/py/pyscpi.svg)](https://badge.fury.io/py/pyscpi)

A Python library for communicating with SCPI devices and a helper library for communicating with the Keysight's [Smart Bench Essentials](https://www.keysight.com/us/en/cmp/2021/keysight-smart-bench-essentials-test-instruments.html) educational equipment. It can be used with Keysight's IOLibrary and driverless using TCP/IP socket communication.

## Using PyVisa

you need to install Keysight's IOLibrary and PyVisa.

## Using Socket (Driverless)

You don't need to install any drivers or libraries. You can use the standard TCP/IP sockets to communicate with the instrument. However, you need to connect the instrument to the same network as your computer either using a direct ethernet cable or a switch/router. Please notice if you are not using a router then you have may need to set the instrument's IP address manually or use a DHCP server for dynamic IP allocation. Further information can be found in the [here]().

## Getting Started

### Installing

You can install the library using pip:

```bash
python -m pip install pyscpi
```

### connecting to the instrument using PyVisa

```python
import pyvisa as visa

rm = visa.ResourceManager()
inst = rm.open_resource('<resource address>')

print(inst.query('*IDN?'))
```

### connecting to the instrument using socket (driverless)

```python
from pyscpi import scpi

inst = scpi.Instrument('<IP address>', 5025)

print(inst.query('*IDN?'))
```

### Reading oscilloscope waveform

```python
from pyscpi.keysight import osc
import numpy as np

t, y1 = osc.readSingleChannel(inst, 1)
```

### Plotting oscilloscope waveform

```python
# %matplotlib ipympl
import matplotlib.pyplot as plt

plt.plot(t, y1)
plt.show()
```

### closing the connection

```python
inst.close()
```


## Acknowledgments

Thanks to [Keysight Education](https://www.keysight.com/us/en/industries/education.html) for providing the Smart Bench Essentials educational equipment.
