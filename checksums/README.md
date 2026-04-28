# Checksums

Release checksums should be published with each GitHub Release.

For v1.0.0, the release should include:

```text
SHA256SUMS
```

Users should verify the downloaded image before flashing it.

Linux:

```bash
sha256sum -c SHA256SUMS
```

macOS:

```bash
shasum -a 256 pcbm-v1.0.0-rpi3-5.img.xz
```

Compare the macOS result to the checksum listed in `SHA256SUMS`.
