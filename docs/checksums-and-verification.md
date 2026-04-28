# Checksums and Verification

Project CBM release images should be verified before flashing.

Download both files from the GitHub Release:

```text
pcbm-v1.0.0-rpi3-5.img.xz
SHA256SUMS
```

## Linux

From the folder containing both files:

```bash
sha256sum -c SHA256SUMS
```

A successful result should report that the image is OK.

## macOS

macOS does not always include `sha256sum` by default. Use:

```bash
shasum -a 256 pcbm-v1.0.0-rpi3-5.img.xz
```

Compare the output against the checksum listed in `SHA256SUMS`.

## Why this matters

Checksum verification confirms that the image you downloaded matches the image that was published. It helps catch corrupted downloads and accidental file mismatches.
