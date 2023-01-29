# pyscpi

[![PyPI version](https://badge.fury.io/py/pyscpi.svg)](https://badge.fury.io/py/pyscpi)

A Python library for communicating with SCPI devices and a helper library for communicating with the Keysight's [Smart Bench Essentials](https://www.keysight.com/us/en/cmp/2021/keysight-smart-bench-essentials-test-instruments.html) educational equipment. The library communicates using multiple backends including PyVisa, USBTMC and socket communication. The library also provides helper functions for reading oscilloscope waveforms and plotting them.

## Using PyVisa and Keysight's IOLibrary

you need to install Keysight's IOLibrary and PyVisa.

## Using alternative methods including usb and ethernet

You can use USBTMC, a standard for communicating with instruments using USB using generic drivers. This method works both in Windows and WSL2. Alternatively, you can use the standard TCP/IP sockets to communicate with the instrument. However, you need to connect the instrument on the same network as your computer, either using a direct ethernet cable or a switch/router. If you are not using a router, then you may need to set the instrument's IP address manually or use a DHCP server for dynamic IP allocation. Further information can be found in the [here](https://danchitnis.github.io/pyscpi/connections/).

## Getting Started

### Installing

You can install the library using pip:

```bash
python -m pip install --upgrade pyscpi
```

### connecting to the instrument using PyVisa

```python
import pyvisa as visa

rm = visa.ResourceManager()
inst = rm.open_resource('<resource address>')

print(inst.query('*IDN?'))
```

### connecting to the instrument using USBTMC

```python
from pyscpi import usbtmc

inst =  usbtmc.Instrument(<VendorID>, <ProductID>)

print(inst.query("*IDN?"))
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

[USBTMC](https://github.com/python-ivi/python-usbtmc) is used for communicating with the instruments using USB.