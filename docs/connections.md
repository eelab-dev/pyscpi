# Connection Guide

There are several ways to connect the instrument to your computer. You can use any of the following methods:

## Keysight IO Libraries Suite using USB

The easiest method for connecting your oscilloscope to a laptop is using the Keysight IO Libraries Suite. This comprehensive collection of instrument drivers enables seamless communication between the oscilloscope and your computer. The software can be easily downloaded from the Keysight website, and once installed, it allows for a direct USB or Ethernet connection between the instrument and the laptop. While the option to connect via Ethernet is available, it is recommended to use the USB connection as it is generally more straightforward to set up. Configuring Ethernet connections can be more complex and require additional network configurations, making the USB connection the preferred method for most students.

### Windows

### WSL2

WSL2 is not yet supported using this method. Please refer to driverless methods for connecting using WSL2.



## Driverless Methods

There are several other methods for connecting your oscilloscope to your computer. These methods do not require using the Keysight IO Libraries Suite, and can be adjusted manually based on project requirements. It's important to note that these methods may require more technical knowledge and may be more challenging to set up compared to using the Keysight IO Libraries Suite. These methods apply to all Keysight Smart Bench Essentials.

## USB

This method is based on USBTMC (USB Test and Measurement Class) protocol, which is a USB class protocol that allows communication with instruments that support the USBTMC standard. USBTMC is a standard protocol for controlling test and measurement instruments over USB and it allows for bi-directional communication between the instrument and the computer. This method is useful for connecting the oscilloscope to the computer as it uses a standard USB connection, which is widely available on most computers.

### Windows

### WSL2

## Direct Ethernet Cable

This method of connecting the oscilloscope to the laptop is based on a direct Ethernet connection. This method involves connecting the oscilloscope and the laptop using an Ethernet cable and establishing a direct communication link between the two devices.However, to establish a stable connection, additional network configurations such as IP addressing may be required. In this method, it is recommended to use APIPA (Automatic Private IP Addressing) over DHCP because it eliminates the need for additional software or a DHCP server to be present on the network. This can be useful in laboratory settings where a DHCP server is not available or difficult to set up. However, it's important to note that using APIPA may lead to poor perfromance and may cause issues with the connection especially in laptops with more than one network interface. In these cases, it is recommended to use DHCP instead.

### using APIPA (Windows & WSL2)

### using DHCP (Windows & WSL2)



## Switch

This method of connecting the oscilloscope to the laptop is based on a switch connection. This method involves connecting the oscilloscope and the laptop using a powered switch. Using More than once device can be connected to the laptop. Similar to the previous method of connecting the oscilloscope to the laptop, additional network configurations such as IP addressing may be required. In this method, it is recommended to use APIPA (Automatic Private IP Addressing) over DHCP because it eliminates the need for additional software or a DHCP server to be present on the network. This can be useful in laboratory settings where a DHCP server is not available or difficult to set up. However, it's important to note that using APIPA may lead to poor perfromance and may cause issues with the connection especially in laptops with more than one network interface. In these cases, it is recommended to use DHCP instead. use the same instructions as the previous method.

## Router

This method is same as the previous method of connecting the oscilloscope to the laptop, but instead of using a switch, a router is used. This method involves connecting the oscilloscope and the laptop using a router. Using More than once device can be connected to the laptop. However unlike the previous methods  additional network configurations such as IP addressing is not required since the router is responsible for assigning IP addresses to the devices connected to it. Simply connect the oscilloscope to the router using an Ethernet cable and connect the laptop to the router using ethernet cable.

It is important to note that this method may require privileged access to the router, which is generally unavailable in laboratory or enterprise settings due to security measures such as MAC address filtering. This can limit the usability of this method in such environments. However, this method can be useful in home networks where the router is not configured for automatic IP assignment and users have more control over the network settings. In such settings, users may connect the oscilloscope and the laptop without the need for additional network configurations.

