# User preferences and machine profiles

Implemented foundation only, 2026-09-16. Existing POC Menu/launcher/boot paths still
read their existing configuration. This slice does not migrate those consumers or
change any frozen image. New preferences are explicit desired values, not evidence
that an existing session applied them.

## Location, format and defaults

Canonical user location:
`$XDG_CONFIG_HOME/project-cbm/preferences.json`, falling back to
`~/.config/project-cbm/preferences.json` when XDG_CONFIG_HOME is missing or relative.
No user/machine-specific absolute path is embedded. Root writes are refused.

```json
{
  "schema_version": 1,
  "default_machine": "x64sc",
  "boot_preference": "menu"
}
```

[Schema](../../schemas/preferences.schema.json). The default machine comes from the
registry's single recommended profile. Boot preference is `menu` or `emulator`;
changing it here does **not** change a service, autologin or the current boot path.
No hostname, credentials, listener settings or arbitrary commands belong in this file.

Read operations never create directories, files or locks. Valid user data overrides
these foundation defaults. Missing data returns `status: default`; malformed,
unsupported-schema, unsafe-permission or unreadable data returns `status: invalid`
with safe defaults. The invalid file stays intact and no silent migration occurs.
The caller must distinguish this fallback from a successful saved preference.

## Try the source command

Use a disposable development-user configuration directory, never a frozen candidate:

```sh
./runtime/bin/pcbm-preferences show
./runtime/bin/pcbm-preferences set default_machine xvic
./runtime/bin/pcbm-preferences set boot_preference menu
```

These are intentional writes to the invoking user's preferences. Do not run with sudo.
`show` emits JSON with status/source/values and succeeds even if it reports invalid
state. `set` emits the saved values only after validation and commit; errors exit 2
with a sanitized explanation. These CLI exit codes are not dialog exit codes and
must not be fed directly into the UI Back/Cancel mapping.

If a malformed file needs recovery, inspect/back it up locally and explicitly run:

```sh
./runtime/bin/pcbm-preferences recover --confirm
```

For bounded malformed content, this retains its original bytes in a private
`preferences.invalid.<unique-id>.json` companion before replacing it with defaults.
A valid file is unchanged in meaning. Unknown schema versions are never automatically
downgraded. Oversized files and unsafe ownership/permissions/symlinks require manual
local recovery, not automatic overwrite. Backups may contain whatever the malformed
file contained; keep them private. No automatic backup deletion is performed.

## Atomic updates and ownership

The application directory must be owned by the current user with mode 0700; data and
lock files must be regular, user-owned, single-link, mode 0600 files. Final directory/
file symlinks are refused. Do not use shared/untrusted configuration directories.
Ancestor directory control remains the ordinary user's OS responsibility; this is
not a security boundary against malicious code already running as that same user.

A nonblocking advisory lock serializes cooperating writers. The writer reads and
validates current data under the lock, merges allowed changes, writes a private
same-directory temporary file, flushes it, atomically replaces the destination and
flushes the directory. Temporary files are cleaned after errors. Before replacement,
a failed write leaves the previous file intact. A failure during final durability
confirmation may mean replacement already happened: read state before retrying.
Power-loss guarantees still depend on filesystem/storage behavior and need Linux/
physical interruption tests. No such qualification is inferred from mocked failures.

## Migration and future consumer work

Historical/current `/etc/pcbm/default-machine.conf` is a literal profile ID;
`boot-mode.conf` uses `menu`/`machine` with historical case variants. They are read as
data, never sourced. `pcbm-info` reports them separately from this new foundation;
effective boot behavior is not inferred from a file that the POC session bypasses.

A later authorized slice should switch each consumer to one shared preference reader,
import validated legacy values once, map `machine` to `emulator`, retain a migration
record/backup, and avoid overwriting an existing valid user file. The product session
and Menu must agree on that transition before boot preference is advertised as active.
No automatic import or privileged writeback is implemented here. VICE continues to
own emulator resources/saved preferences; do not duplicate them in this file.

## Machine-profile registry

[profiles.json](../../runtime/data/profiles.json) is the new authoritative registry
for these consumers, validated against the [schema](../../schemas/machine-profiles.schema.json)
and semantic checks. It covers all 11 existing profile IDs: x64, x64sc, xscpu64,
x64dtv, x128, x128-80col, xcbm2, xcbm5x0, xvic, xplus4, xpet.

Fields are stable ID, name, description, executable basename, video chips,
recommended flag and a tightly constrained launch-options list. Only x128-80col
uses `-80col`; all other lists are empty. Exactly one profile is recommended; IDs are
unique. No paths, shell fragments, downloadable plugins or user executable overrides.
The registry describes launch metadata, not physical qualification or a claim that
all machines/standards have identical geometry.

`pcbm-info` and preferences consume this registry now. Existing Menu/launcher mappings
remain frozen-compatible code until the next targeted migration; they do not read
this file yet. Tests require exact current coverage and schema/default agreement.
Content categories/format compatibility are intentionally deferred rather than encoded
as unverified capabilities. Adding a profile requires source/package/resource review,
registry/schema/tests and appropriate qualification; it is not a dynamic plugin feature.
