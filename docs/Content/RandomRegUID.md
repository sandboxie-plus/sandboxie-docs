# Random Registry UID

RandomRegUID is a sandbox setting in [Sandboxie Ini](SandboxieIni.md).

```ini
[DefaultBox]
RandomRegUID=y
```

During initial sandbox customization, this setting attempts to write replacements for three values in the boxed Registry view:

- `HKLM\Software\Microsoft\Windows NT\CurrentVersion\ProductId`
- `HKLM\Software\Microsoft\Cryptography\MachineGuid`
- `HKLM\Software\Microsoft\SQMClient\MachineId`

It is not a Registry-read hook and does not generate a new value on every read. Other Registry identifiers are not covered by this setting. The three writes are attempted separately, so a failure can leave only some replacements in place.

The runtime fallback is disabled when no effective value is configured. The decision can use image-qualified, template, or global configuration, but it occurs when sandbox customization runs; it does not create a separate persistent identity for each process image. Current process initialization invokes customization only when the initiating process is neither using Sandboxie's restricted-token state nor its AppContainer-token state. This is not a categorical rule about Application Compartment.

Successfully written replacements persist with the sandboxed Registry content. Once the box is marked customized, changing `RandomRegUID` or restarting an application does not by itself repeat the writes. If the relevant sandbox content is removed and subsequently recreated, customization can run again under its normal initialization conditions.

In **Sandbox Options > Advanced Options > Privacy**, **Obfuscate known unique identifiers in the registry** controls the direct box setting. The checkbox is unchecked when no direct value is configured; an effective value can also come from applicable template or global configuration.
