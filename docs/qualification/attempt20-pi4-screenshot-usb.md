# Attempt20 Pi4 owner qualification

**PRIVATE NON-RELEASE Project CBM1.2.0-dev.3. All cases below initially UNTESTED.**
Use a separate card; leave attempt18 and attempt19 evidence unchanged.

Raw SHA-256: `014e9598453e9361984559ac060583dbfb76947ba51206d704c6773e2175d330` (3,095,396,352 bytes).
XZ SHA-256: `8a7e07bd58f126be105f31b63f782d313d1c08f1634174b5090fb1ab8bcfe356` (599,067,756 bytes).
Lock: `dc28290451f7b8ce78eca9625bd3d0ab052ab7df2c61f5776a666c48bd83d514`.
[Exact paths, packages and validation](../build/private-1.2-dev3-attempt20.md).

Follow the [bounded screenshot and USB procedure](screenshot-private-pi4-procedure.md)
for this exact image: S1–S11 (Menu, text, normal MC, guided Import, USB MC, Cover,
VICE/BASIC, moving gameplay, repeats, unavailable display and transitions). Use
`pcbm-screenshot [basename.png]` over SSH as pcbm. Compare the copied PNG with HDMI,
record approximate latency and any audio/gameplay impact, and verify no display or
F10/return lifecycle disruption. Do not patch the running image after a failure.

For guided Import, verify friendly folder/file names without opaque tags; select
known duplicate/similar labels and confirm the intended underlying entry. Capture
these screens with pcbm-screenshot where practical. Keep category/machine explicit;
PRG supported, BIN unsupported, unsupported-only directory0 supported. Normal manual
MC copy and guided CONTENT Import are both present; neither supersedes the other.

Repeat normal MC → USB read-only browse → selected manual copy → F10 → Safe Unmount
→ C64/copied demo → F10 → responsive Menu, plus ordinary reboot/shutdown and copied
content persistence. Attempt19 passed the reported lifecycle; that is a baseline,
not a retroactive attempt20 result. Broad U1–U6 fixture combinations remain untested
except their recorded attempt19 subsets. Busy-unmount failure injection remains an
optional, separate robustness case, not an unperformed normal-safe-unmount test.
Use actual listing/scan/copy/release responsiveness and screenshot times for T1;
no obsolete nonexistent workflow assumptions or formal timing target is imposed.

Record PASS/FAIL/UNTESTED/BLOCKED per case against this hash, actual hardware and
observed behavior. Stop an affected failing case for evidence collection. No release
or further feature work follows automatically.
