from .. import scpi
import sys
import numpy as np


def _read_fixed_bytes(inst, size):
    data = inst.read_bytes()
    while len(data) < size:
        data += inst.read_bytes()

    return data


def readChannel(inst: scpi.Instrument, channel: int, points: int = 0, runAfter: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Reads a channel from the oscilloscope.

    :param inst: The instrument object
    :param channel: The channel to read
    :param points: The number of points to read. If 0, read all points
    :param runAfter: Run the oscilloscope after reading
    :return: A tuple of time and voltage arrays

    """

    inst.write(':TIMebase:MODE MAIN')

    inst.write(f':DIGitize CHANnel{channel}')
    inst.write(':WAVeform:FORMat BYTE')
    inst.write(':WAVeform:POINts:MODE MAXimum')

    if points > 0:
        inst.write(f':WAVeform:POINts {points}')
    else:
        inst.write(':WAVeform:POINts MAXimum')

    inst.query('*OPC?')

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
    data = _read_fixed_bytes(inst, int(points))

    header = data[2:10].decode('utf-8')
    print(header)
    rpoints = int(header)

    if rpoints != (points):
        print('ERROR: points mismatch')

    data = data[10:-1]

    data = np.frombuffer(data, dtype=np.uint8)

    voltCH = (data-yref) * yinc + yorg

    time = (np.arange(0, points, 1)-xref) * xinc + xorg

    if runAfter:
        inst.write(':RUN')

    return time, voltCH


def autoScale(inst, channel):
    inst.write(f':CHANnel{channel}:SCAle:AUTO')


def setTimeAxis(inst, scale, offset):
    inst.write(f':TIMebase:SCALe {scale}')
    inst.write(f':TIMebase:OFFSet {offset}')
    inst.query('*OPC?')


def setChannelAxis(inst, channel, scale, offset):
    inst.write(f':CHANnel{channel}:SCALe {scale}')
    inst.write(f':CHANnel{channel}:OFFSet {offset}')
    inst.query('*OPC?')


def setWGenOutput(inst, state):
    inst.write(f':WGEN:OUTPut {state}')
    inst.query('*OPC?')


def setWGenSin(inst, amp, offset, freq):
    inst.write('WGEN:FUNCtion SINusoid')
    inst.write(f':WGEN:VOLTage {amp}')
    inst.write(f':WGEN:VOLTage:OFFSe {offset}')
    inst.write(f':WGEN:FREQuency {freq}')
    inst.query('*OPC?')
