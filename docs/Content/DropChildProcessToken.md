# Drop Child Process Token

`DropChildProcessToken` is an advanced debugging setting introduced in Sandboxie Plus 1.15.6 / Classic 5.70.6. It can help troubleshoot child-creation problems, including issues historically described as “green box” compatibility problems. It is not a general recommendation to relax token handling.

When the setting matches, Sandboxie clears the explicit `hToken` supplied by the calling process to its child-process creation path. It does not disable Sandboxie's entire token pipeline or rewrite an existing token object.

## Configuration and caller scope

```ini
[DefaultBox]
DropChildProcessToken=parent.exe,y
```

The runtime default is `n`. This is an image-aware setting: `parent.exe` selects the sandboxed process **making the child-creation call**, not the executable it launches. The rule changes how matching callers create children; it does not change the token of `parent.exe` itself.

Sandboxie also clears a caller-supplied child token automatically for images classified as Acrobat Reader or plugin containers. Those hardcoded cases do not require a `DropChildProcessToken` rule. Historical Flash-specific code is commented out and is not an active automatic case.

## What happens to the child

The setting removes a caller-supplied child token from this creation request (`hToken = NULL`). What token the child ultimately runs with depends on the later sandbox mode and token-processing path:

- **Standard sandbox:** The driver ordinarily still reaches `Token_ReplacePrimary()` and assigns Sandboxie's restricted primary token. Clearing the caller's token and performing that later replacement are separate stages.
- **[Application Compartment](../PlusContent/compartment-mode.md) or [OriginalToken](OriginalToken.md):** Normal restricted-primary-token replacement is bypassed. Clearing the supplied token can therefore have a different and potentially larger effect on the Windows token chosen for the child.

The setting does not guarantee that a child inherits its parent's full token or that Sandboxie's remaining isolation mechanisms are disabled. Use it to investigate a specific child-creation compatibility problem, and review the token implications before retaining it in a configuration.

## Related pages

- [AppContainer Token Compatibility](AppContainerTokens.md)
- [Original Token](OriginalToken.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
