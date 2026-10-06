Sandboxie Plus offers six base box types and an optional encrypted/confidential combination.

A sandbox typically isolates your host system from processes running within the box, it prevents them from making permanent changes to other programs and data in your computer. The level of isolation impacts your [security](../PlusContent/security-mode.md) as well as the [compatibility](../PlusContent/compartment-mode.md) with applications.
Sandboxie Plus can [protect your personal data](../PlusContent/privacy-mode.md) from being accessed by processes running under its supervision.

Sandboxie Plus can also combine [encrypted sandbox storage](../PlusContent/BoxEncryption.md) with [Confidential Box](../Content/ConfidentialBox.md) protection, which restricts relevant unsandboxed host-process access to sandboxed process and thread handles. [Mounted-root protection](BoxEncryption.md#root-protection-while-mounted) is a separate filesystem protection option. See [Black Box](../PlusContent/black-box.md) for the combined wizard option.

The table shows the ordinary configuration of the six base types. **Application Compartment** identifies that mode, not a general compatibility rating. Colors and icons are presentation aids, not guarantees about a box's effective settings.

| Box Type | [Security Hardened](../PlusContent/security-mode.md) | [Data Protection](../PlusContent/privacy-mode.md) | [Application Compartment](../PlusContent/compartment-mode.md) |
|-|-|-|-|
|![](../Media/sandbox-r-full.png) Red Box — Security Hardened Sandbox with Data Protection|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-o-full.png) Orange Box — Security Hardened Sandbox|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-b-full.png) Blue Box — Sandbox with Data Protection|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-y-full-e1684328804872.png) Yellow Box — Standard Sandbox|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-c-full.png) Cyan Box — Application Compartment Box with Data Protection|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|
|![](../Media/sandbox-g-full.png) Green Box — Application Compartment Box|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|

## Encrypted and confidential option

The New Box Wizard's **Encrypt Box content and set Confidential** option can be combined with any of the six base types. In the normal wizard workflow, it adds `UseFileImage=y` and `ConfidentialBox=y` while retaining the selected base configuration.

| Feature | Black Box option |
|-|-|
| [Encrypted Storage](BoxEncryption.md) | Yes |
| [Confidential Process Protection](../Content/ConfidentialBox.md) | Yes |
| Security / Data Protection / Application Compartment mode | Retained from the selected base type |

![Black Box type icon](../Media/sandbox-k-full.png) SandMan can display this dark icon for the combined encrypted/confidential presentation. It does not identify one fixed base mode or imply a black border. See [Box Presentation](../Content/BoxPresentation.md) for presentation settings.
