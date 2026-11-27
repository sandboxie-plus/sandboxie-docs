# Is Shadow

`IsShadow` marks a temporary sandbox or template configuration section that SandMan uses to stage edits. It is managed by SandMan, not a sandbox option. The marker is present in Sandboxie Plus since 1.10.0 / 5.65.0. [^1]

## Syntax

Stored format: `IsShadow=y`. SandMan writes the marker to identify a staged section. Do not add or remove it by hand. [^2]

## How staging works

When SandMan merges staged edits into an existing section, it leaves the marker out of the original section. When it keeps a staged section as a new sandbox or template, it removes the marker from that section. Normal cleanup removes temporary sections that are not kept. [^2]

A shadow of an existing sandbox can point to the same file root as the original. Discarding that shadow discards staged configuration edits, not any file changes made in that root. [^2]

## See also

- [Is Virtual](IsVirtual.md)

[^1]: [Release 1.10.0 / 5.65.0](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.10.0) and [tagged SandMan staging code](https://github.com/sandboxie-plus/Sandboxie/blob/v1.10.0/SandboxiePlus/SandMan/SbiePlusAPI.cpp#L561-L580).
[^2]: [Shadow creation, application, and cleanup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Boxes/BoxShadows.cpp#L18-L117).
