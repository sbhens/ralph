# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Ralph is an autonomous coding agent loop. It uses Claude to iteratively implement user stories from a PRD until all are complete.

## Architecture

**Two-phase workflow:**
1. `./ralph.py init` - Interactive setup that creates `prd.json` (user stories), `init.sh` (dependency setup), and `progress.txt` (execution log)
2. `./ralph.py run` - Iterative coding loop that picks the next incomplete story, implements it with TDD, and commits

**Key files:**
- `ralph.py` - Main entry point (Python)
- `prompt.md` - Instructions for the coding agent (read each iteration)
- `init-prompt.md` - Instructions for the init agent
- `prd.json` - User stories with `"passes": true/false` status and `verification.health_check` command
- `progress.txt` - Append-only execution log (NEVER overwrite, only append)
- `.ralph-initialized` - Marker indicating init completed

## Commands

```bash
./ralph.py init                # Initialize project (run once)
./ralph.py run                 # Run coding loop (default 10 iterations)
./ralph.py run -n 20           # Run with 20 iterations
./ralph.py run --model sonnet  # Use sonnet model (default: opus)
```

Re-initialize: `rm .ralph-initialized && ./ralph.py init`

Custom Claude binary: `CLAUDE_CMD=/path/to/claude ./ralph.py run`

## How Ralph Works

- **`init`**: Runs Claude interactively (no `--print`) to interview you and create `prd.json`
- **`run`**: Runs Claude with `--print --output-format stream-json` for real-time display. Loops until all stories have `"passes": true` or max iterations reached

The streaming output is parsed in `parse_stream_json()` to display tool invocations, results, and session cost.

## prd.json Schema

See `prd.json.example` for full structure. Key fields:

```json
{
  "project": { "name": "...", "description": "...", "stack": { ... } },
  "verification": { "health_check": "make build && make test" },
  "stories": [
    { "id": "US-001", "title": "...", "description": "As a user...",
      "acceptance_criteria": ["...", "..."], "passes": false }
  ]
}
```

## iOS Development

The Makefile provides iOS build commands (update `PROJECT_DIR`, `SCHEME`, `SIMULATOR` at the top for your project):

```bash
make build       # Build for simulator
make test        # Run unit tests
make run         # Build and launch in simulator
make deploy      # Build and deploy to connected device
make clean       # Clean build artifacts
```

When creating an iOS application:
1. Install and configure [XcodeBuildMCP](https://github.com/anthropics/XcodeBuildMCP) for Xcode integration
2. Reference SwiftUI skills in `skills/SwiftUI/` - read the relevant `SKILL.md` before using

### Available Skills (in `skills/SwiftUI/`)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `swiftui-ui-patterns` | Standard SwiftUI patterns | Building new UI components |
| `swiftui-view-refactor` | Refactor views for MV patterns | Cleaning up view structure |
| `swiftui-performance-audit` | Performance optimization | Diagnosing slow rendering |
| `swiftui-liquid-glass` | iOS 26+ Liquid Glass API | Adopting glass effects |
| `swift-concurrency-expert` | Swift 6.2+ concurrency fixes | Fixing actor/Sendable issues |
| `ios-debugger-agent` | Build/run/debug on simulator | Testing with XcodeBuildMCP |
| `gh-issue-fix-flow` | GitHub issue resolution | Fixing issues end-to-end |
| `app-store-changelog` | Generate release notes | Creating App Store "What's New" |

Read the `SKILL.md` in each folder for detailed workflows.

## Anthropic API

An Anthropic API key is available via environment variable `ANTHROPIC_API_KEY` (stored in `.env`). Use this for any features requiring LLM capabilities.
