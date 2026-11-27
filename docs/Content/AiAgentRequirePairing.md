# AI Agent Require Pairing

`AiAgentRequirePairing` prevents users from waiving SandMan's pairing-code requirement for AI agent clients that are not already authorized. It is a global-only Sandboxie Plus setting, introduced in 1.19.1 / 5.74.1. [^1]

## Syntax

`AiAgentRequirePairing=(y|n)`

Set this in `[GlobalSettings]` in [Sandboxie.ini](SandboxieIni.md). With `y`, SandMan requires pairing when connected to the Sandboxie API. With `n` (the default), SandMan follows the per-user `Options/McpRequirePairing` preference in `Sandboxie-Plus.ini`. That preference defaults to requiring pairing, so `n` does not itself turn pairing off. [^2]

## Usage

To keep the pairing code required even if the user has chosen to waive it:

```ini
[GlobalSettings]
AiAgentRequirePairing=y
```

An unauthorized client needs the code to use tools that require pairing. SandMan does not revoke existing authorizations or make remembered clients enter a new code. Public tools, such as documentation and settings-schema lookup, still do not require pairing. [^3]

## See also

- [Allow AI Agent](AllowAiAgent.md)
- [AI Agent Endpoint](AiAgentEndpoint.md)
- [AI Agent Require Confirmation](AiAgentRequireConfirmation.md)

[^1]: [Release 1.19.1 / 5.74.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.19.1) and [tagged pairing policy](https://github.com/sandboxie-plus/Sandboxie/blob/v1.19.1/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L244-L250).
[^2]: [Global and per-user pairing policy](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L244-L251).
[^3]: [Client authorization](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L359-L389), [pairing checks on tool calls](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L731-L750), and [public tool list](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpTools.cpp#L371-L388).
