# Ralph

Autonomous coding agent loop for iOS/SwiftUI projects. Uses Claude to iteratively implement user stories from a PRD until all are complete.

## Quick Start

```bash
./ralph.py init    # Interactive setup - creates prd.json
./ralph.py run     # Run coding loop until complete
```

## How It Works

1. **Init**: Claude interviews you about your project and creates `prd.json` with user stories
2. **Run**: Claude picks the next incomplete story, implements it with TDD, runs code review, commits, and repeats

## Requirements

- Python 3
- Claude Code CLI (`~/.claude/local/claude`)
- Xcode (for iOS projects)
- `ANTHROPIC_API_KEY` in `.env`

## Creating a New Project

1. Create a new repo from this template
2. Initialize submodules: `git submodule update --init --recursive`
3. Run `./ralph.py init`
4. Run `./ralph.py run`

## Updating Skills

Pull latest SwiftUI skills from upstream:

```bash
git submodule update --remote skills/SwiftUI
git add skills/SwiftUI && git commit -m "Update SwiftUI skills"
```

See `CLAUDE.md` for detailed documentation.
