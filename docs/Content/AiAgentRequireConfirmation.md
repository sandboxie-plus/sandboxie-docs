# AI Agent Require Confirmation

`AiAgentRequireConfirmation` keeps SandMan from automatically approving AI agent operations that go through its consent prompt. It is a global-only Sandboxie Plus setting, introduced in 1.19.1 / 5.74.1. [^1]

## Syntax

`AiAgentRequireConfirmation=(y|n)`

Set this in `[GlobalSettings]` in [Sandboxie.ini](SandboxieIni.md). When SandMan is connected to the Sandboxie API, `y` turns either permissive consent mode into **Ask before every change** for requests that go through the consent check. With `n` (the default), SandMan uses the selected mode as-is. This setting does not rewrite the user's preference or turn **Look, do not touch** into a prompt: that mode still refuses those requests. [^2]

## Usage

To require confirmation before applying AI agent edits to an existing sandbox:

```ini
[GlobalSettings]
AiAgentRequireConfirmation=y
```

SandMan can still stage proposed edits in a temporary configuration copy without asking. It checks consent when the agent asks to apply those edits to the original sandbox. To distinguish a staged copy from the original, see [Is Shadow](IsShadow.md). [^3]

## See also

- [Allow AI Agent](AllowAiAgent.md)
- [AI Agent Endpoint](AiAgentEndpoint.md)
- [AI Agent Require Pairing](AiAgentRequirePairing.md)

[^1]: [Release 1.19.1 / 5.74.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.19.1) and [tagged consent policy](https://github.com/sandboxie-plus/Sandboxie/blob/v1.19.1/SandboxiePlus/SandMan/Mcp/McpConsent.cpp#L40-L53).
[^2]: [Effective consent mode and action handling](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpConsent.cpp#L40-L113).
[^3]: [Writing edits to the staged copy](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpOperate.cpp#L480-L505) and [consent before applying them to the original](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpOperate.cpp#L575-L602).
