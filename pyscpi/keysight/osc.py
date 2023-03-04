import numpy as np
from dataclasses import dataclass


@dataclass
class Preamble:
    """A class to store the preamble data from the oscilloscope channel.

    :param format: The format of the data
    :param type: The type of the data
    :param points: The number of points
    :param xinc: The x increment
    :param xorg: The x origin
    :param xref: The x reference
    :param yinc: The y increment
    :param yorg: The y origin
    :param yref: The y reference
    """

    format: str
    type: str
    points: int
    xinc: float
    xorg: float
    xref: float
    yinc: float
    yorg: float
    yref: float


def getPreamble(inst, debug: bool = False) -> Preamble:
    """Reads the preamble from the oscilloscope.

    :param inst: The instrument object from pyscpi or pyvisa
    :param debug: Print debug messages
    :return: A Preamble object

    """

    peram = inst.query(':WAVeform:PREamble?')
    peram = peram.split(',')
    _log(peram, debug)

    pre = Preamble(peram[0], peram[1], int(peram[2]), float(peram[4]), float(
        peram[5]), float(peram[6]), float(peram[7]), float(peram[8]), float(peram[9]))

    return pre


def _read_large_raw_bytes(inst, debug) -> bytes:
    chunk_size = 1024
    data = inst.read_raw(chunk_size)
    header = data[2:10].decode('utf-8')
    _log(header, debug)

    hpoints = int(header)

    while len(data) - len(header) < hpoints:
        data += inst.read_raw(chunk_size)

    return data


def _read_large_data_bytes_np(inst, debug) -> bytes:
    chunk_size = 1024
    data = inst.read_raw(chunk_size)
    np.frombuffer(data[10:], dtype=np.uint8)
    header = data[2:10].decode('utf-8')
    data = np.frombuffer(data[10:], dtype=np.uint8)
    _log(header, debug)

    hpoints = int(header)

    while len(data) < hpoints:
        data = np.append(data, np.frombuffer(
            inst.read_raw(chunk_size), dtype=np.uint8))

    return data[:-1]


def _readWaveDate(inst, channel: int, points: int, debug: bool = False) -> np.ndarray:

    inst.query('*OPC?')
    inst.write(f':WAVeform:SOURce CHANnel{channel}')
    inst.query('*OPC?')
    _log('Reading channel ' + str(channel), debug)

    inst.write(':WAVeform:FORMat BYTE')
    inst.write(':WAVeform:POINts:MODE MAXimum')

    _log('Reading points', debug)

    if points > 0:
        inst.write(f':WAVeform:POINts {points}')
    else:
        inst.write(':WAVeform:POINts MAXimum')

    inst.query('*OPC?')

    _log('Reading data', debug)

    inst.write(':WAVeform:DATA?')
    data = _read_large_data_bytes_np(inst, debug)

    return data


