# Current checksums and verification

For **Project CBM 1.1.0**, download
[project-cbm-1.1.0.img.xz](https://github.com/cdaters/project-cbm/releases/download/v1.1.0/project-cbm-1.1.0.img.xz)
and [SHA256SUMS](https://github.com/cdaters/project-cbm/releases/download/v1.1.0/SHA256SUMS).
Follow the [current verification commands](release/getting-started.md#download-and-check-the-image)
for macOS, Linux or Windows. The image SHA-256 is:

```text
8b3738a204da16e148f5674a95f1ffb55a67b8ad1ce1d997b1858594a899c13d
```

SHA256SUMS lists 19 accompanying release assets. Checking the entire list without
all those downloads will report missing files; verifying the image alone is sufficient
before flashing. A checksum detects changed bytes, not independent publisher trust.
Do not use the old filenames or historical checksum file below for 1.1.0.

## Historical 1.0 instructions — retained unchanged

The original guide below documents the earlier release and is not current setup advice.

---

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
