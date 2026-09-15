#!/bin/bash
set -Eeuo pipefail
: "${CBM_KIT:?frozen kit required}" "${CBM_RELEASE_LOCK:?lock required}" "${CBM_RECIPE_DIR:?recipe required}"
python3 "$CBM_RECIPE_DIR/tools/install_poc_stage.py" "$CBM_RELEASE_LOCK" "$CBM_KIT" "$ROOTFS_DIR"
