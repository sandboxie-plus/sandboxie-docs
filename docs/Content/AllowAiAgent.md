# Allow AI Agent

`AllowAiAgent` lets an administrator prevent SandMan from opening its AI agent listener. It is a global-only Sandboxie Plus setting, introduced in 1.19.1 / 5.74.1. SandMan checks this policy when it is connected to the Sandboxie API. [^1]

## Syntax

`AllowAiAgent=(y|n)`

Set this in `[GlobalSettings]` in [Sandboxie.ini](SandboxieIni.md). `n` blocks listener startup. `y` (the default) permits startup, but does not open the listener automatically or override the user's choice to turn AI agent connections off. [^2]

## Usage

To stop SandMan from opening a new listener even if the user has enabled AI agent connections:

```ini
[GlobalSettings]
AllowAiAgent=n
```

If the listener is already open, close it with **AI Agent Connection (MCP)** or exit SandMan. Setting `n` affects the next startup attempt; it does not close a running listener. [^2] [^3]

## See also

- [AI Agent Endpoint](AiAgentEndpoint.md)
- [AI Agent Require Pairing](AiAgentRequirePairing.md)
- [AI Agent Require Confirmation](AiAgentRequireConfirmation.md)

[^1]: [Release 1.19.1 / 5.74.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.19.1) and [tagged listener startup](https://github.com/sandboxie-plus/Sandboxie/blob/v1.19.1/SandboxiePlus/SandMan/SandMan.cpp#L3145-L3163).
[^2]: [User and administrator checks at listener startup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3145-L3163).
[^3]: [Listener close action](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3260-L3272).
