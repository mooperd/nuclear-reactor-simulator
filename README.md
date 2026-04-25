# Nuclear Reactor Simulator: Chrome DevTools MCP Guide

This project includes configuration for the **Chrome DevTools MCP server** so an AI coding assistant can inspect and control a live Chrome browser while you work.

## What is MCP?

**MCP (Model Context Protocol)** is a standard for connecting AI assistants to external tools.

In this project, MCP is used to connect your assistant to **Chrome DevTools**, which enables actions like:

- opening and navigating pages
- checking browser console errors
- inspecting network requests
- taking screenshots and DOM snapshots
- recording and analyzing performance traces

## What is configured in this repo?

- `.vscode/mcp.json` registers a local MCP server named `chrome-devtools`
- `.vscode/tasks.json` defines a background task named `serve-nuclide-chart`

The MCP server is launched with:

- `npx -y chrome-devtools-mcp@latest --isolated=true`

`--isolated=true` means Chrome uses a temporary profile for MCP sessions.

## Prerequisites

- VS Code with GitHub Copilot Chat + MCP support
- Node.js `20.19+` (this workspace currently has Node `22.x`)
- npm
- Google Chrome installed

## How to use it in this project

### 1) Start the local web server

Run the VS Code task:

- `serve-nuclide-chart`

It serves the project at:

- `http://127.0.0.1:8000/`

Main page:

- `http://127.0.0.1:8000/nuclide-chart.html`

### 2) Start/trust the MCP server in VS Code

Open the MCP server list in VS Code and start `chrome-devtools`.

If prompted, confirm trust for the server configuration.

### 3) Use MCP-powered prompts in chat

Example prompts:

- "Open http://127.0.0.1:8000/nuclide-chart.html and summarize console errors."
- "Take a screenshot of the nuclide chart."
- "Record a performance trace for this page and report bottlenecks."
- "List failed network requests and likely causes."

## Typical workflow

1. Start `serve-nuclide-chart`
2. Ask assistant to open and inspect `nuclide-chart.html`
3. Fix issues in code
4. Re-run analysis (console/network/performance)

## Security notes

- MCP servers can execute powerful tooling locally.
- Only run MCP servers you trust.
- Avoid exposing sensitive data in pages while running debugging automation.

## Troubleshooting

### MCP server does not start

- Verify Node and npm:
  - `node -v`
  - `npm -v`
- Check MCP logs from VS Code's MCP server management UI.

### Browser actions fail

- Ensure Chrome is installed and can launch normally.
- Restart the MCP server from VS Code.
- Retry with a simple prompt first (open page, take screenshot).

### Local page not reachable

- Confirm `serve-nuclide-chart` task is running.
- Open `http://127.0.0.1:8000/` in your normal browser.

## References

- Chrome DevTools MCP package: https://www.npmjs.com/package/chrome-devtools-mcp
- VS Code MCP docs: https://code.visualstudio.com/docs/copilot/chat/mcp-servers
