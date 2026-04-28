# Troubleshooting

## I do not see the Project CBM menu

Try these:

1. Make sure the Pi has booted fully.
2. Check HDMI and keyboard connections.
3. Press Enter once.
4. If you are at the Linux command line, run:

```bash
pcbm-menu
```

or:

```bash
/usr/local/bin/pcbm-menu
```

## I launched a C128 file and it does not work

The Content menu uses the current default machine.

Set the correct default machine first:

```text
MACHINES -> DEFAULT -> C128
```

or:

```text
MACHINES -> DEFAULT -> C12880
```

Then launch the file again.

## I cannot find the Pi on the network

Try:

1. Plug in Ethernet.
2. Go to `CONTROL -> NETWORK`.
3. Look for the IP address.
4. Use the IP address instead of `pcbm.local`.
5. Run `TEST` in the Network Menu.
6. Reboot the Pi.

## Samba file sharing does not appear

Try:

```text
CONTROL -> NETWORK -> SAMBAON
```

Then connect using the IP address shown in the Network Menu.

The share name is:

```text
Project CBM
```

## WiFi is not working

WiFi is intentionally left unconfigured in the release image.

Go to:

```text
CONTROL -> NETWORK -> CONFIG
```

Set your WiFi country, then configure wireless LAN.

## USB Import says no USB drive was found

Try:

1. Use a normal USB flash drive.
2. Make sure it has a readable partition.
3. Try FAT32 or exFAT.
4. Unplug and reconnect the drive.
5. Restart Project CBM or reboot the Pi.

## VICE opens, but I cannot find the emulator menu

Press:

```text
F10
```

Project CBM sets the VICE UI key to F10.

## I accidentally exited to the Linux command line

Run:

```bash
pcbm-menu
```

or reboot:

```bash
sudo reboot
```
