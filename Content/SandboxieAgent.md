# The Sandboxie Agent Options

It is important to note that the Sandboxie Plus agent described below is quite new.   Most of the documentation for Sandboxie is still being updated to cover the new agent.  If you see documentation that refers Classic or Sandboxie Control that always refers to the classic application.  While the features of the new agent generally include everything in the old agent, they may be located in different places or with different wording. 

## Overview

Sandboxie is divided into many different components and services to provide the seamless integration it does.   One of the most user-visible pieces is the Sandboxie Agent.   This is the UI or primary application most users are interacting with for managing their sandboxes.  This agent is also the only difference between Sandboxie Classic and Sandboxie Plus installs (both can be used next to each other as well).  The agent acts as the graphical interface for editing the [Sandbox Settings](SBPlusSandboxSettings.md) along with the signaling tool to the other components to control the sandboxes themselves.

There are two major versions of the agent that are used:

- [Sandboxie Plus](SandboxiePlus.md) - The modern sandbox manager (SandMan.exe) having a more up to date interface and the latest features.  It uses a more modern UI platform so generally scales better with different dpi settings and matches Windows 10/11 theming more closely.  Almost all features in the Classic Agent have now implemented in Sandboxie Plus.  Virtually all features added to Sandboxie at this point are only added to the Sandboxie Plus agent.

- [Classic Sandboxie Control](SandboxieControl.md) -  The original UI application (SbieCtrl.exe) in Sandboxie Classic, well documented and the only UI available prior to June of 2020.  It receives only minor updates to keep existing features working with api changes.

## What agent should I use?

Both agents are included as many individuals have a preference for one over the other.  **Most new users should use [Sandboxie Plus](SandboxiePlus.md) agent** as it has all the new features, and a modern UI.   The [Classic Sandboxie Control](SandboxieControl.md) agent is mostly preferred by users who have been using Sandboxie for considerable time and know the old agent well.   There are currently no plans to end support for the classic tool.  Both tools edit the same configuration files, so it is possible to generally switch between them.   There are select features that the UI itself starts/controls that may only work with Sandboxie Plus.  You can also manage the sandbox configuration by editing the [Sandboxie Ini](SandboxieIni.md) directly (not recommended).
