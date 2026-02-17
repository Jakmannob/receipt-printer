# receipt-printer

A collection of scripts I use for my receipt printer project.
The project is designed to work on Linux, specifically on the **Raspberry Pi** (4 or newer).

## Setup

Setup is dependent on your USB devices, so you need to personalize it.
Connect both your **thermal POS printer** and your **USB camera** to your RPi and turn both devices on.

### Configuration

You first need to find out the USB information of your devices.
Run:

```console
$ lsusb
```

And find the correct lines for your devices, which should look like:

```console
Bus xxx Device xxx: ID <VENDOR_ID>:<PRODUCT_ID> <NAME>
```

Put the `<VENDOR_ID>`, `<PRODUCT_ID>` and `<NAME>` into the `devices.toml` config file.
Also, you may set the `paper_width` and `has_cutter` attributes for your printer in that config file.
The device setup will create a system symlink to your camera, you can customize this by replacing the value for `device` in the camera config.

### Installation

To install, you then must set up the virtual environment and udev rules for the USB devices.
Run:

```console
$ setup.sh
$ sudo install.sh
```

## Running the project

Execute:

```console
$ run.sh
```
