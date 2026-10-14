# Enable EFS

_EnableEFS_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.0 / 5.70.0. It allows selected EFS-related file-open requests outside Application Compartment mode to retry through Sandboxie's session-user file proxy after a native access-denied result. The retry remains subject to certificate capability, file-policy checks, and Windows filesystem authorization.

> [!NOTE]
> The proxy retry requires a currently applicable active advanced [supporter certificate](https://sandboxie-plus.com/supporter-certificate/) with the encryption capability[^1]. This is separate from the Windows EFS credentials needed to decrypt a file.

## Usage

```ini
[DefaultBox]

EnableEFS=y
```

The consumer fallback is disabled: if no effective value enables `EnableEFS`, this additional retry is not enabled. Effective configuration can come from the box, applicable enabled templates, or `GlobalSettings` fallback. A direct box value takes precedence over inherited values; `EnableEFS=n` explicitly overrides an inherited enabling value. The DLL resolves the setting for its calling process's box, and the worker checks the named box resolved from the caller. This is a box boolean, not a program-qualified setting.

The DLL queries the setting during eligible operations, and the worker rechecks it for each proxy request. After configuration reload, later eligible requests can use the changed value without inherently requiring a sandboxed application, SbieSvc, SbieDrv, or Windows restart. Existing handles are not automatically revoked, and changing the setting does not establish cancellation of already-submitted work. File-policy lists have their own reload lifecycle, and certificate-state refresh is separate from ordinary configuration reload.

## Enabling via Sandboxie Manager GUI

You can enable the setting from the Sandboxie Manager (also known as SandMan) for a specific sandbox (or the DefaultBox) using the following steps:

1. Open SandMan.
2. Right-click the sandbox you want to configure, and choose "Sandbox Options".
3. In the settings dialog, select the "General Options" category on the left.
4. Switch to the "File Options" tab and scroll to the "Disk/File access" section.
5. Check the option labeled "Allow sandboxed processes to open files protected by EFS".
6. Click "Apply" or "OK" to save the setting.

The checkbox reads the direct box setting, not necessarily the inherited effective configuration. Checking normally writes `EnableEFS=y`; unchecking removes ordinary direct values rather than writing `n`, so an inherited `y` may remain effective. A direct `EnableEFS=n` can override that inheritance, but a later save with the checkbox unchecked can remove that direct `n` too.

SandMan displays an advanced-certificate badge when the encryption capability is unavailable; the badge does not itself disable the checkbox or bypass runtime checks. The checkbox is disabled in [Application Compartment](NoSecurityIsolation.md) mode, where the ordinary DLL EFS retry is excluded.

## Overview

The Encrypting File System (EFS) is a Windows feature that provides filesystem-level encryption. `EnableEFS` controls an additional compatibility retry, not a blanket rule denying every EFS access when disabled. Native access depends on the selected Sandboxie file-routing path, Windows rights and EFS credentials, filesystem and sharing conditions, and applicable Sandboxie restrictions.

The setting does not supply EFS private keys, proxy every encrypted-file operation, or guarantee successful access. A Sandboxie supporter certificate authorizes the proxy feature; it is not a Windows EFS decryption credential.

## How It Works

For a selected true-file open that reaches the EFS retry path:

1. **Native Attempt**: Sandboxie first attempts the native open. Only an original `STATUS_ACCESS_DENIED` result in non-compartment mode, with effective `EnableEFS` enabled, proceeds to the EFS check[^2].
2. **EFS Detection**: The DLL checks `FILE_ATTRIBUTE_ENCRYPTED` on the selected target or, in certain missing-target cases, its parent. This parent check is not limited exclusively to file-creation requests. Detection alone does not establish authorization, decryption, or a usable handle[^2].
3. **Proxy Request**: If detection succeeds and reports EFS, the DLL submits the request to a session-specific UserServer worker[^4].
4. **Worker Authorization**: The worker validates the caller and Windows session, rechecks effective `EnableEFS`, verifies certificate capability, and checks device-path and process file-policy eligibility[^3][^6].
5. **Opening and Transfer**: The worker attempts to open the requested object with the supplied parameters and transfer a handle to the sandboxed caller. SbieSvc coordinates the worker, but the open uses the Windows session-user token rather than the main service's SYSTEM token; it is not necessarily the caller's restricted token. Windows authorization still applies, and a worker-side open does not guarantee a usable transferred handle[^5].

A successful native open does not need this retry, and other native failures do not trigger this branch. Non-EFS detection or failed attribute retrieval can prevent dispatch. Other routing paths, including ordinary sandbox-copy creation, need not use this helper.

## Security Considerations

- **Direct-Object Access**: Proxy access can expose a handle to the underlying object instead of creating a sandbox copy. If a writable handle to a host file is permitted, writes through that handle can affect the host file directly. This does not disable all sandbox isolation: worker checks, Windows permissions, handle rights, and other Sandboxie operation-specific controls remain relevant[^5].
- **Path Validation**: Proxy requests are subject to additional checks against the caller's process-specific file-policy lists, including Rule Specificity when enabled. A winning closed-path classification rejects proxy authorization. Proxy authorization should not be assumed to reproduce every normal file-routing behavior[^6].
- **Write Access Control**: Read-classified and write-classified requests have different authorization requirements. Access bits, creation dispositions other than `FILE_OPEN`, and delete-on-close can make a request write-capable, even without an intended change to existing contents. Write-capable requests require the proxy's open-path authorization; `EnableEFS=y` does not permit unrestricted writes[^7].

Do not broaden `OpenFilePath` permissions merely to enable EFS. Passing proxy authorization still does not guarantee Windows access or handle delivery.

## Certificate Requirements

The runtime requires a successful certificate-state query and an active certificate with the encryption capability (`opt_enc`)[^3][^8]. The project's UI calls this an active advanced supporter certificate; the worker enforces the capability flags rather than relying on that label alone. A generic supporter certificate without the required capability is insufficient.

Installation, nominal certificate level, or expiration date alone does not establish current acceptance. This capability is also associated with other encryption/protection features, whose runtime behavior is separate. It does not replace Windows EFS credentials.

## Related Messages

- [SBIE2225](SBIE2225.md) - "An attempt was made to access an EFS file" - Can report EFS detection during non-compartment file routing without an enabled setting or proxy attempt, or a failed eligible proxy retry. The message alone does not prove the final operation failed; it can coexist with certificate or transport diagnostics[^9].
- [SBIE6004](SBIE6004.md) - In the EFS worker, certificate-state retrieval failure or an unavailable active encryption capability causes this diagnostic and immediate rejection of that proxy request[^3]. It is not emitted for every native EFS access, and this worker check does not itself schedule five-minute process termination. Separate driver feature-enforcement paths can use the same message with different consequences.

## Limitations

- The worker accepts native paths with the case-insensitive prefix `\Device\HarddiskVolume`. This is a path-form restriction, not proof of a physical disk type, EFS-capable filesystem, available keys, or usable access. Normal network/UNC paths do not qualify merely by being mapped to a drive letter[^10].
- Proxying remains subject to the sandbox's file [resource access rules](ResourceAccess.md) and the worker's additional authorization checks; it is not a universal copy-on-write path or a substitute for Windows authorization.
- Application Compartment skips this ordinary retry; that does not guarantee either success or denial of native EFS access.
- Unsupported object-attribute forms, caller/session or policy rejection, native open failures, handle-transfer problems, and transport errors or timeouts can prevent access. Different response layers mean there is no single guaranteed application-visible Windows error for every proxy failure[^4][^5].

[^1]: [`UserServer::OpenFile()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L641-L652) rechecks effective enablement and requires `CertInfo.active && CertInfo.opt_enc` after successful state retrieval.
[^2]: [`File_GetFileType()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L5016-L5077) identifies `FILE_ATTRIBUTE_ENCRYPTED`. [`File_NtCreateTrueFile()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L4624-L4690) implements the native-first retry and conditional parent check; `File_NtCreateFileImpl()` also uses EFS detection during routing.
[^3]: The [driver state query](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/api.c#L1246-L1255) supplies certificate state. The [worker check](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L648-L652) logs SBIE6004 and rejects the request if retrieval fails or active encryption capability is absent.
[^4]: [`File_NtCreateFileProxy()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L4726-L4798) constructs the request and handles the reply. [`SbieDll_CallProxySvr()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/callsvc.c#L800-L864) handles transport, rejection, and timeout results.
[^5]: [`UserServer::StartWorker()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L181-L246) obtains and duplicates the session-user token to create the worker. [`UserServer::OpenFile()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L720-L759) opens the submitted native object and attempts handle transfer to the caller.
[^6]: The [worker policy path](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L660-L714) checks the device prefix, acquires process path lists, and applies additional authorization using [`SbieDll_MatchPathImpl()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/dllpath.c#L506-L595).
[^7]: [Write classification and authorization](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L663-L714) consider the access mask, disposition, and `FILE_DELETE_ON_CLOSE`, then require open-path authorization for write-capable requests and reject closed/write classifications.
[^8]: [`SCertInfo`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/verify.h#L24-L44) defines `opt_enc` for EFS and other encryption/protection features. [Certificate validation](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/verify.c#L982-L1085) establishes capability and activity rather than a simple expiration-date test.
[^9]: SBIE2225 is emitted at the [`File_NtCreateFileImpl()` detection site](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L3862-L3865) and the [`File_NtCreateTrueFile()` retry-failure site](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L4672-L4685).
[^10]: The [device-prefix check](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L660-L661) accepts the `\Device\HarddiskVolume` name prefix; it does not independently verify filesystem encryption capability.
