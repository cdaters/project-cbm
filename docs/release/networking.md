# Networking and services

[Documentation index](../README.md) · [User Manual](user-guide.md)

You can use Project CBM offline. A home-network connection is useful for copying files,
connecting by terminal and using a BBS. It does not require enabling every service.
Use CONTROL → Network for the connection itself, and CONTROL → Services for features
other computers can reach.

## Addresses and Computer Name

**Computer Name** identifies the Pi on your network. The default is `projectcbm`.
With Network Discovery on, many home networks let you use **projectcbm.local** rather
than remember a numeric address. If you rename the Pi to `mycbm`, try `mycbm.local`.

An **IP address** is an address assigned to a network interface, usually by your router.
Main Menu shows useful current addresses. Network/System Information shows more detail,
including multiple connected interfaces. An Ethernet and Wi-Fi connection can have
different addresses at the same time. Use an address reachable from your other computer.
An address may change after reconnecting or restarting the router.

The **MAC address** identifies the network adapter on the local network. A **gateway**
is normally your router, used to reach other networks. **DNS servers** translate names
into addresses. These details are mainly useful when troubleshooting; displaying them
is not the same as offering editable settings. Project CBM shows values from its system
information service rather than guessing interface names.

## Ethernet and Wi-Fi

For Ethernet, connect the cable and choose Use Ethernet in setup, or Enable normal
networking later. A normally configured home router supplies the address automatically.
Check the Network screen if no address appears. Offline mode also disables Ethernet.

For Wi-Fi, choose the country where the Pi is actually used; this sets the radio rules.
Nearby Wi-Fi networks waits for the radio and a fresh scan, then lets you choose an
SSID (the network name) and password. The normal workflow supports WPA personal
networks with an 8–63 printable ASCII character password. Enterprise, open and unusual
network configurations require Advanced Linux administration. A hidden SSID can be
entered using Join Wi-Fi by name. Passwords are masked and not displayed in status.

## Network controls

| Action under CONTROL → Network | What it changes or shows |
| --- | --- |
| Network information (IP/MAC and status) | Opens System Information; read-only |
| Computer Name | Saves a new name and updates local identity/discovery configuration |
| Wi-Fi country and radio | Sets the regulatory country and enables the radio |
| Nearby Wi-Fi networks | Runs the guided scan/choose/connect workflow |
| Join Wi-Fi by name (WPA personal) | Enter the exact SSID and password; enables networking |
| Disconnect Project CBM Wi-Fi | Disconnects the Project CBM-managed connection; does not erase its saved password |
| Forget Project CBM Wi-Fi | Removes that saved connection after confirmation; separately administered connections remain |
| Enable normal networking | Allows configured Ethernet/Wi-Fi connections to activate |
| Stay offline (disable connections) | Disconnects networking, including Ethernet and remote sessions |

Use a Computer Name beginning with a lowercase letter, followed by lowercase letters,
digits or hyphens, ending with a letter/digit, at most 63 characters. Do not enter spaces
or `.local`; discovery supplies the suffix. Choose a distinct name for a second Pi.
Changes persist. Remote sessions may disconnect when their connection/name changes;
reconnect using the newly displayed address.

## Services

Each service screen reports actual state and offers only useful actions. **Off** offers
Turn On; **On** offers Turn Off. **Starting / Pending** means it has not yet reached a
confirmed usable state. **Failed** needs attention; **Unavailable** means information or
the required service is unavailable. Refresh status rechecks it. A saved On preference
is not itself proof a connection will succeed. Settings persist through reboot.

Project CBM is a single-owner home-LAN appliance. These services are intended for your
local network, not automatic Internet exposure. Choose real passwords; do not forward
service ports on your router unless you deliberately administer that exposure.
Turning networking on does not automatically turn optional services on.

## Remote Access

Remote Access (SSH) gives you a text terminal on the Pi from another computer.

1. Open CONTROL → Services → **Remote Access (SSH)**.
2. Choose **Turn On Remote Access (SSH)** and wait for **Status: On**.
3. Open **How to connect**. Note the current name/address and username.
4. On macOS/Linux, open Terminal. On Windows, open PowerShell/Terminal with OpenSSH
   Client available. Run:

```sh
ssh pcbm@projectcbm.local
```

Use the **administrator password chosen during first boot**, not the File Sharing
password. SSH password entry normally shows no characters; that is separate from the
masked Project CBM setup dialogs. On first connection, SSH asks you to trust the Pi's
host key. Verify the target before accepting. After a reflash the key changes; investigate
an unexpected change rather than routinely bypassing warnings.

