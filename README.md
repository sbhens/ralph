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

**Option A: GitHub UI**
1. Click "Use this template" on GitHub
2. Clone with submodules: `git clone --recurse-submodules <url>`

**Option B: CLI**
```bash
gh repo create my-app --template sbhens/ralph --clone
cd my-app && git submodule update --init --recursive
```

Then:
```bash
./ralph.py init    # Interactive PRD setup
./ralph.py run     # Start coding loop
```

## Updating Skills

`skills/SwiftUI` is a submodule from [Dimillian/Skills](https://github.com/Dimillian/Skills). Pull latest:

```bash
git submodule update --remote skills/SwiftUI
git commit -am "Update SwiftUI skills"
```

See `CLAUDE.md` for detailed documentation.
