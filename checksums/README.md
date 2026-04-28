# Project CBM Checksums

This folder contains archived checksum files for Project CBM release assets.

Checksums allow users to verify that downloaded release files have not been corrupted, altered, or incompletely downloaded.

The primary checksum file for each release is also attached directly to the matching GitHub Release.

## Available Checksums

| Version | File |
|---|---|
| v1.0.0 | `v1.0.0/SHA256SUMS` |

## Verifying a Download

After downloading the release assets and the matching `SHA256SUMS` file, place them in the same folder and run:

Linux / Raspberry Pi OS:

```bash
sha256sum -c SHA256SUMS
```

macOS:

```bash
shasum -a 256 -c SHA256SUMS
```

If the files are valid, you should see output similar to:

```text
pcbm-v1.0.0-rpi3-5.img.xz: OK
pcbm-v1.0.0-docs.zip: OK
```

If verification fails, delete the downloaded file and download it again from the official Project CBM GitHub Release.
