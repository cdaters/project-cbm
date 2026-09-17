# POC4 run 2: runtime evidence and source-correction review

This is additive to the [initial investigation](poc4-regression-investigation-2026-09-17.md),
[run 1 attestation](poc4-attempt3-pi3b-owner-report-2026-09-17.json), and
[first-boot audit](poc4-first-boot-ux-findings-2026-09-17.md). Historical reports retain
their original evidence limits. [Run 2 attestation](poc4-attempt3-run2-2026-09-17.json)
records the independent reproduction. No new physical test was performed by Codex.

## Executive decision

Both physical root causes remain **UNCONFIRMED**; their relationship is **UNKNOWN**.
One recovered launch establishes successful x64sc/KMSDRM startup and normal exit,
not terminal restoration. Missing instrumentation cannot be reconstructed.

The owner subsequently authorized engineering use of the already-mounted read-only
Paragon card despite unknown earlier journal behavior, and independently correct,
testable defensive source work despite lack of absolute root-cause proof. Source
hardening and bounded first-boot corrections are implemented, not a physically
qualified fix. Next-candidate construction remains separately gated. No AGENTS edit,
package build/version/tag, lock, image, service activation, push or publication.

## Card, collection and photographs

At collection `/dev/disk4` was the removable USB MBR card, 32,227,983,360 bytes.
FAT32 boot `/dev/disk4s1` (offset 8,388,608, size 536,870,912) was already mounted
writable at `/Volumes/bootfs`. Ext4 `/dev/disk4s2` (offset 545,259,520, size
31,682,706,944) was already mounted **read-only**, Paragon `ufsd_ExtFS`, at
`/Volumes/rootfs`. No mount state changed; boot files were not accessed. Paragon
application version observed previously: 14.0.46. Earlier writable root mounting
and journal replay are UNKNOWN, not asserted absent or present.

Classification: **READ-ONLY ENGINEERING RUNTIME EVIDENCE FROM A USED PHYSICAL POC4
REPRODUCTION CARD**. It is neither pristine forensic capture nor immutable candidate
evidence. Installed identity was read first and matched lock
`435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9`, Product
1.1.0-poc.4, integration `b362c70215cef0e2c6c6a845635c47fd39b3ebbf`, Menu
1.1.0~poc4.1-1+pcbm1. No whole used-card hash comparison was made.

Private external directory: `qualification/poc4-run2-2026-09-17` under configured
ProjectCBM-Work. `inventory.json` SHA-256:
`4852ff9f49f5f785fdead33ec28cdda5dccae2d72a7b63676b4de5f8af5aa23b`.
It contains every relative path, presence/absence, byte count and SHA-256, plus the
five photograph captions/hashes. `collection-script.py` records the exact allowlist,
identity/read-only checks, non-symlink checks and source/copy/source hash agreement.
Nine card files and five photographs were copied; no lock files, NetworkManager
profiles, credentials, /etc, full home or journal were copied. Private logs stay
outside Git. Free-form VICE output was reviewed for sensitive-pattern presence and
only bounded non-secret diagnostic facts are summarized here. TheBench has ownership
disabled and is unencrypted; private classification is not an encryption claim.

Photos 01–05 show respectively `us`, `en_US.UTF-8`, `UTC`, `America/Phoenix`, and the
visible returned Menu with Commodore 64 default/RUN selected. Original supplied
hashes all reverified. No still photo proves keyboard/VT response, timing, audio or
motion. Dynamic PASS/FAIL classifications come from the owner.

## Recovered launch and setup facts

All retained slots were inspected: exactly `launch-1789611551300369799`. It has
`record.json`, `before.json`, `sample-0.json`, and `vice.log`. Samples 1/2, top-level
snapshot/report and `/var/log/journal/` were absent. No new reports were generated.

- Profile `x64sc`, executable `/usr/bin/x64sc`, no content autostart; UID 1000;
  launcher PID 1215, VICE PID 1244. Phase `exited`, status **0**, signal null.
