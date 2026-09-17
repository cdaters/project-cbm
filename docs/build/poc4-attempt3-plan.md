# POC4 attempt #3: integration plan

Owner authorization: one new private candidate after the
[bounded actual Combian V3.7 review](../design/combian-v37-bounded-review.md).
Do not physically test attempt #2. It remains immutable pre-Cover evidence.

## Identity and package reconciliation

Use **Project CBM 1.1.0-poc.4 / private-engineering-poc4, attempt 3**. The existing
factory already represents attempts separately, and the owner permits that convention.
This remains the same first-boot/runtime activation milestone, now including Covers;
it is not a beta, RC, public release or identical-input rebuild. A new integration
commit/lock digest and distinct `private-poc4-attempt-3` work/artifact paths distinguish
it. Never overwrite attempt #1/#2, their locks or output. Menu is independently
versioned **1.1.0_poc4.1**, new annotated tag `v1.1.0_poc4.1`, Debian
`project-cbm-menu 1.1.0~poc4.1-1+pcbm1 / all`, dependency `project-cbm-runtime-api (= 1)`.

Only Menu payload changed: seven exact Covers, renderer/shared launcher, Advanced
Mixer and import destination feedback. Product runtime/data and runtime package
recipe are byte-unchanged from their recorded source commit; reuse runtime
`1.1.0~poc4-1`, VICE `3.10-1+pcbm3`, TCPser `1.1.6~beta-1+pcbm1`. First-boot/stage
payload, geometry, optional software, qualification media, base/host package closures
and pi-gen/environment patches remain unchanged. The asset inventory now declares
private Covers with provenance limits. Standard mc/mc-data and alsa-utils already
exist in the frozen Debian closure; no new dependency acquisition is needed.

The Menu build record explicitly retains Cover manifest/renderer/wrapper/launcher/
registry descriptors plus seven asset objects and mc/mc-data/alsa-utils package
identities. The schema-4 lock references this record; no circular output hashes.
The integration source tar, new Menu source archive, Debian source/buildinfo and
packages remain retained outside the appliance.

## Sequence

1. Verify mounted bulk storage and guest ext4 headroom. Run pinned host-drift guard.
2. Test source fixtures and build exact tagged Menu with standard Debian tooling.
3. In a NEW disposable native target: install packages, verify dpkg/APT/AppArmor and
   sudoers, first-boot/owner/service/backend behavior, synthetic USB import, actual
   standard utilities and installed headless SDL Cover lifetime. Never archive credentials.
4. Repeat the actual invalid-TMPDIR/AppArmor regression on a NEW copy of failed-stage
   root; preserve sanitization and security. Do not weaken a failing package check.
5. Archive the committed integration as `inputs/project-cbm-integration-poc4-attempt3.tar`.
   Run `tools/freeze_poc4_covers.py WORKSPACE RECIPE INTEGRATION_COMMIT MENU_COMMIT TAG_OBJECT`.
   It verifies attempt #2 then creates `inputs/frozen-poc4-attempt3`, changing only the
   declared new inputs. Retained objects can be hard-linked; never edited in place.
6. Verify new kit, host state, and construct once with `construct_poc.py ... --attempt 3`
   inside the established isolated network namespace, using the sanitized environment.
7. Run complete read-only image, filesystem/unit/ELF, activation and Cover validators;
   compare raw/XZ; measure footprint; verify historical/prior-attempt preservation.
8. Bind a new Pi 3B procedure to exact hashes, retain source/bundles/evidence and verify
   offline restoration. Stop for owner physical testing; no additional build or push.

Native namespace results are not Pi radio, KMS/VT, ALSA hardware or C64 application
qualification. Boot optimization remains deferred. StrikeTerm public rights remain
pending; reference SID/demo content is not bundled; proper PSID/RSID playback is deferred.
