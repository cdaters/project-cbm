# Validation and qualification

## Safe checks for continuity/source work

- Run `git diff --check` and inspect staged paths/sizes and diff. Validate added
  JSON and local documentation links. Scan new files for private keys, token shapes,
  password hashes and accidental history/identity material without printing contents.
- Syntax-check each shell file individually. In project-cbm-menu:

  ```bash
  for f in scripts/pcbm-* packaging/*.sh; do bash -n "$f" || exit; done
  ```

  Syntax checks do not execute the scripts. Use ShellCheck when available and
  distinguish existing findings from regressions. It was unavailable in this phase.
- Never use an installer, docs-sync, release-prep or hardware/service command as
  a harmless static check. No installer, packaging build or runtime was run here.
- For runtime work, add focused tests for relevant launcher, service, mount,
  error/cancel, config and packaging/version behavior. The old CI only packages ZIPs.

## Preservation verification

`tools/preservation-inventory.py verify MANIFEST.json` reads the recorded tree
and detects changes/loss/additions in file bytes, paths/types, modes, mtimes and
xattr hashes, without following symlinks. It does not promise ACL/ownership/atime
preservation. Detailed manifests are private external records, not publication inputs.
Anchor hashes are in [preservation-manifests.json](preservation-manifests.json).
Use the recorded script against historical, retained-audit and prior-audit-records
manifests on TheBench; do not regenerate a baseline to hide a mismatch.

Git bundles must pass `git bundle verify`; complete before-local .git archives also
retain reflogs/config/unreachable objects. Check existing tag objects/peeled commits
against [provenance](provenance.md). Recovery blob hashes must match all 17 original
image extracts. Full verification results are recorded in the external phase archive.

## Hardware policy and matrix

Retain the full [audit hardware and comparison matrix](audit-2026-09-15.md#j-hardware-and-qualification-matrix).
It covers Pi 3B, 3A+ (512 MiB), 3B+, 4B, 400, 5, 500 and 500+. All remain
unqualified by this work. Pi 3 is the performance floor; do not silently use x64
instead of x64sc to hide a regression. CM/Zero models are not automatically added.

Compare exact 1.0.0 Trixie against frozen 1.1 candidates with equivalent hardware,
power, cooling, display, storage and licensed content. Record image hashes, board
revision/RAM, EEPROM/kernel/firmware, VICE config, display/audio/controller identity
and throttling. Separate first boot from steady state; use >=10 boot/launch runs,
median and worst case. The audit's tentative thresholds are review triggers, not
measured guarantees. Measure Pi 3 RAM/swap and audio continuity early.

Qualify boot/expansion/offline operation, VICE machines/media, graphics/audio/input,
USB import, storage types, service/credential policy, IP232, power, backup/restore,
two-flash identity and release integrity. Keep per-candidate results in
/Volumes/TheBench/ProjectCBM-Work/qualification and commit small summaries here.
No physical tests were performed during audit or preservation.

## Black-box recovery acceptance

The [recovery test matrix](recovery.md#8-acceptance-tests-and-current-evidence) adds
context-free handoff, offline bundle restore, mounted-image identity, lost-builder/
upstream reconstruction, metadata agreement, privacy negatives, old-schema reading,
qualification binding, hash-cycle rejection, relocation and independent-backup drills.
A build passing syntax checks does not meet these gates. The accepted preservation
bundles passed the actual offline all-ref/17-script restore test in this design pass.
No 1.1 image/schema/runtime test is claimed; those components do not exist yet.
Keep PASS/FAIL/UNTESTED/BLOCKED and exact candidate/test-suite identity in records.