- Monotonic start 559.002774890, audio complete 559.334208431, end 587.033407119:
  about 28.031 seconds for the recorded wrapper interval, excluding Cover. This is
  neither a first-boot timing nor a measurement of perceived return latency.
- `before.json` is **AFTER Cover, BEFORE VICE**. Both snapshots report tty1 and
  login sessions for tty1 and tty2; Menu PID 1178 and shell launcher PID 1207 sleep
  in `do_wait`. These are expected waiting ancestors, not proof of a hung Menu.
- During sample 0 VICE is running, four threads. Both snapshots show 1080p60 active
  DRM output. Getty tty1/tty2, first-boot unit and NetworkManager report active;
  SSH inactive. NetworkManager running does not mean networking was enabled.
- VICE telemetry: KMSDRM/OpenGL, fullscreen, logical 719x544, equal X/Y scale
  1.985294, window/output 1920x1080, VICII true-aspect resource. This supports
  unchanged geometry configuration, not a new physical geometry PASS.
- ALSA driver/device opened at 48 kHz. HDMI subdevice available before launch and
  in use in sample 0. This is not proof of audible output. No joystick detected;
  joystick use in this run remains UNTESTED. Optional 2000/4000/CMDHD drive-ROM
  messages do not explain the keyboard/VT regression.
- Setup state/status agree: complete=true; region, owner and network markers.
  Root-growth completion marker is true. Growth journal records the earlier
  partition proposal/free tail; it is not a current free-space measurement.
  Network marker does not identify enabled/offline choice or Wi-Fi success.
  None of these files records navigation history or per-operation duration.

## Updated differential

The detailed original matrix remains in the initial investigation. These are the
relevant updates; **no physical cause is classified CONFIRMED CAUSE**.

| Component / behavior | POC3 → frozen POC4 #3 | Missing Cover? | Dead input/VT? | Classification / confidence | Evidence and next test |
| --- | --- | --- | --- | --- | --- |
| Base/SDL/PAM/systemd/kernel catalog | Identical package catalog | No differential explanation | No binary-drift explanation | UNRELATED as a package-change hypothesis; high | Retained hash differential; preserve exact packages |
| VICE binary/geometry | Identical package bytes | Cannot explain new prelaunch artwork by itself | Runtime interaction still possible | UNRELATED as binary regression; high | Run2 KMSDRM/OpenGL/status0; physically recheck geometry/audio |
| tty1/tty2 getty/PAM recipes | Unchanged; setup/session consumer added | Indirectly possible | Later session behavior unknown | POSSIBLE CONTRIBUTOR; low | Both VTs work prelaunch and sessions exist during VICE; capture postcleanup |
| Registry/profile/art | New Cover mapping; seven assets present | Mis-selection not supported | No direct input ownership | UNRELATED to mapping defect on default run; high | Run2 x64sc agrees with c64 mapping; test explicit/content profiles |
| SDL Cover | New process, 0.75s presentation | Yes | Can change keyboard/VT/DRM state | STRONG CANDIDATE, not proven | No stored Cover log; instrument stages and parent restoration |
| GNU timeout foreground group | Separate group around Cover; no foreground option | Can affect console initialization/input | May interact with SDL cleanup | POSSIBLE CONTRIBUTOR; medium source confidence, unknown physical effect | New supervisor preserves group; inspect phase records on Pi |
| Capture ordering | Saved state only after Cover | Does not explain initial nonvisibility | Can restore an already damaged baseline | STRONG CANDIDATE; confirmed source weakness, unproven physical cause | New pre-Cover baseline and both restoration comparisons |
| Restoration errors | One try block silently swallows failures | Not initial Cover visibility | One failed ioctl skips later restoration | POSSIBLE CONTRIBUTOR; source defect confirmed | Independent restore operations plus verification/error records |
| VICE shutdown | F10/Quit/return physically worked on POC3 | Not initial Cover | SDL/console cleanup still possible | UNKNOWN | Run2 exit0/no signal rules out observed crash, not mode damage |
| Menu/dialog/stdin | Visually returns; no postcleanup capture | No direct cause | Foreground/input state unknown | UNKNOWN | Menu `do_wait` snapshot is during launch only; postcleanup PTY/group records needed |
| Cover status suppression | New stdout/stderr/status discarded | Hides failure point | Hides transition evidence | Confirmed diagnostic defect, not confirmed physical cause | Retain structured stage/status/timeout evidence |
| Keyboard/VT before RUN | POC3 works; run2 POC4 works | — | Narrows regression to lifecycle interval | Confirmed owner observation; high | Repeated postreturn keyboard and VT physical checks remain required |

