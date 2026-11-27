# AI Agent Troubleshooting

Use this page either to investigate a sandbox problem with a connected agent or to get the connection working. Start with the Sandboxie message log; turn on resource tracing only when the messages do not explain the problem. [^1]

## Diagnose a sandbox problem

1. Tell the agent the sandbox name, the application, what you expected, and roughly when the problem happened.
2. Ask it to search the message log first. For example: *Check the recent Sandboxie messages for BrowserBox. Tell me what Sandboxie reported when the app failed to start, and what is still uncertain. Do not change settings.* The message log does not require resource tracing. [^1]
3. If you need more detail about resource access, enable the [Trace Log](TraceLog.md) in SandMan, reproduce the application problem, and ask the agent to look at that short time window. The trace cannot recover events that happened while tracing was off. Turn it off after collecting the evidence. [^1]

Treat a denied access as a clue, not as proof that the application failed because of it. Review any proposed rule change before applying it; do not relax isolation just to remove a trace entry.

## The client cannot connect

- **The client says Sandboxie-Plus is not accepting agent connections.** Check that SandMan is running and **Options > AI Agent Connection (MCP)** is on. If a custom pipe is in use, compare the client's pipe name with [`AiAgentEndpoint`](../Content/AiAgentEndpoint.md). [^2]
- **The menu item is unavailable or the listener will not open.** Check **Settings > General Config > AI Agent** and the SandMan message log. If an administrator has set [`AllowAiAgent=n`](../Content/AllowAiAgent.md), ask the administrator; the user setting cannot override it. [^3]
- **Setup cannot find `SbieMcp.exe`.** Open **Help > Troubleshoot with an AI Agent** to check the installation. The setup dialog expects the bridge executable next to SandMan. [^4]
- **SandMan refuses the client as sandboxed.** This is expected. Use a trusted local client outside the sandbox; leave the application you are investigating sandboxed. [^5]

## The agent can read documentation but not my sandboxes

Documentation lookup does not prove the client is paired. Ask the client to pair, look for the code in **Options > AI Agent Session Window**, and give it only to that client. If the code expired, have the same client request a new one. Then ask it to list or inspect a sandbox again to verify access. [^6]

## The agent can inspect but cannot apply a change

Check the consent mode and any prompt in the **AI Agent Session Window**. In **Look, do not touch**, covered changes are rejected without prompting. An administrator can also require confirmation even when the user has selected a less restrictive mode. This is separate from pairing; reconnecting will not lift the restriction. [^7]

## Offline documentation is unavailable

If the agent reports that the offline documentation pack is missing, check for `docs.7z` next to `SandMan.exe` in the Sandboxie Plus installation folder. A missing pack affects documentation lookup, not the agent connection itself. [^8]

1. Sign in to GitHub and open a recent successful run on the [Sandboxie CI workflow page](https://github.com/sandboxie-plus/Sandboxie/actions/workflows/main.yml). Use the run for your installed build if it is still available.
2. Under **Artifacts**, download **Assets** (`Assets.zip`). If the ZIP does not contain `docs.7z`, try another recent successful run. [^9]
3. Extract `docs.7z` from the ZIP and copy it next to `SandMan.exe`. Leave `docs.7z` itself packed. [^8]
4. If **Options > AI Agent Connection (MCP)** is already on, turn it off and back on to load the pack. Ask the agent to look up a Sandboxie setting to check that it works. [^8]

## See also

- [AI Agent Connection (MCP)](ai-agent-connection.md)
- [AI Agent Administration](ai-agent-administration.md)
- [Known Conflicts](../Content/KnownConflicts.md)

[^1]: [Message log and trace tools](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpTools.cpp#L303-L320).
[^2]: [Client connection error](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SbieMcp/main.cpp#L628-L637) and [listener startup and endpoint selection](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3145-L3176).
[^3]: [Menu state and tooltips](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3213-L3233) and [listener startup warning](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3259-L3264).
[^4]: [Setup menu action](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L793-L798) and [missing bridge message](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpConnectDialog.cpp#L100-L108).
[^5]: [Sandboxed client check](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L250-L271).
[^6]: [Session window action](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L928-L934), [pairing code display](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/SandMan.cpp#L3374-L3384), and [tool access and pairing code handling](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L731-L789).
[^7]: [Effective consent mode and read-only refusal](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpConsent.cpp#L39-L102).
[^8]: [Where SandMan looks for the archive](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpDocs.cpp#L33-L51) and [loading the pack at listener startup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/SandMan/Mcp/McpServer.cpp#L149-L158).
[^9]: [Sandboxie CI pack and artifact steps](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/.github/workflows/main.yml#L187-L205) and [GitHub artifact download instructions](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts).