If the name does not resolve, substitute the current IP shown by Project CBM, for example
`ssh pcbm@192.168.1.50` with your own address. Microsoft documents the
[Windows OpenSSH client](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse).
Type `exit` to disconnect. To disable the service, return to its screen and choose
**Turn Off Remote Access (SSH)**; check that it reports Off.

### SFTP file transfer

An SFTP client uses the same SSH service, account and administrator password. Its
starting folder is `/home/pcbm`; open `content` for the Project CBM library. For a
command-line client:

```sh
sftp pcbm@projectcbm.local
```

Then use `cd content/games/c64`, `put MyGame.d64`, and `bye`. `put` can replace a same-name
file, unlike USB import's duplicate-preserving policy. Review the destination first.

## File Sharing

File Sharing lets another computer browse and write the Project CBM content library.
The share is named **Project CBM**, including the space. It exports `/home/pcbm/content`,
not your entire home, system settings or administrator credentials.

1. Open CONTROL → Services → **File Sharing**.
2. Choose **Set / change File Sharing password**, or let Turn On request it when unset.
   Choose and confirm a separate password of 12–128 printable characters, excluding colon.
3. Choose **Turn On File Sharing**. This also turns on Network Discovery.
4. Wait for **Status: On**, then open **How to connect**.

The username is **pcbm**. **The File Sharing password is separate from the administrator
password.** The program providing sharing, Samba, keeps its own password database.
Changing one password does not change the other. Do not post either password in support
requests. To turn sharing off, use **Turn Off File Sharing** and check Off; discovery
can be controlled separately.

### From a Mac

In Finder choose **Go → Connect to Server** and enter:

```text
smb://projectcbm.local/Project%20CBM
```

Choose Registered User, enter `pcbm` and your File Sharing password. The opened share
contains `games`, `demos`, `programs`, `music` and the other library folders. Copy a C64
game into `games/c64`, then find it in CONTENT → GAMES on the Pi. Finder's Network
sidebar may also show the Pi when discovery works, but the direct address is sufficient.
Eject the share in Finder when finished.

### From Windows

In File Explorer's address bar enter:

```text
\\projectcbm.local\Project CBM
```

Sign in as `pcbm` with the File Sharing password. Copy to the appropriate machine
folder exactly as on a Mac. If saved credentials are wrong, disconnect the old session
and remove/update its saved entry in Windows Credential Manager before reconnecting.

### When discovery does not work

Use the IP shown on the Pi, for example `smb://192.168.1.50/Project%20CBM` on Mac or
`\\192.168.1.50\Project CBM` on Windows. Replace the example address with your Pi's.
Both computers must be on a network that allows them to communicate; guest Wi-Fi often
isolates devices. If IP works but `.local` does not, the share itself is working.

## Network Discovery

Project CBM uses Avahi for local names and service announcements (mDNS). With discovery
on, compatible computers can resolve the `.local` name. File Sharing also advertises
its SMB service to compatible browsers. Turn discovery on/off from its Services screen;
no Internet service is required. Direct IP access remains available when other services
are on even if discovery is off.

Automatic Windows Network browsing is not guaranteed; no extra Windows browsing daemon
is included solely to populate that screen. A missing Finder/Explorer icon does not
prove sharing is broken. Try How to connect and the direct address before changing
advanced settings.

## BBS / Modem

A bulletin board system (BBS) is a computer you connect to with terminal software to
read messages or exchange files. Old Commodore terminals expect a modem. **TCPser**
provides an emulated modem connection to network BBS systems.

Enable **BBS / Modem** under Services when using compatible terminal software. **Modem
port and speed** accepts a local port from 1024–65535 (default **25232**) and baud
300, 1200, 2400, 9600, 19200 or 38400. **How to connect** shows the local emulator
endpoint **127.0.0.1:25232** at the default port. This local address means the Pi itself;
it is not the address of the remote BBS and not a public modem server.

Configure the terminal/emulated modem according to its own instructions and the chosen
VICE interface. Use a BBS endpoint you are permitted to access. Terminal software may
have its own saved settings/passwords; protect those with your personal backups.
StrikeTerm is separately rights-gated; its presence in a test image does not make it
part of the public release. End-to-end BBS connectivity still needs physical testing.
Turn **BBS / Modem** off when not needed.

## Quick connection checks

If SSH is refused, verify Remote Access reports On. If sharing rejects a password,
check that you used its separate password. If neither service is reachable, check IP,
normal-networking mode, cable/Wi-Fi and guest-network isolation. See
[troubleshooting](troubleshooting.md#network-and-services) before collecting logs.
