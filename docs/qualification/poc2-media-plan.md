# Proposed tiny qualification-media bundle

2026-09-15. **Proposal only. Nothing acquired, generated, embedded or hashed.**
Authorization is required before producing media or POC2. It would be misleading
to call nonexistent files known-good or supply invented SHA-256 values.

## Recommendation and scope

Choose **C: a separately versioned qualification input injected by the controlled
image build before freezing**, enabled only for private engineering/qualification
profiles initially (A for delivery). Exclude it from normal public releases.
Public examples/diagnostics (B) can be reconsidered after demonstrated user value
and license review; they are not needed to diagnose this failure. Never copy files
onto an already frozen candidate and keep its old identity.

Prefer new, short, Project CBM-owned programs rather than acquiring scene/game/
music files. Use ordinary CONTENT categories and the current x64sc autostart path,
not a separate test launcher. Proposed initial payload budget: less than 200 KiB;
this is not an SD-card requirement.

| Proposed name | Author/source/version | Rights / SHA-256 status | Normal path and purpose |
| --- | --- | --- | --- |
| pcbm-smoke.prg | Future Project CBM contributors; repository qualification/media; proposed 0.1.0 | Explicit standalone MIT license proposed; not yet authored/licensed; SHA-256 pending | programs/qualification: load/run simple BASIC text/checks, about 1–2 KiB |
| pcbm-sid-check.prg | Same original source/version, no borrowed tune | Same pending license/hash | music/qualification: short original SID voice/tone sequence with on-screen expectations, about 2–4 KiB |
| pcbm-video-input.prg | Same original source/version | Same pending license/hash | demos/qualification: color/moving pattern, frame counter, keyboard and joystick state, about 4–8 KiB |
| pcbm-check.d64 | Deterministically generated from the same owned source; same bundle version | Same pending license/hash; generator/tool identity also required | programs/qualification: standard 35-track 174,848-byte disk, directory and contained smoke-program load |

Paths are beneath /home/pi/pcbm. No ROM, existing game, scene artwork or existing
music composition would be bundled by this proposal. A source repository license
must not be assumed to license unrelated media. Explicit author/license review
is required even for these proposed new files.

The current content filter includes PRG/SID/D64, but pcbm_launch_content passes
content to the selected emulator's `-autostart`; it does not demonstrate a PSID/
RSID player route. The proposed SID PRG tests C64 SID sound and the Music browser,
**not** PSID/RSID file playback. Do not expand POC2 with an unqualified music-player
subsystem. A desirable existing SID/demo with unclear rights must remain an
optional owner-supplied local qualification artifact, with separate provenance
and test identity, never silently embedded. No such external artifact is selected.

## Gates before a file becomes a declared input

1. Author/review small source, explicit redistribution license and author credits;
   record authoritative repository URL/path and exact commit/version. Pin any
   assembler/tokenizer/disk generator and its license/source.
2. Generate deterministically outside the appliance; inspect outputs and expected
   behavior in an independently known-working reference environment. Record that
   reference identity and results. A test file running only in the candidate under
   investigation is insufficient evidence that it is known-good.
3. Record actual per-file SHA-256, byte length, source revision, license/reference,
   purpose, expected display/sound/input result and permitted redistribution.
   Disk contents must have the same declared program identities.
4. Freeze an archive and per-file provenance/license manifest, retain source/tools/
   outputs externally, and verify every digest before integration. Add an explicit
   optional qualification-media input to a versioned release-lock contract with
   positive/negative fixtures; do not rely on an undocumented side-copy operation.
5. Bind the new lock, engineering profile and resulting image hash to qualification.
   Image minimal identity can reference the lock/build ID; full recovery records
   remain outside the image. No self-referential image hash in the input lock.
6. Validate category discovery, normal launch, disk autostart/directory handling,
   expected F10 return and license-file placement. Then qualify physical Pi 3B
   display, audible SID output and keyboard/joystick separately. Lack of a joystick
   is UNTESTED, not a fabricated pass or a media failure.

Until these gates are met the table is a design, not a checksum manifest or an
approved distributable payload. The immediate [POC1 report](poc1-pi3b-analysis.md)
therefore recommends authorization to create and validate it before POC2 freezing.
