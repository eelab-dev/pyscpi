from .. import scpi
import sys
import numpy as np


def read_fixed_bytes(inst, size):
    data = inst.read_bytes()
    while len(data) < size:
        data += inst.read_bytes()

    return data


# Read a channel from the oscilloscope
# @param inst The instrument to read from
# @param channel The channel to read
# @param points The number of points to read
# @param runAfter Run the oscilloscope after reading
# @return xdata, ydata

def readChannel(inst, channel, points=0, runAfter=True):
    inst.write(':STOP')

    inst.write(':WAVeform:FORMat BYTE')
    inst.write(f':WAVeform:SOURce CHANnel{channel}')
    inst.write(':TIMebase:MODE MAIN')
    inst.write(':WAVeform:POINts:MODE MAXimum')

    inst.query('*OPC?')

    if points > 0:
        inst.write(f':WAVeform:POINts {points}')
    else:
        inst.write(':WAVeform:POINts MAXimum')

    #points = int(inst.query(':WAVeform:POINts?'))

    peram = inst.query(':WAVeform:PREamble?')
    peram = peram.split(',')
    print(peram)

    format = peram[0]
    type = peram[1]
    points = int(peram[2])
    xinc = float(peram[4])
    xorg = float(peram[5])
    xref = float(peram[6])
    yinc = float(peram[7])
    yorg = float(peram[8])
    yref = float(peram[9])

    inst.write(':WAVeform:DATA?')
    data = read_fixed_bytes(inst, int(points))

    header = data[2:10].decode('utf-8')
    print(header)
    rpoints = int(header)

    if rpoints != (points):
        print('ERROR: points mismatch')

    data = data[10:-1]

    data = np.frombuffer(data, dtype=np.uint8)

    ydata = (data-yref) * yinc + yorg

    xdata = (np.arange(0, points, 1)-xref) * xinc + xorg

    if runAfter:
        inst.write(':RUN')

    return xdata, ydata