Missing instrumented facts remain unavailable: Cover backend/exit/timeout, original
pre-Cover keyboard/termios, foreground process group, post-Cover comparison and
post-VICE/cleanup capture. Powered-down live state is gone. Do not infer K_OFF,
SIGKILL, SIGTTIN, a stopped renderer, or a particular restore failure from these logs.

## Source corrections and ownership

Product `build/pigen/stage-cbm/files/engineering.py` remains the unprivileged runtime
owner installed by the integration stage. Menu resolves registry/content/flags then
executes its explicit `run-with-cover` interface. This fails closed with older Product
helpers rather than silently mixing incompatible source. There is no second emulator
launch route or privilege change. The private marker controls diagnostic persistence,
not whether terminal protection is used. Diagnostics `snapshot` remains marker-gated.

1. Capture our controlling terminal's termios, keyboard mode, display mode, VT mode,
   tty, session and foreground group **before any Cover child**. Only numeric state,
   never keystrokes, argv or arbitrary environment, is recorded.
2. Spawn Cover in the existing foreground group and sanitized launch environment.
   Keep the existing 2-second whole-process bound, TERM then 0.5-second grace then
   KILL if needed; wait/reap before VICE. No extra presentation sleep or mode switch.
   Record PID, monotonic times, status/signal, timeout/escalation and allowlisted
   renderer stage/backend/dimensions. Raw backend text is intentionally not retained.
3. Restore the pre-Cover baseline before VICE and after VICE. Each restoration is
   independent, so failed keyboard ioctl cannot skip termios. Read back and compare;
   never claim success from a silent ioctl failure. Only our open terminal is touched.
   Restore saved VT_AUTO when originally AUTO; do not transplant another process's
   VT_PROCESS signal ownership. Foreground group is observed, never forcibly assigned.
   BSD kernel-managed PENDIN is excluded from equality, not from the saved restore.
4. Preserve original VICE argv/geometry/ALSA/F10/status. Interruption during Cover or
   audio does not start a new VICE. Cleanup executes even when diagnostics cannot save.
   Final readback and failures are recorded and an unverified-restore warning is shown.
5. Remove launcher's unconditional `stty sane` substitution. Existing unrelated Menu
   legacy terminal commands were not expanded into a new reset strategy.
6. Renderer emits bounded structured stages: initialization, video driver, renderer,
   first submitted presentation, released. It preserves aspect and desktop mode.
   Held RUN key events no longer skip a decorative Cover. This is predictable UX,
   not proof that a key event caused the physical nonvisibility. Cleanup attempts
   every allocated SDL resource even if an earlier destroy call raises.

Host PTY/child tests prove ordering, saved-mode restoration through three cycles,
failure-open behavior, missing renderer, TERM/KILL/reap and parent-signal handling.
They cannot prove physical SDL KMS/VT behavior, actual visible duration, uninterruptible
kernel I/O termination, or a native driver's restoration semantics. Submitted-present
telemetry is not itself a photograph or physical visibility proof.

## First-boot stage and UX corrections

The [earlier audit](poc4-first-boot-ux-findings-2026-09-17.md) retains the old contracts.
New shared Menu presentation library supplies shallow common selections with Advanced
identifier entry; Product catalogs remain validation authority. No US-only default is
committed. Common countries: Australia, Canada, France, Germany, United Kingdom and
United States; English/French/German locale variants are named. Keyboard choices map
to `us`, `gb`, `ca`, `fr`, `de`. Timezones offer named cities and UTC, with Advanced for
all other supported identifiers. Menu text remains English, not translated by locale.

