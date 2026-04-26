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

- `.vscode/mcp.json` registers two local MCP servers:
  - `chrome-devtools` (launches isolated headless Chrome)
  - `chrome-devtools-attached` (connects to `http://127.0.0.1:9222`)
- `.vscode/tasks.json` defines a background task named `serve-nuclide-chart`

Default MCP server launch:

- `npx -y chrome-devtools-mcp@latest --headless=true --isolated=true`

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

How to run it in VS Code:

1. Open the Command Palette (`⇧⌘P` on macOS).
2. Run **Tasks: Run Task**.
3. Select **serve-nuclide-chart**.
4. Leave the task running while testing in browser/MCP.

Alternative:

- Menu: **Terminal → Run Task... → serve-nuclide-chart**

To stop the server task:

1. Open Command Palette (`⇧⌘P`).
2. Run **Tasks: Terminate Task**.
3. Choose **serve-nuclide-chart**.

It serves the project at:

- `http://127.0.0.1:8000/`

Main page:

- `http://127.0.0.1:8000/nuclide-chart.html`

### 2) Start/trust the MCP server in VS Code

Open the MCP server list in VS Code and start `chrome-devtools`.

If prompted, confirm trust for the server configuration.

If the default server cannot launch Chrome in your environment, start `chrome-devtools-attached` instead and connect to a Chrome instance running with remote debugging on port `9222`.

### 3) Use MCP-powered prompts in chat

Example prompts:

- "Open http://127.0.0.1:8000/nuclide-chart.html and summarize console errors."
- "Take a screenshot of the nuclide chart."
- "Record a performance trace for this page and report bottlenecks."
- "List failed network requests and likely causes."

## Capture console errors and page HTML (copy/paste prompts)

Use these prompts in Copilot Chat after the MCP server is running:

1. Open page:

  - "Open http://127.0.0.1:8000/nuclide-chart.html"

2. Capture browser errors:

  - "List all console messages for the current page and highlight errors and warnings only."

3. Capture full rendered HTML:

  - "Return `document.documentElement.outerHTML` from the current page."

4. Save both into files in this repo:

  - "Create `debug/console-errors.txt` with the error/warning output and `debug/page.html` with the current page HTML."

If output is too large, ask:

- "Split the HTML output into chunks and save to `debug/page.html` without truncation."

## One-command capture without MCP

You can capture browser console issues + final rendered HTML with one command:

- `npm run capture:debug`

Optional arguments:

- `npm run capture:debug -- --url=http://127.0.0.1:8000/nuclide-chart.html`
- `npm run capture:debug -- --out=./debug`
- `npm run capture:debug -- --timeout=60000`

Output files:

- `debug/page.html`
- `debug/console-errors.json`
- `debug/console-errors.txt`

## Human Operator UI for `chrome-devtools-attached`

If you want a manual control panel that feels like “being the bot”, this repo now includes a local UI backed by Puppeteer connected to a Chrome debug port.

### Start Chrome in remote-debug mode

1. Fully quit Chrome.
2. Start Chrome with remote debugging:

  - `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile-stable`

### Start the operator UI

- `npm run ui:attached`

Then open:

- `http://127.0.0.1:8787/`

The UI provides:

- page list/select/new page
- navigate/back/forward/reload
- wait-for-text
- run page JavaScript (`evaluate_script` style)
- capture screenshot to `debug/screenshots/`
- view live console and network request buffers

## Typical workflow

1. Start `serve-nuclide-chart`
2. Run `npm run capture:debug`
3. Fix issues in code
4. Re-run capture and compare outputs

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

If this still fails, use attached mode:

1. Fully quit Chrome.
2. Start Chrome with remote debugging:

  - `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile-stable`

3. In VS Code MCP servers, start `chrome-devtools-attached`.
4. Retry the same prompts.

### Local page not reachable

- Confirm `serve-nuclide-chart` task is running.
- Open `http://127.0.0.1:8000/` in your normal browser.

## References

- Chrome DevTools MCP package: https://www.npmjs.com/package/chrome-devtools-mcp
- VS Code MCP docs: https://code.visualstudio.com/docs/copilot/chat/mcp-servers
