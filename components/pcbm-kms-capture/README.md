# Project CBM KMS capture component

GPL-2.0-only, separately built and packaged from MIT Project CBM Runtime.
Technical starting point: Paul Cercueil's kmsgrab, commit
`d4c6061a59f4b7ecb6b39f96c7d39a5d5f48b702`,
https://github.com/pcercuei/kmsgrab . Exact reviewed upstream files are retained in
`upstream/`, with original notices; COPYING contains GPL version 2.
Project CBM's replacement implementation is in capture.c and policy.h, under the
same GPL-2.0-only license. It does not compile the original unrestricted tool.
Corresponding source includes this directory, build rules and upstream reference.

The fixed helper accepts no arguments. It is invoked only through the separately
installed, fixed sudo rule. It checks the existing trusted activation policy and
pcbm UID/account. No setuid bits or file capabilities are installed. It opens DRM
primary nodes read-only, drops any implicitly acquired idle-console master
immediately, never acquires/steals an existing master, exports read-only pixels,
closes all device/PRIME/GEM resources, permanently drops groups/UID/GID and all
capabilities, and only then encodes PNG to stdout. It never opens output paths.

Only one connected active vc4 display with one fullscreen, unscaled, unrotated,
linear RGB565/XRGB8888/opaque ARGB8888 plane is admitted. Non-identity color LUTs,
CTM, extra planes/displays and unsupported modifiers fail closed. Bounds: 4096 on
each axis, 64 MiB scanout, three attempts, 10 s process alarm, 256 MiB address space.
Capture is a bounded CPU snapshot, not a promise of tear-free concurrent rendering.
No framebuffer, VT or modesetting writes are issued.