| Stage | Input/purpose | Back, failure and retry | Work, progress and persisted state |
| --- | --- | --- | --- |
| Welcome | Explain local/offline setup and current keyboard | Back/Escape pauses | No mutation |
| Region | Named country/language → locale identifier | Back pauses; keyboard Back revisits | Draft only |
| Keyboard | Named layout | Back → Region; timezone Back revisits | Draft only; new layout applies after reboot |
| Timezone | Named city/UTC → zoneinfo identifier | Back → Keyboard | Draft only |
| Apply region | Validate all three against Product catalogs | Invalid/failure → Region retry | Immediate applying-region/keyboard/timezone infobox; localedef/update-locale/setupcon/timedatectl; region marker after success |
| Owner | Hidden password and confirmation | Back → Region; confirmation Back → password; mismatch retries | Preparing-owner infobox; fixed chpasswd stdin, owner-ready check, marker; no later password-reset API |
| Network | Stay Offline / Ethernet / Wi-Fi | Back → Region without undoing owner enrollment | Configuring-network infobox; setup-network marker; incomplete until final finish |
| Wi-Fi country | Named regulatory country | Back → Network; Escape pauses | Configuring-country/radio infobox; fixed validated raspi-config adapter enables radio |
| Scan/SSID | Supported WPA-personal list | Back → Country; retry/rescan available | Scanning then reading-list infoboxes; no invented percentages |
| Password/connect | Hidden input, explicit non-display explanation | Back → scan; failure → password retry, alternate SSID, country or Offline | Connecting infobox; existing stdin → fixed root-only NM credential file; NM activation wait up to30s |
| Finish | Save preferences and completion | Failure → Network retry; completed setup republishes readiness only | Saving-preferences/configuration infoboxes; setup-finish only after chosen path completes |

Already committed region/network changes can be revised while setup is incomplete;
Back does not claim rollback. Owner enrollment is never repeated/reset once its marker
exists. Interrupted Wi-Fi setup resumes at Network for an explicit choice, not an
accidental finish caused by a lost shell flag. Only three fixed setup-Wi-Fi operations
are admitted, after region/owner/network markers and a verified owner credential.
They retain network readiness/catalog/credential boundaries. SSH/services and other
ordinary configuration remain gated until setup-finish. No broad setup bypass exists.

No physical operation-duration measurements exist. Synthetic tests verify working
feedback precedes the backend and simulate failures, not Pi speed. Linux compound
configuration commands now share a 65-second budget beneath the 75-second client
bound; each subprocess remains capped at60s, NM connection wait at30s, scan-cache
read at8s. Filesystem I/O itself has no hard real-time guarantee. Timeouts may leave
partial applied state and are reported as unconfirmed/retryable, not rolled back.

