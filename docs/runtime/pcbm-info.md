# Using pcbm-info

`pcbm-info` reports what Project CBM was built as and what it is running on now.
It works without the interactive Menu or a network connection. No sudo is needed.
This first implementation is source-only; it has not been added to a new image.
POC1–3 do not gain the command through this work.

## Run it

In a future installation containing this command:

```sh
pcbm-info
pcbm-info --json
```

Today, from the source checkout, use `./runtime/bin/pcbm-info` with the same options.
The normal display is a concise summary. JSON is structured data for support tools
and the future configuration UI; it is not intended to be read as a pretty menu.

- **Built as:** product version, candidate/build identity and recorded component
  versions from the installed identity. Those facts do not change after installation.
- **Running on:** actual model, OS/kernel, usable memory, root capacity and connectors.
- **Current state:** current package versions, hostname, legacy default-machine
  configuration, service/link state, and the new preference foundation's values.

A package version changed by an administrator can differ from the original build.
Unknown means the collector could not establish a fact. A missing command, headless
system or masked service does not make the whole report unusable. “Masked” means a
service has been prevented from starting; it is not a failed running service.
Network link “up” does not prove Internet access. Advertised display modes are not
reported as an active mode. The existing engineering DRM helper can supply it when
already installed/authorized; otherwise it remains unknown.

Memory is Linux-usable memory after reservations, not necessarily the capacity on the
box. Storage reports the actual root filesystem and space available to an ordinary
user. It does not assume the root device is an SD card.

## Asking for support

Run `pcbm-info` and copy the relevant summary. For a structured local report:

```sh
pcbm-info --json > pcbm-info-report.json
```

The redirection above is your explicit file write; the collector itself is read-only.
Review before sharing: hostname and interface names can identify your local setup.
The report excludes IP/MAC addresses, Wi-Fi names/passwords, serial numbers, machine-id,
private keys, user history and builder environment. It does not gather logs or send
telemetry. A report identifies state; it does not authenticate a release or qualify
hardware. Synthetic examples are clearly labeled in [the example](info-example.txt).

## Preferences in this slice

The new preferences are not yet connected to existing Menu/boot behavior. The report
keeps them separate from the legacy configuration that existing consumers read.
Effective boot mode remains unknown: a saved choice alone does not prove which boot
path ran. See the [preference guide](preferences.md); do not edit a frozen candidate
to try this foundation during physical qualification.
