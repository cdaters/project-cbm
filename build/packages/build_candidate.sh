#!/bin/bash
# Build only the changed runtime/Menu packages in a NEW candidate workspace.
set -euo pipefail
recipe=$(realpath "${1:?integration recipe}")
w=$(realpath "${2:?guest bulk workspace}")
[[ $(uname -m) == aarch64 && $(findmnt -T "$w" -no FSTYPE) == ext4 ]]
[[ $(df --output=avail -B1 "$w" | tail -1) -gt $((40*1024**3)) ]]
attempt=${3:?new attempt number}
menu=${4:?Menu source version, e.g. 1.1.0_rc1}
selection=${5:-runtime-menu}
[[ $selection == runtime-menu || $selection == runtime-vice || $selection == runtime-menu-vice ]]
[[ $attempt =~ ^[1-9][0-9]?$ && $menu =~ ^1\.1\.0_(poc4\.[0-9]+|rc[0-9]+)$ ]]
out="$w/packages/poc4-attempt$attempt"
mkdir "$out"
mkdir "$out/product"
tar -xf "$w/inputs/project-cbm-integration-poc4-attempt$attempt.tar" -C "$out/product"
mv "$out/product/project-cbm" "$out/runtime"
rmdir "$out/product"
if [[ $selection != runtime-vice ]]; then
  tar -xf "$w/inputs/project-cbm-menu-$menu.tar" -C "$out"
  mv "$out/project-cbm-menu-$menu" "$out/menu"
fi
cp -a "$recipe/build/packages/runtime/debian" "$out/runtime/debian"
export SOURCE_DATE_EPOCH=1789513200 TZ=UTC LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
components=(runtime)
[[ $selection == runtime-vice ]] || components+=(menu)
for name in "${components[@]}"; do
  version=$(cd "$out/$name"; dpkg-parsechangelog -S Version)
  upstream=${version%-*}
  tar --sort=name --mtime="@$SOURCE_DATE_EPOCH" --owner=0 --group=0 --numeric-owner --anchored --exclude="$name/debian" -C "$out" -cf - "$name" | gzip -n > "$out/project-cbm-${name}_${upstream}.orig.tar.gz"
  (cd "$out/$name"; dpkg-buildpackage -us -uc -sa) > "$out/$name-build.log" 2>&1
  printf '%s source and binary package build completed\n' "$name"
done
if [[ $selection != runtime-menu ]]; then
  # The unchanged authenticated upstream source is pinned by the established recipe.
  python3 - "$recipe/build/inputs-poc.json" "$w/inputs/vice-3.10.tar.gz" <<'PY'
import hashlib,json,sys
from pathlib import Path
pin=json.loads(Path(sys.argv[1]).read_text())['vice']
assert hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest()==pin['sha256']
PY
  cp "$w/inputs/vice-3.10.tar.gz" "$out/project-cbm-vice_3.10.orig.tar.gz"
  tar -xf "$out/project-cbm-vice_3.10.orig.tar.gz" -C "$out"
  cp -a "$recipe/build/packages/vice/debian" "$out/vice-3.10/debian"
  (cd "$out/vice-3.10"; DEB_BUILD_OPTIONS=parallel=6 dpkg-buildpackage -us -uc -sa) > "$out/vice-build.log" 2>&1
  printf 'vice source and binary package build completed\n'
fi
sha256sum "$out"/*.deb > "$out/package-sha256sums.txt"
cat "$out/package-sha256sums.txt"
