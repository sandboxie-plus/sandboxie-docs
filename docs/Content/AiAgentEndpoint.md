# AI Agent Endpoint

`AiAgentEndpoint` sets the named pipe SandMan listens on for local AI agent connections. It is a global-only Sandboxie Plus setting, introduced in 1.19.1 / 5.74.1. [^1]

## Syntax

`AiAgentEndpoint=<pipe-name>`

Put the pipe name in `[GlobalSettings]` in [Sandboxie.ini](SandboxieIni.md). Use just the name, without a pipe path or surrounding spaces. Start it with `SbieMcp` (case-insensitive), keep it to 64 characters or fewer, and use only ASCII letters, digits, underscores, hyphens, and periods. [^2]

## Usage

To use a custom name:

```ini
[GlobalSettings]
AiAgentEndpoint=SbieMcp_Custom
```

Close and reopen the listener using **AI Agent Connection (MCP)** in SandMan, and update the client's configuration to use the same pipe name. A listener that is already open keeps its original name. [^3]

SandMan reads the global value when it starts the listener and is connected to the Sandboxie API. If the global value is unavailable or empty, SandMan uses `Options/McpEndpoint` from the per-user `Sandboxie-Plus.ini`, with `SbieMcp` as the default. If the selected name fails validation, the listener does not start; SandMan does not try another name. [^3]

## See also

- [Allow AI Agent](AllowAiAgent.md)
- [AI Agent Require Pairing](AiAgentRequirePairing.md)
- [AI Agent Require Confirmation](AiAgentRequireConfirmation.md)

[^1]: [Release 1.19.1 / 5.74.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.19.1) and [tagged SandMan source](https://github.com/sandboxie-plus/Sandboxie/blob/v1.19.1/SandboxiePlus/SandMan/SandMan.cpp#L3158-L3175).
[^2]: [Endpoint name validation](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpProtocol.cpp#L9-L47).
[^3]: [Endpoint selection](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3163-L3176), [validation before opening the listener](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L124-L143), and [listener toggle](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3259-L3264).
