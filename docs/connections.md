# Connection Guide

There are several ways to connect the instrument to your computer. You can use any of the following methods:

## Keysight IO Libraries Suite using USB

The easiest method for connecting your oscilloscope to a laptop is using the [Keysight IO Libraries Suite](https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html). This comprehensive collection of instrument drivers enables seamless communication between the oscilloscope and your computer. The software can be easily downloaded from the Keysight website, and once installed, it allows for a direct USB or Ethernet connection between the instrument and the laptop. While the option to connect via Ethernet is available, it is recommended to use the USB connection as it is generally more straightforward to set up.

### Windows

Simply download and run the installer with admin privilege from the [Keysight website](https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html). Once installed, you can connect the oscilloscope to the laptop using a USB cable.

### WSL2

WSL2 is not yet supported using this method. Please refer to other methods for connecting using WSL2.


## USBTMC

This method is based on USBTMC (USB Test and Measurement Class) protocol, which is a USB class protocol that allows communication with instruments that support the USBTMC standard. USBTMC is a standard protocol for controlling test and measurement instruments over USB and it allows for bi-directional communication between the instrument and the computer. This method is useful for connecting the oscilloscope to the computer as it uses a standard USB connection, which is widely available on most computers.

### Windows
- Install the [Zadig](https://zadig.akeo.ie/) driver installer. (closed software, run at your own risk)
- Connect the oscilloscope to the computer using a USB cable.
- Open Zadig and select the oscilloscope from the list of devices.
- Select the WinUSB driver from the list of drivers and click on the Replace Driver button.
- Install [libusb](https://libusb.info/) by downloading the [latest archive](https://github.com/libusb/libusb/releases/latest)
- Extract the archive and copy the `libusb-1.0.dll` from `VS2015-x64/dll/` to the `C:\Windows\System32` folder. (you need admin privilege to do this)
- install the [PyUSB](https://github.com/pyusb/pyusb) library using command `python -m pip install pyusb`.
- In the code, use the following code to connect to the instrument:
```python
from pyscpi import usbtmc

inst =  usbtmc.Instrument(<VendorID>, <ProductID>)
```
- Replace `<VendorID>` and `<ProductID>` with the Vendor ID and Product ID of the instrument.


### WSL2

- Install [usbipd-win](https://github.com/dorssel/usbipd-win/releases/latest) by downloading and running the latest `*.msi` release.
- follow the commands [here](https://github.com/dorssel/usbipd-win/wiki/WSL-support#usbip-client-tools) to prepare WSL2 for usbipd-win.
```bash
sudo apt install linux-tools-virtual hwdata
sudo update-alternatives --install /usr/local/bin/usbip usbip `ls /usr/lib/linux-tools/*/usbip | tail -n1` 20
```
- Install the latest version of [wsl-usb-gui](https://gitlab.com/alelec/wsl-usb-gui/-/releases).
- Open `wsl-usb-gui` and select the oscilloscope from the list of devices.
- Click the `Attach` button. This will attach the oscilloscope to WSL2, and detach it from Windows.
- Confirm that the oscilloscope is attached to WSL2 by running the following command in WSL2 by running `lsusb`.
- You should enable permissions for `udev` to access the device.
- In WSL2 install the [PyUSB](https://github.com/pyusb/pyusb) library using command `python -m pip install pyusb`.
- In the code, use the following code to connect to the instrument:
```python
from pyscpi import usbtmc

inst =  usbtmc.Instrument(<VendorID>, <ProductID>)
```
- Replace `<VendorID>` and `<ProductID>` with the Vendor ID and Product ID of the instrument.


## TCP/IP Sockets (Driverless)

There are several other methods for connecting your oscilloscope to your computer. These methods do not require using the Keysight IO Libraries Suite, and can be adjusted manually based on project requirements. It's important to note that these methods may require more technical knowledge and may be more challenging to set up compared to using the Keysight IO Libraries Suite. These methods apply to all Keysight Smart Bench Essentials.



### Direct Ethernet Cable

This method of connecting the oscilloscope to the laptop is based on a direct Ethernet connection. This method involves connecting the oscilloscope and the laptop using an Ethernet cable and establishing a direct communication link between the two devices.However, to establish a stable connection, additional network configurations such as IP addressing may be required. In this method, it is recommended to use APIPA (Automatic Private IP Addressing) over DHCP because it eliminates the need for additional software or a DHCP server to be present on the network. This can be useful in laboratory settings where a DHCP server is not available or difficult to set up. However, it's important to note that using APIPA may lead to poor perfromance and may cause issues with the connection especially in laptops with more than one network interface. In these cases, it is recommended to use DHCP instead.

#### using APIPA (Windows & WSL2)

#### using DHCP (Windows & WSL2)



### Switch

This method of connecting the oscilloscope to the laptop is based on a switch connection. This method involves connecting the oscilloscope and the laptop using a powered switch. Using More than once device can be connected to the laptop. Similar to the previous method of connecting the oscilloscope to the laptop, additional network configurations such as IP addressing may be required. In this method, it is recommended to use APIPA (Automatic Private IP Addressing) over DHCP because it eliminates the need for additional software or a DHCP server to be present on the network. This can be useful in laboratory settings where a DHCP server is not available or difficult to set up. However, it's important to note that using APIPA may lead to poor perfromance and may cause issues with the connection especially in laptops with more than one network interface. In these cases, it is recommended to use DHCP instead. use the same instructions as the previous method.

### Router

This method is same as the previous method of connecting the oscilloscope to the laptop, but instead of using a switch, a router is used. This method involves connecting the oscilloscope and the laptop using a router. Using More than once device can be connected to the laptop. However unlike the previous methods  additional network configurations such as IP addressing is not required since the router is responsible for assigning IP addresses to the devices connected to it. Simply connect the oscilloscope to the router using an Ethernet cable and connect the laptop to the router using ethernet cable.

It is important to note that this method may require privileged access to the router, which is generally unavailable in laboratory or enterprise settings due to security measures such as MAC address filtering. This can limit the usability of this method in such environments. However, this method can be useful in home networks where the router is not configured for automatic IP assignment and users have more control over the network settings. In such settings, users may connect the oscilloscope and the laptop without the need for additional network configurations.

