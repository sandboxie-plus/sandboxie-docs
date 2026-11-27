# AI Agent Connection (MCP)

Sandboxie Plus can connect a local AI agent to SandMan to help diagnose sandbox problems. A paired agent can inspect sandbox settings, running processes, and recent Sandboxie messages. Start with diagnosis before asking the agent to change anything. The connection was introduced in Sandboxie Plus 1.19.1 / 5.74.1. [^1]

## Connect an agent

1. In SandMan, open **Help > Troubleshoot with an AI Agent**. Follow the setup instructions for your MCP client. Use a trusted local client running outside any sandbox. SandMan refuses connections from sandboxed processes. [^2]
2. In SandMan, turn on **Options > AI Agent Connection (MCP)** if it is not already on. [^3]
3. Ask the client to inspect one named sandbox. If it asks for a pairing code, open **Options > AI Agent Session Window** and give the displayed code only to the client you intended to connect. [^3] [^4]
4. Check that the agent can identify the sandbox and summarize its recent messages. If it can look up documentation but cannot see your sandboxes, check [pairing and connection problems](ai-agent-troubleshooting.md#the-agent-can-read-documentation-but-not-my-sandboxes). [^1] [^4]

## Pairing and approval

Pairing lets the client use tools that can read information about your Sandboxie installation. It does not approve changes. SandMan uses a separate consent mode for requests such as applying configuration edits or starting a program. For a diagnostic session, choose **Look, do not touch** to refuse requests that go through the change-approval check. [^4] [^5]

The connection to SandMan is local. Your AI client may still send the conversation and tool results to its model provider. Review the client's data-handling settings before sharing sensitive diagnostics.

## Disconnect

Turn off **Options > AI Agent Connection (MCP)** when you are finished. This stops the listener and closes its active connections. [^3]

## See also

- [AI Agent Administration](ai-agent-administration.md)
- [AI Agent Troubleshooting](ai-agent-troubleshooting.md)

[^1]: [Sandboxie Plus 1.19.1 / 5.74.1 release](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.19.1) and [diagnostic tools](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpTools.cpp#L282-L320).
[^2]: [Setup menu](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L793-L798), [client setup dialog](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpConnectDialog.cpp#L100-L153), and [local client checks](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L250-L271).
[^3]: [Options menu actions](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L928-L934), [listener toggle](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3259-L3264), and [listener shutdown](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L192-L223).
[^4]: [Pairing code in the session window](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3374-L3384) and [pairing checks on tools](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L731-L750).
[^5]: [Consent modes and decisions](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpConsent.cpp#L54-L110) and [operation handlers](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpOperate.cpp).
