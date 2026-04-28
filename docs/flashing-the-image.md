# Flashing the Project CBM Image

Project CBM is distributed as a compressed Raspberry Pi image:

```text
pcbm-v1.0.0-rpi3-5.img.xz
```

Writing this image to a microSD card will erase the selected card.

## Recommended: Raspberry Pi Imager

1. Download the `.img.xz` file from the Project CBM GitHub Releases page.
2. Insert a microSD card into your computer.
3. Open Raspberry Pi Imager.
4. Choose your Raspberry Pi model.
5. Choose **Use custom** for the operating system.
6. Select `pcbm-v1.0.0-rpi3-5.img.xz`.
7. Choose the correct microSD card.
8. Skip extra customization options unless the release notes specifically say otherwise.
9. Write the image.
10. Let Imager verify the card.
11. Eject the card, insert it into the Raspberry Pi, connect HDMI and keyboard, then power on.

## Alternative: BalenaEtcher

BalenaEtcher can also write `.img.xz` files.

1. Select the Project CBM image.
2. Select the microSD card.
3. Flash the image.
4. Let Etcher verify the write.
5. Eject the card and boot the Pi.

## Linux command-line example

Use this only if you are comfortable identifying disk devices.

```bash
xzcat pcbm-v1.0.0-rpi3-5.img.xz | sudo dd of=/dev/sdX bs=4M status=progress conv=fsync
```

Replace `/dev/sdX` with the correct device for your SD card.

`dd` will overwrite whatever device you point it at. Check twice before pressing Enter.

## Do not copy the image file to the card

Do not drag `pcbm-v1.0.0-rpi3-5.img.xz` onto the SD card as a normal file. That will not create a bootable Project CBM card.
