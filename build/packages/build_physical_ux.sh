#!/bin/bash
# Build only the changed runtime/Menu packages in a NEW candidate workspace.
set -euo pipefail
recipe=$(realpath "${1:?integration recipe}")
w=$(realpath "${2:?guest bulk workspace}")
[[ $(uname -m) == aarch64 && $(findmnt -T "$w" -no FSTYPE) == ext4 ]]
[[ $(df --output=avail -B1 "$w" | tail -1) -gt $((40*1024**3)) ]]
out="$w/packages/poc4-attempt6"
mkdir "$out"
mkdir "$out/product"
tar -xf "$w/inputs/project-cbm-integration-poc4-attempt6.tar" -C "$out/product"
mv "$out/product/project-cbm" "$out/runtime"
rmdir "$out/product"
tar -xf "$w/inputs/project-cbm-menu-1.1.0_poc4.4.tar" -C "$out"
mv "$out/project-cbm-menu-1.1.0_poc4.4" "$out/menu"
cp -a "$recipe/build/packages/runtime/debian" "$out/runtime/debian"
export SOURCE_DATE_EPOCH=1789513200 TZ=UTC LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
for name in runtime menu; do
  version=$(cd "$out/$name"; dpkg-parsechangelog -S Version)
  upstream=${version%-*}
  tar --sort=name --mtime="@$SOURCE_DATE_EPOCH" --owner=0 --group=0 --numeric-owner --anchored --exclude="$name/debian" -C "$out" -cf - "$name" | gzip -n > "$out/project-cbm-${name}_${upstream}.orig.tar.gz"
  (cd "$out/$name"; dpkg-buildpackage -us -uc -sa) > "$out/$name-build.log" 2>&1
  printf '%s source and binary package build completed\n' "$name"
done
sha256sum "$out"/*.deb > "$out/package-sha256sums.txt"
cat "$out/package-sha256sums.txt"
