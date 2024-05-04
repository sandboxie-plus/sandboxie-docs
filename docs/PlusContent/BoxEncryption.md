# Encrypted Sandboxes

## Encrypted Box Image support

The Encrypted Box Image support empowers you to establish safeguarded sandboxed environments, fostering a level of protection that goes above and beyond to shield your confidential data.

In the pursuit of unassailable data security, the integration of Encrypted Box Image support represents a monumental leap forward. This technology grants you the capacity to construct sandboxed environments fortified by AES-XTS encrypted box images. This advanced methodology leverages the well-established cryptography implementation used in [DiskCryptor](https://diskcryptor.org), to create an impervious barrier around your sensitive data.

## Sandboxie Driver for Uncompromised Security:

A vital cornerstone in the security architecture is the SbieDrv driver. This guardian sentinel stands guard over the mounted encrypted box root folder, thwarting any unauthorized attempts by unsanctioned applications to access it. By ensuring that no data can escape the confines of the sandbox and preventing any exfiltration attempts by host applications, the sbiedrv driver establishes a watertight barrier.

## Secure Data Exchange and Inherent Confidentiality:

Root protection being activated mandates the definition of [OpenFilePath](../Content/OpenFilePath.md) paths for seamless data exchange between the host system and the encrypted sandbox. This method guarantees that file transfers occur within controlled parameters, maintaining the integrity of your data. Furthermore, the default setting of `ConfidentialBox=y` within an encrypted sandbox preserves the sanctity of your data by inhibiting host processes from accessing the memory of processes operating within the confines of the sandbox.
