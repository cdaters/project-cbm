# Appliance setup and privilege review

2026-09-15. Owner requirement recorded during POC1 Pi 3B qualification.
**Design only; no privilege, networking, first-boot or Menu behavior changed.**
This is separate from the [x64sc failure](poc1-pi3b-analysis.md).

## Concrete diagnosis

The owner encountered privilege/passwordless-sudo errors involving
/usr/bin/raspi-config while trying ordinary settings. The exact error transcript
and entry path were not captured. Static inspection establishes the incompatibility:

- Pinned Menu pcbm-system and pcbm-network call `sudo -n raspi-config` and explain
  failure as needing passwordless sudo for that path.
- The frozen image has raspi-config and raspi-config-core 20260730 installed.
- Its /etc/sudoers retains normal password-authenticated `%sudo` administration;
  /etc/sudoers.d has no Project CBM command grant. The pi account belongs to sudo,
  but factory policy supplies no usable password and no passwordless sudo.
- The direct console service starts Bash despite pi's nologin account shell.
  That does not confer administration or provide an ordinary login recovery path.

Therefore this Menu operation cannot normally authorize itself on pristine POC1.
It is an integration/UX mismatch, not a consequence of NetworkManager being masked.
Even with authorization, disabled networking would be a separate operational
condition. Do not mark intentionally masked SSH/Samba/TCPser/Avahi/NetworkManager
as failed services or silently enable them during qualification.

## What v1 attempted, and why not to copy it

The actual historical image's /etc/sudoers.d/pcbm allows passwordless poweroff/reboot,
raspi-config, selected TCPser/Samba/network service actions, and mount/umount/tee/
mkdir/rm. It tried to let a physical appliance user configure networking, manage
optional services, import storage/content and shut down without password prompts.

The general file/mount utilities accept unrestricted arguments; root writes/removal
and mount operations are far broader than those product operations. raspi-config
is itself a broad, evolving administration surface, not a narrow appliance action.
A command entry without arguments does not restrict its arguments. No exploit was
attempted. [sudoers semantics](https://manpages.debian.org/trixie/sudo/sudoers.5.en.html)
support the interpretation; it is not a recommendation to restore those rules.

The repository's pcbm-sudoers.example is not identical to the shipped fragment:
it includes a release-prep command and Avahi restart, lacks shipped nmbd entries,
and uses legacy /usr/local paths. Do not treat that example as the installed truth.
The Menu's dhcpcd/NetworkManager guessing, generic permission-repair guidance and
service-state handling also do not constitute a supported setup contract. Samba
credential enrollment, modern account policy and service prerequisite validation
are not solved by those grants. Read-only status should normally need no root.

**Recommendation:** no direct passwordless raspi-config in normal/public CBM.
Retain it as an explicitly authenticated advanced/admin tool if useful. Normal
appliance users must not need it to complete supported setup. Raspberry Pi's
[configuration documentation](https://www.raspberrypi.com/documentation/computers/configuration.html)
describes it as an administrative tool; CBM should expose a smaller product surface.

## Supported configuration UX for 1.1

| Setting | First boot (offline capable) | CONTROL / System Settings | Advanced or underlying OS |
| --- | --- | --- | --- |
| Locale, keyboard, timezone | Simple choices; valid defaults and later-change route | Change supported values; explain restart effects | OS locale/tzdata and keyboard machinery |
| Wi-Fi regulatory country | Ask before enabling Wi-Fi; allow deferral with radio disabled | Change using validated country list | Never infer regulatory authorization from timezone |
| Wi-Fi credentials/network | Optional; explicit Skip network | Scan/select/hidden SSID, enroll, disconnect/forget; useful errors | NetworkManager owns profiles, DHCP/DNS/routes |
| Ethernet/status | Show status; not required to finish setup | Read-only addresses/link/connectivity state | Normal OS automatic configuration; no wrapper for routine DHCP |
| Hostname | Optional choice or safe default | Validated rename with effects explained | hostname management and dependent service identity |
| Audio | Optional simple device/test later | User-level output/preferences and bounded test | ALSA driver/device discovery; root only where specifically required |
| Display | Automatic safe detection | Small tested set only, preview/revert where feasible | KMS/EDID normal behavior; unusual boot/hardware tuning is advanced |
| SSH | Not required; explicit opt-in only after policy/enrollment | Enable/disable with credential/key readiness and status | Fresh host keys; explicit admin policy, no inherited builder credentials |
| Samba | Not required | Enable/disable, share status and distinct credential enrollment | Unix password does not automatically update Samba password; test both |
| TCPser/BBS | Not required | Validated serial/network options and opt-in service control | Do not accept arbitrary daemon arguments or automatically expose listeners |

No forced network access, online account or service enablement is needed to reach
the Commodore appliance. Wi-Fi users should complete setup inside CBM without a
shell or sudoers edits. Persist choices atomically and resume after interruption;
never regenerate/overwrite successful choices merely because setup reruns. Keep
root expansion/machine identity in their existing single first-boot mechanism;
interactive preferences are a separate retry-safe phase, not a competing expander.
Build sealing must contain neither enrolled credentials nor completion state.

## Recommended privilege architecture

Use small root-owned fixed-purpose helpers, called through exact reviewed sudoers
entry points, with ordinary OS tools/APIs underneath. A custom daemon is unnecessary
initially. NetworkManager's [nmcli/API](https://networkmanager.dev/docs/api/latest/nmcli.html)
is a possible implementation mechanism, not blanket authorization for every NM action.
Existing polkit actions can be considered per operation when their scope matches;
broad network-profile modification permission is not automatically the right boundary.

Requirements before implementation:

- Declare each operation, allowed local operator/group/session, input schema,
  affected files/services, output/error codes and rollback behavior. Tie active-seat
  assumptions to the corrected PAM/logind session and test remote/inactive callers.
- No NOPASSWD: ALL, root shell, arbitrary executable/path/unit, shell evaluation,
  wildcard general-purpose utilities, user-controlled helper code or environment.
  Reject unsupported fields/values; fixed PATH and controlled subprocess argv.
- Root-owned implementation/configuration; safe file ownership and symlink checks,
  atomic updates/locking, constrained service names and sensible bounds. Unprivileged
  display/status/preferences remain unprivileged.
- Carry secrets over protected stdin/D-Bus, not argv or logs. Root-owned protected
  network profiles; no password echo, history, broad environment capture or image
  embedding. Record action/result without Wi-Fi/Samba secrets.
- Explicitly test injection, traversal, symlink swaps, unauthorized units/callers,
  repeat/interrupted operations, credential failures and no unintended root access.
  Validate sudoers with visudo in the controlled test environment before activation.
- Separate the appliance operator role from optional authenticated system admin.
  An operator compromise may perform approved appliance actions, not arbitrary root
  administration. Review existing sudo-group membership when that policy is designed.

This is a recommendation, not a completed security design or implemented helper.

## POC2 boundary and acceptance after POC2

For the launch-diagnosis POC2, make unsupported setup actions accurately identify
that the engineering profile has no supported enrollment path; remove instructions
to grant blanket permissions or manually repair sudoers. Keep intentionally masked
services masked unless a new explicit engineering-SSH profile is approved. Do not
restore v1 sudoers to make its old Menu calls work.

Defer the complete first-boot preference wizard, Wi-Fi/credential enrollment,
service configuration UI, helper implementation and public service defaults beyond
POC2. They remain **required 1.1 product work**, with offline-skip, ordinary Wi-Fi
setup, distinct Samba credentials and negative privilege tests in acceptance.
An engineering diagnostic console is not the final appliance setup experience.
