# Crownstone UART

Official Python lib for Crownstone: "Crownstone Unified System Bridge", or **Crownstone USB** implementation.

This works on all platforms and requires a **Crownstone USB** to work.

# Install guide

This module is written in Python 3 and needs Python 3.7 or higher. The reason for this is that most of the asynchronous processes use the embedded asyncio core library.

If you want to use python virtual environments, take a look at the [README_VENV](README_VENV.MD)

You can install the package by pip:
```
pip3 install crownstone-uart
```

If you prefer the cutting edge (which may not always work!) or want to work on the library itself, use the setuptools: `python3 setup.py install`


## Requirements for the Crownstone USB

### OS X
OS X requires installation of the SiliconLabs driver: [https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)

### Ubuntu
In order to use serial without root access, you should be in the `dialout` group.

You can check if you're in the group:
```
$ groups
```

To add yourself:
```
$ sudo adduser $USER dialout
```

You may need to logout and login again.


### Raspbian
Similar to Ubuntu.

### Arch Linux
To use serial in Arch Linux, add yourself to the `uucp` group.

To add yourself to the group:
```console
$ sudo gpasswd -a $USER uucp
```
Make sure to logout and login again to register the group change.

# Example

An example is provided in the root of this repository.

## Prerequisites

- First use the [phone app](https://crownstone.rocks/app) to setup your Crownstones and the Crownstone USB.
- Make sure you update the Crownstones' firmware to at least 5.4.0.
- Find out what port to use (e.g. `COM1`, `/dev/ttyUSB0`, or `/dev/tty.SLAB_USBtoUART`), use this to initialize the library.
- Have this library installed.

## Find the IDs of your Crownstones

Firstly run the example script that simply lists the IDs of the Crownstones.:
```
$ python3 ./examples/discovery_example.py
```

Once some IDs are printed, use one of them for the next example. This can take a while because Crownstones, if not switched, only broadcast their state every 60 seconds.


## Switch a Crownstone, and show power usage.

Edit the file `switch_example.py`:
- Set `targetCrownstoneId` to a Crownstone ID that was found in the previous example.

Run the file:
```
$ python3 ./examples/switch_example.py
```


# API documentation

[The API documentation can be found here.](./DOCUMENTATION.md)


# License

MIT