def readChannels(inst, channels: list[int], points: int = 0, runAfter: bool = True, debug: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Reads multiple channels from the oscilloscope.

    :param inst: The instrument object from pyscpi or pyvisa
    :param channels: A list of channels to read eg. [1, 2]
    :param points: The number of points to read. If 0, read all points
    :param runAfter: Run the oscilloscope after reading
    :param debug: Print debug messages
    :return: A NumPy tuple of time and voltage arrays

    """

    inst.write(':TIMebase:MODE MAIN')

    channelCommand = ''
    for channel in channels:
        channelCommand = channelCommand + f'CHANnel{channel}, '

    channelCommand = channelCommand[:-2]

    _log(channelCommand, debug)

    inst.write(f':DIGitize {channelCommand}')

    inst.write(f':WAVeform:SOURce CHANnel{channels[0]}')

    pream = getPreamble(inst, debug)

    allData = np.empty([pream.points, len(channels)])

    for i in range(len(channels)):
        _log(f'Reading channel {channels[i]}', debug)
        data = _readWaveDate(inst, channels[i], points)
        if len(data) != (pream.points):
            print('ERROR: points mismatch, please investigate')
        allData[:, i] = data

    voltCH = (allData-pream.yref) * pream.yinc + pream.yorg

    time = (np.arange(0, pream.points, 1)-pream.xref) * pream.xinc + pream.xorg

    if runAfter:
        inst.write(':RUN')

    return time, voltCH


def readSingleChannel(inst, channel: int, points: int = 0, runAfter: bool = True, debug: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Reads a single channel from the oscilloscope.

    :param inst: The instrument object from pyscpi or pyvisa
    :param channel: The channel to read
    :param points: The number of points to read. If 0, read all points
    :param runAfter: Run the oscilloscope after reading
    :param debug: Print debug messages
    :return: A NumPy tuple of time and voltage arrays

    """

    inst.write(':TIMebase:MODE MAIN')

    inst.write(f':DIGitize CHANnel{channel}')
    inst.write(f':WAVeform:SOURce CHANnel{channel}')
    inst.write(':WAVeform:FORMat BYTE')
    inst.write(':WAVeform:POINts:MODE MAXimum')

    if points > 0:
        inst.write(f':WAVeform:POINts {points}')
    else:
        inst.write(':WAVeform:POINts MAXimum')

    inst.query('*OPC?')

    pream = getPreamble(inst, debug)

    _log('Reading data', debug)

    inst.write(':WAVeform:DATA?')

    data = _read_large_data_bytes_np(inst, debug)

    if len(data) != (pream.points):
        print('ERROR: points mismatch, please investigate')

    voltCH = (data-pream.yref) * pream.yinc + pream.yorg

    time = (np.arange(0, pream.points, 1)-pream.xref) * pream.xinc + pream.xorg

    if runAfter:
        inst.write(':RUN')

    return time, voltCH


def autoScale(inst) -> None:
    """Autoscales the oscilloscope.

    :param inst: The instrument object from pyscpi or pyvisa
    """

    inst.write(f':AUToscale')
    inst.query('*OPC?')


def setTimeAxis(inst, scale: float, position: float) -> None:
    """Sets the time axis of the oscilloscope.

    :param inst: The instrument object from pyscpi or pyvisa
    :param scale: The scale of the time axis in seconds
    :param position: The position of the time axis from the trigger in seconds
    """

    inst.write(f':TIMebase:SCALe {scale}')
    inst.write(f':TIMebase:POSition {position}')
    inst.query('*OPC?')


def setChannelAxis(inst, channel: int, scale: float, offset: float) -> None:
    """Sets the channel axis (y-axis) of the oscilloscope.

    :param inst: The instrument object from pyscpi or pyvisa
    :param channel: The channel to set
    :param scale: The scale of the channel axis in volts
    :param offset: The offset of the channel axis in volts
    """
    inst.write(f':CHANnel{channel}:SCALe {scale}')
    inst.write(f':CHANnel{channel}:OFFSet {offset}')
    inst.query('*OPC?')


def setWGenOutput(inst, state: int | str) -> None:
    """Sets the output state of the waveform generator. (Only available on specific models)

    :param inst: The instrument object from pyscpi or pyvisa
    :param state: The state to set the output to (0 or 1) or ('OFF' or 'ON')
    """

    inst.write(f':WGEN:OUTPut {state}')
    inst.query('*OPC?')


def setWGenSin(inst, amp: float, offset: float, freq: float) -> None:
    """Sets the waveform generator to a sine wave. (Only available on specific models)

    :param inst: The instrument object from pyscpi or pyvisa
    :param amp: The amplitude of the sine wave in volts
    :param offset: The offset of the sine wave in volts
    :param freq: The frequency of the sine wave in Hz. The frequency can be adjusted from 100 mHz to 20 MHz.
    """

    inst.write('WGEN:FUNCtion SINusoid')
    inst.write(f':WGEN:VOLTage {amp}')
    inst.write(f':WGEN:VOLTage:OFFSet {offset}')
    inst.write(f':WGEN:FREQuency {freq}')
    inst.query('*OPC?')


def setWGenSquare(inst, v0: float, v1: float, freq: float, dutyCycle: int) -> None:
    """Sets the waveform generator to a square wave. (Only available on specific models)

    :param inst: The instrument object from pyscpi or pyvisa
    :param v0: The voltage of the low state in volts
    :param v1: The voltage of the high state in volts
    :param freq: The frequency of the square wave in Hz. The frequency can be adjusted from 100 mHz to 10 MHz.
    :param dutyCycle: The duty cycle can be adjusted from 1% to 99% up to 500 kHz. At higher frequencies, the adjustment range narrows so as not to allow pulse widths less than 20 ns.
    """

    inst.write('WGEN:FUNCtion SQUare')
    inst.write(f':WGEN:VOLTage:LOW {v0}')
    inst.write(f':WGEN:VOLTage:HIGH {v1}')
    inst.write(f':WGEN:FREQuency {freq}')
    inst.write(f':WGEN:FUNCtion:SQUare:DCYCle {dutyCycle}')
    inst.query('*OPC?')


def setWGenRamp(inst, v0: float, v1: float, freq: float, symmetry: int) -> None:
    """Sets the waveform generator to a ramp wave. (Only available on specific models)

    :param inst: The instrument object from pyscpi or pyvisa
    :param v0: The voltage of the low state in volts
    :param v1: The voltage of the high state in volts
    :param freq: The frequency of the ramp wave in Hz. The frequency can be adjusted from 100 mHz to 100 kHz.
    :param symmetry: Symmetry represents the amount of time per cycle that the ramp waveform is rising and can be adjusted from 0% to 100%.
    """

    inst.write('WGEN:FUNCtion RAMP')
    inst.write(f':WGEN:VOLTage:LOW {v0}')
    inst.write(f':WGEN:VOLTage:HIGH {v1}')
    inst.write(f':WGEN:FREQuency {freq}')
    inst.write(f':WGEN:FUNCtion:RAMP:SYMMetry {symmetry}')
    inst.query('*OPC?')


def setWGenPulse(inst, v0: float, v1: float, period: float, pulseWidth: float) -> None:
    """Sets the waveform generator to a pulse wave. (Only available on specific models)

    :param inst: The instrument object from pyscpi or pyvisa
    :param v0: The voltage of the low state in volts
    :param v1: The voltage of the high state in volts
    :param period: The period of the pulse wave in seconds. The period can be adjusted from 10 ns to 10 s.
    :param pulseWidth: The pulse width can be adjusted from 20 ns to the period minus 20 ns.
    """

    inst.write('WGEN:FUNCtion PULSe')
    inst.write(f':WGEN:VOLTage:LOW {v0}')
    inst.write(f':WGEN:VOLTage:HIGH {v1}')
    inst.write(f':WGEN:PERiod {period}')
    inst.write(f':WGEN:FUNCtion:PULSe:WIDTh {pulseWidth}')
    inst.query('*OPC?')


def setWGenDC(inst, offset: float) -> None:
    """Sets the waveform generator to a DC wave. (Only available on specific models)

    :param inst: The instrument object from pyscpi or pyvisa
    :param offset: The offset of the DC wave in volts
    """

    inst.write('WGEN:FUNCtion DC')
    inst.write(f':WGEN:VOLTage:OFFSet {offset}')
    inst.query('*OPC?')


def setWGenNoise(inst, v0: float, v1: float, offset: float) -> None:
    """Sets the waveform generator to a noise wave. (Only available on specific models)

    :param inst: The instrument object from pyscpi or pyvisa
    :param v0: The voltage of the low state in volts
    :param v1: The voltage of the high state in volts
    :param offset: The offset of the noise wave in volts
    """

    inst.write('WGEN:FUNCtion NOISe')
    inst.write(f':WGEN:VOLTage:LOW {v0}')
    inst.write(f':WGEN:VOLTage:HIGH {v1}')
    inst.query('*OPC?')


def _log(msg, EnableLog: bool) -> None:
    if EnableLog:
        print(msg)
