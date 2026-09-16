# Project CBM runtime foundation

This source implements `pcbm-info`, the user-preference foundation and the initial
machine registry. It is **not installed into POC1, POC2 or POC3**. No image or package
was built for this slice; existing Menu/boot consumers are deliberately unchanged.

From the product checkout (Python 3.11+; standard library only):

```sh
./runtime/bin/pcbm-info
./runtime/bin/pcbm-info --json
./runtime/bin/pcbm-preferences show
```

Do not use sudo. Information collection is read-only and creates no preference files
or Python bytecode. On a Mac or ordinary Linux development machine, missing Raspberry
Pi/Project CBM interfaces produce unknown values, not invented Pi data.

- [User guide](../docs/runtime/pcbm-info.md)
- [Information contract](../docs/runtime/info-contract.md)
- [Preferences/registry](../docs/runtime/preferences.md)
- [Implementation checkpoint and tests](../docs/runtime/foundation-slice.md)

## Future installation boundary (not performed here)

A future product integration package/stage should install only `bin/`, `project_cbm/`
and `data/` beneath `/usr/share/project-cbm/runtime/`, root-owned, directories 0755,
Python/JSON files 0644 and entry points 0755. Create command symlinks:

- `/usr/bin/pcbm-info` → `/usr/share/project-cbm/runtime/bin/pcbm-info`
- `/usr/bin/pcbm-preferences` → `/usr/share/project-cbm/runtime/bin/pcbm-preferences`

Entry points resolve their own location, so a relocated staged copy works without
PYTHONPATH or hard-coded operator paths. The interpreted Python modules are runtime
code; tests, benchmark fixtures, development requirements, full schemas and repository
history must not be copied into the appliance. No Python package manager is needed
at runtime. The product package should depend on python3 (>= 3.11); it does not depend
on dialog. Read-only dpkg-query/systemctl queries use existing Debian/systemd utilities
and degrade gracefully if unavailable. User preferences stay outside vendor files.

Factory consumption/versioning is a subsequent bounded change: retain the exact
source, package and registry identities in new inputs. Never rebuild/retag a frozen
Menu or product input under its old identity. Do not silently add this directory to
an existing frozen release lock or finished image.
