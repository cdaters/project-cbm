# Boot experience backlog — owner observation, 2026-09-17

The owner of the tested POC4 attempt #4 Pi 3B observes a Raspberry Pi rainbow screen,
Linux/kernel/userspace startup messages, then Project CBM Menu. The desired appliance
experience minimizes visible Raspberry Pi/Linux implementation detail and reaches an
interactive Menu as quickly as responsibly possible.

Quiet boot and fast boot are separate work items. Quiet boot concerns presentation:
firmware splash, console verbosity and a truthful path for setup/failure/recovery
messages. Hiding messages is not evidence of reduced boot time. Fast boot concerns
measured time to a keyboard-responsive Menu, including firmware, kernel, userspace,
first-boot setup and ordinary subsequent boots as distinct intervals.

Before optimization, measure actual Pi 3B timing across repeated cold/warm boots;
record media, power/display conditions, first-boot versus normal startup, median and
worst case. Identify the critical path before removing or parallelizing work. Retain
accessible diagnostic output and failure visibility. Preserve known-good getty/PAM/
TTY/session behavior, terminal ownership, Menu input/VT switching, setup/readiness and
security boundaries. Do not infer speed from systemd timing alone or a hidden console.

This is backlog only, not implementation or a performance promise. No boot splash,
cmdline, service/getty/PAM/session, firmware or startup optimization is authorized by
this physical-evidence follow-up. See the [physical review](../qualification/poc4-attempt4-physical-review-2026-09-17.md).

## Attempt #5 owner observation, 2026-09-18

The owner again reports the Raspberry Pi rainbow and Linux/kernel/userspace startup
messages. Quiet appliance presentation and a Project CBM boot splash remain deferred.
Measured boot-time optimization remains a separate deferred task. This correction
cycle makes no firmware, cmdline, getty, PAM, TTY or session boot changes.
