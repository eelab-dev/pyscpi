import numpy as np
import matplotlib.pyplot as plt

from pyscpi import scpi
from pyscpi.keysight import osc


inst = scpi.Instrument('192.168.178.50', 5025)

print(inst.query('*IDN?'))

t, y1 = osc.readSingleChannel(inst, 1)

plt.plot(t, y1)
plt.show()

inst.close()
