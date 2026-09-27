# Attempt24: Pi 4 UX, Online Library and attribution qualification

**PRIVATE NON-RELEASE 1.2.0-dev.5 / attempt24.**

2026-09-27 update: [owner results and read-only diagnosis](attempt24-owner-review-2026-09-27.md)
record successful Assembly64 downloads, supported/unsupported guided-preview evidence,
and direct-default-machine boot **FAIL** (VICE selects offscreen before boot artwork
release). Preserve this image. Other cases below remain UNTESTED unless separately
recorded; the download report does not establish the whole save/lifecycle matrix.

Subsequent owner evidence: external TERM of invisible VICE restored visible Menu
but not physical keyboard responsiveness, despite apparently correct foreground
ownership. A later mistaken `kbd_mode -s` diagnostic changed the mode; only after
that was raw/scancode mode measured. Forcing Unicode mode restored usability.
See the linked chronology: original keyboard mode is UNKNOWN, automatic post-TERM
keyboard cleanup is FAIL, manual recovery is PASS, and normal direct-boot F10/exit
remains UNTESTED. Do not reproduce or repair this on attempt24.

Additional [full physical results](attempt24-full-physical-results-2026-09-27.md) record
Central search/metadata/download/save, guided Import UX, normal FILES/USB and game
capture PASS in the owner-reported scope. Filter/server failures remain intermittent;
Cover capture is UNTESTED, not FAIL.

Raw SHA-256 `754b34e4ab1abd0af65d97956546f295036a4a418b15c20d7f3dd0f14fd1ba7c` (3,095,396,352 bytes).
XZ SHA-256 `efb7f642b91160b2143abd7f958509f2ffc2f8d618667ba697a4c1f01955f051` (598,643,500 bytes).
Lock `ee0308da672c783cf3142e7a581b80344e42cc3605f227b7d8f18cb50dd62819`.
[Exact paths, packages and validation](../build/private-1.2-dev5-attempt24.md).
Preserve21 as an intermediate build and22/23 as failed preflight/freeze evidence;
use this image for the combined requested qualification.


Do not update attempt20 in place. Preserve its card/captures and use the new image
on separate media. This procedure qualifies only the exact image and Pi model
recorded in the completed build record. Stop a failing case and retain a screenshot
and the reproduction; do not repair that qualification image in place.

Record PASS/FAIL/UNTESTED for each case, hardware, image SHA-256 and observations.
Prior attempt20 results remain valid for that image; they do not automatically
qualify changed behavior here.

1. **Screenshot storage/privacy.** From the engineering Mac, with Main Menu visible,
   run `ssh pcbm@projectcbm.local 'pcbm-screenshot'`. It prints an absolute path under
   `/home/pcbm/content/screenshots/`. Names use `pcbm-YYYYMMDDTHHMMSSZ.png`; repeated
   captures in the same second use `-01`, `-02`, etc. Check directory 0700, files
   0600 and pcbm ownership; access through the existing authenticated Project CBM
   SMB share. Existing `/home/pcbm/screenshots` captures stay untouched if present
   on retained old media; a fresh image does not migrate files from another card.
   Try an explicit basename twice: the second attempt must refuse overwrite.
   `time pcbm-screenshot` is optional timing instrumentation, not normal syntax.
2. **Dialog presentation.** CONTENT, FILES/USB, CONTROL and subordinate dialogs show
   a clear compact hierarchy and action title. Device sizes are readable KB/MB/GB,
   using 1024-byte steps. Arrow/Tab/Enter/Escape behavior remains usable; no opaque
   IDs, hashes or backend keys appear alongside friendly names.
3. **Guided Import navigation.** CONTENT > Import from USB; select a partition,
   navigate into nested folders, Scan, then Back. It returns to source navigation
   while keeping the read-only lease. Parent folder works; scan a different folder
   without remounting. End Import / Release USB is the deliberate exit. Test an
   unsupported-only ROM folder: explain files are present but unsupported, show
   no Select All for an empty supported list, suggest FILES > USB Drive. Mixed
   PRG/BIN: select/import only PRG after explicit category/machine review. BIN must
   remain unsupported. Capture these screens using pcbm-screenshot.
4. **FILES USB regression.** Ordinary MC, then FILES > USB Drive > partition > Mount
   Read-Only. Check arrows, Tab, function keys, manual copy of chosen test content,
   F10 and normal Safe Unmount. No writable USB mount. Deliberate busy-unmount fault
   injection is optional robustness coverage; do not conflate it with normal release.
5. **Attribution and Online search.** Open About & Support Assembly64: team credit,
   independent Project CBM API client, official site and optional PayPal/Ko-fi links.
   It works without contacting the backend; Back returns normally. No payment action
   or FTP fallback is present.

   **Online search and details.** CONTENT > Online Library shows Powered by Assembly64
   and Internet connection required. Search a known title, inspect metadata and files;
   test one offered repository/category/year filter and Back/retry. Check friendly
   labels, sensible result paging and responsiveness. Server Information is a separate
   public directory; Central stays selected and listed unqualified servers are not
   silently queried. A directory failure must not prevent trying a Central search.
6. **Selected download and library save.** Choose a small release you are entitled to
   use. Select each required disk/file; choose category and machine explicitly.
   Prepare Save downloads only the selection into private temporary storage. Review
   exact destination/Already Present/Keep Both, then Save to Library. Verify folders
   and disk relationships, no MIME envelope in media files, no extra files and no
   overwrite. Repeat the same selection to exercise Already Present; a deliberately
   different local same-name copy should result in Keep Both for the set. Back before
   final Save must leave the library untouched. Test cancellation on an appropriate
   small operation; completed saves remain, incomplete staging does not become content.
7. **Offline and lifecycle.** Saved content appears in Browse Library and remains
   available offline. Launch the copied/downloaded C64 demo through the existing
   launcher, verify display/audio, F10 and responsive Menu. Save & Run is not included.
   Check persistence after reboot and ordinary shutdown. Direct boot to the current
   default machine is now a separate known FAIL: stop that case on attempt24 and
   retain evidence; a corrected candidate must demonstrate visible VICE and normal
   F10/Menu return after the boot-artwork handoff. On the corrected candidate,
   verify the entire boot artwork -> Cover -> visible VICE -> F10/Quit/exit ->
   restored tty1 kernel keyboard/console modes -> responsive physical Menu sequence.
   Include bounded external-TERM and failed/abnormal-launch cleanup tests, recording
   read-only mode observations before any recovery. A foreground dialog and visible
   redraw are not sufficient for PASS. Disconnecting Internet
   should produce a concise network error with Back/Retry; restore connectivity
   using normal controls, not modifications to the image.
8. **Capture coverage.** Capture Main Menu, text console, ordinary MC, guided Import,
   USB MC, a machine Cover, VICE/BASIC and moving C64 gameplay. The new GPL helper corrects attempt20’s rejection of
   normal page flips; moving gameplay capture is a required retest. Copy each intended PNG
   to the engineering Mac and compare against HDMI: colors, content and borders;
   capture must not change the display. Note latency and any audio/gameplay impact,
   repeat captures, and try near a Cover/display transition. A transition may fail
   concisely rather than save a misleading image. F10/return remains normal. Record
   unsupported/no-display as UNTESTED if headless setup would be disruptive; do not
   infer multi-display support. Screenshots can contain private filenames, addresses
   or credentials: keep them private and share only deliberately selected captures.

No throughput download, background crawl, provider messages or publication. Exact
provider rate quotas, other-server policies and any remaining download semantics
can be revisited after this physical evidence. Report remaining questions before
contacting the provider; do not send messages automatically.
