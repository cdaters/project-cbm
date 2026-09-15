# Milestone 1 input and installed-identity contracts

Status: implemented host-only contract foundation, 2026-09-15. No real release lock,
component package, builder, first boot or image exists. ADR-0001 remains authoritative.
The [old worksheet](../recovery-contract.example.json) is historical design, deliberately
rejected by the new validator. Schema 1 below supersedes its field layout; this is
not a migration of an existing released schema.

## Running the checks

Use Python 3.11+ and the exact dependencies in
[requirements-contracts.txt](../../requirements-contracts.txt). Python 3.14.5 on macOS
was tested. Use an isolated environment; these dependencies are not image packages.
Retain platform-specific wheels and their hashes externally for offline restoration.
The implementation uses the standard [JSON Schema 2020-12 vocabulary](https://json-schema.org/draft/2020-12)
through jsonschema, plus focused semantic checks, not a custom schema engine.

```sh
python -m unittest discover -s tests -v
python tools/build_contracts.py validate tests/fixtures/release-lock.synthetic.json --allow-fixture
python tools/build_contracts.py identity tests/fixtures/release-lock.synthetic.json --allow-fixture
```

`identity` writes JSON to stdout only. Rejected inputs produce no identity and exit 2.
Do not redirect output onto the lock. Tool commands never fetch, execute a recipe,
mount, install, build or provision anything. No pcbm-info command was implemented.
The tests run without network after dependencies are available.

## Input lock, schema 1

[Release-lock schema](../../schemas/release-lock.schema.json) and
[synthetic fixture](../../tests/fixtures/release-lock.synthetic.json) are human-inspectable JSON.
The fixture uses `.invalid` URLs and invented digests, is marked `fixture: true`, and
requires `--allow-fixture`. It is never an input candidate. No production lock has
been created. Real locks must use `fixture: false` and verified retained input bytes.
Flipping that flag cannot authenticate inputs; schema validation is not provenance.

| Group | Required inputs |
| --- | --- |
| Product/integration | Independent product version and candidate name; arm64; exact product Git commit, ref, public origin and retained source bytes |
| Base | Lite/Trixie generation and release identity; exact pi-gen Git commit/source; ordered stages; config and patches; authenticated APT metadata; binary and source closure catalogs |
| Components | VICE/Menu/TCPser independent version; public source origin and checksum; source Git identity where applicable; exact package name/version/architecture/checksum; build recipe/options/ordered patches; predecessor component build record; corresponding source |
| Menu | `source.git.ref` is `refs/tags/v<VERSION>`; `source.git.commit` is the **peeled commit**; `tag_object` is the annotated tag object or null for a lightweight tag; source artifact hash is mandatory |
| Configuration | Schema version; defaults; assets/license inventory; sealing and first-boot recipe identities |
| Build | Environment contract version 1; exact environment recipe/bootstrap/host dependency closure/toolchain; source-date epoch; reproducibility policy |

Current Git IDs use full 40-character SHA-1 object IDs; artifact checksums are
separate SHA-256 fields. Short/moving commit values fail. Exact Git tag-to-commit and
package-file metadata verification against retained repositories/.debs belongs to
acquisition/packaging implementation; current tests check the declared relationships.
Never treat tag spelling alone as proof of a matching commit. Source URL queries,
credentials, fragments and non-HTTPS schemes fail; source availability is not fetched.

Each artifact has a portable relative `path`, positive `size_bytes`, lowercase
64-hex `sha256`. Absolute/traversal/ambiguous locators and conflicting identities for
one locator fail. `validate LOCK --artifact-root ROOT` additionally checks each
**directly declared file's** size/hash offline and refuses escapes through symlinks.
Only use trusted, quiescent retained roots; this is not a sandbox for hostile concurrent
filesystem mutations. Nested closure catalogs must eventually be walked and verified
by acquisition tooling; their formal formats/readers are still incomplete. A passing
lock schema alone does not prove transitive closure, licenses or authentication.

Package names are project-cbm-vice (arm64), project-cbm-menu (all), and
project-cbm-tcpser (arm64). Version consistency is checked as
`package.version = package.upstream_version + '-' + package.revision`.
Upstream identity is preserved (e.g. TCPser `1.1.6_beta`); `_` maps to Debian `~`
in `package.upstream_version`. Further version schemes require an explicit contract
extension. The initial VICE gate is 3.10, with SDL2 and ALSA configure options;
actual option acceptance and dependency closure must be checked during package work.

## Freeze order and acyclic checksums

1. Retain source/config/build recipes, bootstrap/toolchain and dependency inputs.
2. Build/verify components externally. Produce package artifacts and component build
   records. Their hashes are **known predecessor inputs** to image assembly.
3. Freeze the lock only after all required hashes are known. Unknown package hashes
   belong in planning notes, not nullable fields accepted as a frozen lock.
4. Hash exact saved lock bytes. Generate installed identity from those bytes.
5. Assemble and seal an image; only afterward produce final image hashes, image build
   records, qualification and release publication metadata externally.

The integration commit must precede the lock: a committed lock cannot identify its
own containing commit. No final image, qualification, final manifest or self-hash
field is accepted in the lock. No final-image/final-manifest digest is accepted in
installed identity. External provenance binds those outputs later. This is structural
cycle prevention, not a completed validator for the future external attestation graph.

JSON reader rules: UTF-8, no BOM, duplicate keys, non-finite numbers or floating-point
numbers; one MiB input ceiling. Unknown fields/schema versions fail validation.
Writer: ASCII-escaped UTF-8, sorted object keys, two-space indentation, stable array
order, final LF. Hash exact saved bytes, never parsed/reformatted equivalence. Additional
whitespace changes the build ID. Schema readers remain external and are retained by version.

## Minimal installed identity

[Installed-identity schema](../../schemas/installed-identity.schema.json) describes
`/usr/share/project-cbm/identity.json`: root-owned 0644, installed once during image
construction. It is a package/integration-owned support record, not user configuration.
This follows the [Debian filesystem policy](https://www.debian.org/doc/debian-policy/ch-files.html)
for installed data; `/etc/os-release` remains the upstream authority for OS details.
The future pcbm-info command reads this record without maintaining another version source.

The projection includes product/candidate, architecture, integration commit, base
identity/pi-gen commit, component versions/package versions and package hashes,
configuration schema, and full lock SHA-256 as build ID and external manifest lookup.
A fixture marker ensures test output remains visibly synthetic. Lookup is an ID,
not a network requirement or final-manifest digest. The checked fixture is under 4 KiB.
No source trees, lock, archive locators, recipes, build logs, host names/paths, keys,
credentials, qualification, package closure or schemas are installed merely for recovery.
Unknown/private fields fail the identity allowlist. All full records remain external.

This immutable-by-policy base identity does not certify live apt updates or resist a
privileged edit on writable ext4. First boot must not rewrite it. Offline support reads
it through an ordinary Linux/ext4-capable reader, without boot, network or proprietary tools.

## Bulk workspace guard

[Workspace schema](../../schemas/workspace-config.schema.json) is an **operator-local**
contract. It carries `mountpoint`, `workspace`, `workspace_id`, and an operation-specific
positive `minimum_free_bytes`; absolute machine paths never enter release locks.
The configured workspace must already exist below a real mounted volume on the same
filesystem, without symlink/`..` aliases, and contain a regular marker file
`.project-cbm-workspace.json` with only its expected `workspace_id`. The tool checks
space and fails closed. It creates nothing and never falls back to /tmp or ~/Code.

The marker is a continuity identifier, not cryptographic volume authentication. The
operator must verify the actual external volume/path before registration. No marker
was installed on TheBench in this phase; the future registration/bootstrap step
requires the owner-approved host/storage plan. Tests inject mount observations using
small temporary fixtures; they do not claim a provisioned Linux build workspace.

A future launcher must run this guard before download, VM creation/start or every
large build, then separately check guest ext4 semantics and free space. The guard is
not a space reservation and cannot prevent hot-unplug or races; recheck at stage
boundaries, stop on I/O failure and never silently relocate work. APFS hosts virtual
disk files and archives; it does not become a suitable Linux rootfs through this check.
