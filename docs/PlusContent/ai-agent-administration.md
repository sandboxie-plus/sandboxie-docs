# AI Agent Administration

Use the global AI-agent settings in [Sandboxie.ini](../Content/SandboxieIni.md) to control whether SandMan can open the listener, which pipe it uses, and whether users can waive pairing or confirmations. The settings belong in `[GlobalSettings]`. SandMan reads these policies when it is connected to the Sandboxie API; they are not per-sandbox settings. [^1] [^2] [^3]

## Choose the control you need

| Goal | Setting | Effect |
| --- | --- | --- |
| Prevent the listener from opening | [`AllowAiAgent=n`](../Content/AllowAiAgent.md) | Blocks a new listener. It does not stop one that is already open. [^1] |
| Keep a fixed pipe name | [`AiAgentEndpoint`](../Content/AiAgentEndpoint.md) | A nonempty global name overrides the per-user choice at listener startup. The client must use the same name. [^1] |
| Prevent users from waiving the pairing code | [`AiAgentRequirePairing=y`](../Content/AiAgentRequirePairing.md) | Requires a code for clients that are not already authorized. It does not revoke existing authorizations or remove remembered clients. [^2] |
| Keep confirmation on for covered operations | [`AiAgentRequireConfirmation=y`](../Content/AiAgentRequireConfirmation.md) | Treats less restrictive consent modes as **Ask before every change**. It leaves **Look, do not touch** in effect if the user selected it. [^3] |

Use [Configuration Protection](../Content/ConfigurationProtection.md) if users should not be able to change these policies in `Sandboxie.ini`.

## Allow diagnosis without automatic changes

Keep pairing enabled and select **Look, do not touch** for diagnosis. Pairing governs access to tools that read live Sandboxie information; the consent mode decides how SandMan handles requests that go through its change-approval check. A paired client can still read diagnostics. A temporary configuration copy is distinct from applying edits to the original sandbox. [^2] [^3] [^4]

To let users approve changes individually without letting them turn off confirmations, set `AiAgentRequireConfirmation=y`. This policy enforces a minimum level of confirmation; it does not change the user's saved preference. [^3]

## Stop access now

If a listener is already open, turn it off with **Options > AI Agent Connection (MCP)** or exit SandMan. Set `AllowAiAgent=n` if it must not open again. To change the endpoint instead, close and reopen the listener after editing the setting, and update the client to match. [^1] [^5]

## See also

- [AI Agent Connection (MCP)](ai-agent-connection.md)
- [AI Agent Troubleshooting](ai-agent-troubleshooting.md)

[^1]: [Listener startup policy and endpoint selection](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3145-L3176).
[^2]: [Pairing policy](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L239-L249), [remembered clients](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L359-L389), and [pairing checks on tools](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L731-L750).
[^3]: [Policy and effective consent mode](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpConsent.cpp#L39-L61) and [consent decisions](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpConsent.cpp#L83-L110).
[^4]: [Writing to a staged copy](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpOperate.cpp#L480-L505) and [approval before applying it to the original sandbox](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpOperate.cpp#L575-L602).
[^5]: [Stop and clear the listener](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3179-L3200) and [listener toggle](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3259-L3264).
