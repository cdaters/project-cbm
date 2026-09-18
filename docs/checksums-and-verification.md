> **Historical v1.0 documentation.** For current 1.1 instructions use the
> [user guide](release/user-guide.md), [networking guide](release/networking.md)
> and [recovery help](release/recovery.md). Old credentials and service defaults do not apply.

# Checksums and Verification

> Use the checksum asset from the matching release. The repository v1.0.0 copy
> contains a preserved malformed trailing record; see [current checksum notes](v1.0-current-notes.md#checksums).

Project CBM release images should be verified before flashing.

Download files from the GitHub Release:

```text
pcbm-v1.0.0-rpi3-5.img.xz
pcbm-v1.0.0-docs.zip
SHA256SUMS
```

## Linux

From the folder containing files:

```bash
sha256sum -c SHA256SUMS
```

A successful result should report that the image is OK.

## macOS

macOS does not always include `sha256sum` by default. Use:

```bash
shasum -a 256 -c SHA256SUMS
```

If the files are valid, you should see output similar to:

```text
pcbm-v1.0.0-rpi3-5.img.xz: OK
pcbm-v1.0.0-docs.zip: OK
```

If verification fails, delete the downloaded file and download it again from the official Project CBM GitHub Release.

## Why this matters

Checksum verification confirms that the image you downloaded matches the image that was published. It helps catch corrupted downloads and accidental file mismatches.