Password input uses the existing hidden widget with explicit explanation; no character
masking flag was adopted after safety review rejected that proposed option, including
a retry citing the [upstream dialog manual](https://invisible-island.net/dialog/manpage/dialog.html).
That manual documents `--insecure` as asterisk feedback (length exposure), not cleartext;
the exact option remains approval-blocked and was not bypassed. Secrets
are not echoed or put in child argv, logs, result text, diagnostics or extra files.
WPA-personal printable ASCII 8–63 characters, including spaces, punctuation and
backslashes, retains its existing contract; no evidence condemns special characters.
Synthetic transport/keyfile tests do not prove radio authentication. The original
failed credential is unknown and was neither requested nor reconstructed.

New fixed `wifi_country_required` / `wifi_failed` results give actionable retry
guidance without echoing backend errors. They do **not** claim authentication failure:
the bool-returning adapter cannot distinguish bad password, signal or router failure.
Malformed scan responses are rejected atomically before any partial SSID menu is used.

## Next candidate and physical qualification

No next version/tag/hash is assigned. Include both repositories' source-correction
commits listed in the related checkpoint change inventory and CURRENT-STATE.
Rebuild/version **project-cbm-runtime** (setup/backend/results) and **project-cbm-menu**
(launcher, renderer, shared setup UI, first-run/config UI). Refresh Product integration
archive/stage/recipe hash for the lifecycle owner; refresh request/result schemas,
Menu manifest/install payload and native/offline validation inputs. Existing Cover
artwork, profile registry, VICE 3.10-1+pcbm3, TCPser and optional-content packages are
reusable unchanged if retained hashes/rights still satisfy the next lock. Do not consume
arbitrary Menu main. The old attempt-3 Cover validator remains historical; next-candidate
validation must explicitly inspect the new lifecycle owner/phase files and interface.

Before a future freeze: complete matching-source host suites, native Linux PTY/signal
and actual SDL cleanup/timeout tests, real installed dependency/package/schema/privilege
checks, locale/layout/timezone catalog checks, NetworkManager keyfile parsing with
synthetic punctuation/space credentials, first-boot resume/readiness and offline checks.
No new package was constructed here to perform those installed/native checks.

Then follow the [unbound physical regression draft](poc4-next-candidate-regression-draft.md):
prelaunch VT roundtrip; correct default/profile/content Cover; visible bounded aspect-
preserving presentation; VICE geometry/keyboard/F10/Quit; **immediate Menu keyboard and
postreturn VT roundtrip**; second and third cycles; collect every new phase record.
Run all four original qualification-media programs/disks, audio and available joystick.
Fresh-card setup must test every named stage, Back/change, Escape/resume, invalid input,
failed connection/password retry, alternate SSID/country, Offline, actual elapsed times,
completion and reboot without unexpected rerun. Do not bind this draft to nonexistent
candidate hashes or mark READY TO FLASH.

SID-Wizard use/save/relaunch, StrikeTerm use/return, physical USB import, Wi-Fi reconnect,
external Samba, SSH enable/connect/disable, TCPser end-to-end, mDNS, Advanced Mixer,
preferences/direct-boot/service persistence remain UNTESTED unless exact separate
evidence establishes otherwise. Presence and source tests are not functionality passes.

Dosbian principles used: presentation does not own emulator lifecycle, bounded lifetime,
explicit terminal ownership, truthful working feedback and recoverable configuration.
No Dosbian code copied, no MEDIA/TOOLS/POWER/recovery redesign, no boot presentation,
PSID/RSID playback, additional Pi model, broad privilege or rights change.

## Validation, refs and recovery

The first recovery-script run at `archive/poc4-run2-source-correction-2026-09-17`
is preserved **incomplete, not sealed**. Its private archive umask077 propagated
to a permissions test that expects normal umask022, causing an additional fixture
failure; no integrity mismatch or runtime-source defect was established. The distinct
`-verified` checkpoint supplies explicit test umask022 while retaining private output
permissions. Both test outcomes remain evidence; no candidate/build retry occurred.

Final retained host results: Product 155 tests, 154 PASS and one unchanged contextual
macOS `test_mktemp_regression` FAIL (the earlier baseline has the same failure);
Menu 70/70 PASS. Nine focused lifecycle tests pass. The unprivileged macOS sandbox
previously passed153 Product tests before the final two additions; do not conflate
that run with the retained unsandboxed run. ShellCheck unavailable; Bash syntax,
Python AST/JSON, links, diff/secret review pass. No native Linux installation or
actual radio test was executed in this slice. Test logs record exact elapsed suite
time, not physical first-boot operation time.

Final suite totals, exact logical commits, clean branch status, manifest hash and
offline restoration results are retained in the related external checkpoint
`archive/poc4-run2-source-correction-2026-09-17-verified`. It contains both Git bundles,
refs/peeled tags/fsck, source-change inventories, this documentation, validation logs,
run2 evidence references and hashes for preserved POC3/POC4 artifacts. Images are
referenced, not duplicated. The preceding checkpoint remains unchanged. Independent
encrypted backup/custody is still unresolved.

**One next owner action:** review the defensive source corrections and remaining
physical uncertainties, then authorize a separately versioned next-candidate milestone.
This report does not claim that either physical root cause is proven or that the next
candidate will pass. Stop before packages, tags, input freeze, image build or physical test.
