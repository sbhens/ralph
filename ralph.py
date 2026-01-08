#!/usr/bin/env python3
"""
Ralph - Autonomous Coding Agent Loop

Usage:
    ./ralph.py init              # Interactive project setup
    ./ralph.py run               # Run coding loop (default 10 iterations)
    ./ralph.py run -n 20         # Run with 20 iterations
    ./ralph.py run --model sonnet  # Use sonnet model
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
INIT_MARKER = SCRIPT_DIR / ".ralph-initialized"
PRD_FILE = SCRIPT_DIR / "prd.json"
PROMPT_FILE = SCRIPT_DIR / "prompt.md"
INIT_PROMPT_FILE = SCRIPT_DIR / "init-prompt.md"
CLAUDE_CMD = os.environ.get("CLAUDE_CMD", os.path.expanduser("~/.claude/local/claude"))


def parse_stream_json(line: str) -> None:
    """Parse a single line of stream-json output and print human-readable version."""
    try:
        data = json.loads(line)
        msg_type = data.get("type", "")

        if msg_type == "system" and data.get("subtype") == "init":
            model = data.get("model", "unknown")
            print(f"[Session started - {model}]", flush=True)

        elif msg_type == "assistant":
            message = data.get("message", {})
            content = message.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    text = item.get("text", "")
                    if text:
                        print(text, flush=True)
                elif item.get("type") == "tool_use":
                    tool_name = item.get("name", "unknown")
                    tool_input = item.get("input", {})
                    if tool_name == "Bash":
                        cmd = tool_input.get("command", "")[:80]
                        print(f"\n>>> Bash: {cmd}", flush=True)
                    elif tool_name == "Read":
                        path = tool_input.get("file_path", "").split("/")[-1]
                        print(f"\n>>> Read: {path}", flush=True)
                    elif tool_name == "Edit":
                        path = tool_input.get("file_path", "").split("/")[-1]
                        print(f"\n>>> Edit: {path}", flush=True)
                    elif tool_name == "Write":
                        path = tool_input.get("file_path", "").split("/")[-1]
                        print(f"\n>>> Write: {path}", flush=True)
                    elif tool_name == "Glob":
                        pattern = tool_input.get("pattern", "")
                        print(f"\n>>> Glob: {pattern}", flush=True)
                    elif tool_name == "Grep":
                        pattern = tool_input.get("pattern", "")
                        print(f"\n>>> Grep: {pattern}", flush=True)
                    else:
                        print(f"\n>>> {tool_name}", flush=True)

        elif msg_type == "user":
            content = data.get("message", {}).get("content", [])
            for item in content:
                if item.get("type") == "tool_result":
                    is_error = item.get("is_error", False)
                    print(" [ERROR]" if is_error else " [OK]", flush=True)

        elif msg_type == "result":
            duration = data.get("duration_ms", 0) / 1000
            cost = data.get("total_cost_usd", 0)
            print(f"\n[Done: {duration:.1f}s, ${cost:.4f}]", flush=True)

    except json.JSONDecodeError:
        print(line, flush=True)


def run_claude_interactive(prompt: str) -> None:
    """Run Claude in interactive mode (for init)."""
    cmd = [CLAUDE_CMD, "--dangerously-skip-permissions", prompt]
    subprocess.run(cmd, cwd=SCRIPT_DIR)


def run_claude_streaming(prompt: str, model: str) -> None:
    """Run Claude in print mode with streaming JSON output."""
    cmd = [
        CLAUDE_CMD,
        "--print", prompt,
        "--model", model,
        "--dangerously-skip-permissions",
        "--output-format", "stream-json",
        "--verbose",
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=SCRIPT_DIR,
    )

    for line in process.stdout:
        line = line.strip()
        if line:
            parse_stream_json(line)

    process.wait()


def has_incomplete_stories() -> bool:
    """Check if prd.json has any stories with passes: false."""
    if not PRD_FILE.exists():
        return False
    try:
        with open(PRD_FILE) as f:
            prd = json.load(f)
        stories = prd.get("stories", [])
        return any(not story.get("passes", False) for story in stories)
    except (json.JSONDecodeError, KeyError):
        return False


def cmd_init(args) -> int:
    """Initialize a new project."""
    if INIT_MARKER.exists():
        print(f"Already initialized. To re-run: rm {INIT_MARKER} && ./ralph.py init")
        return 0

    print("Ralph - Project Initializer")
    print("===========================\n")

    if not INIT_PROMPT_FILE.exists():
        print(f"Error: {INIT_PROMPT_FILE} not found")
        return 1

    prompt = INIT_PROMPT_FILE.read_text()
    run_claude_interactive(prompt)

    # Check if initialized
    if INIT_MARKER.exists():
        print("\nDone! Run ./ralph.py run to start coding.")
        return 0

    # Ask user to confirm
    response = input("\nDid initialization complete? (y/n) ").strip().lower()
    if response == "y":
        INIT_MARKER.touch()
        print("\nDone! Run ./ralph.py run to start coding.")
        return 0
    else:
        print("\nRun ./ralph.py init again to retry.")
        return 1


def cmd_run(args) -> int:
    """Run the coding loop."""
    if not INIT_MARKER.exists():
        print("Not initialized. Run ./ralph.py init first.")
        return 1

    if not PROMPT_FILE.exists():
        print(f"Error: {PROMPT_FILE} not found")
        return 1

    prompt = PROMPT_FILE.read_text()

    print("Ralph - Coding Loop")
    print("===================")
    print(f"Max iterations: {args.iterations}")
    print(f"Model: {args.model}")

    for i in range(1, args.iterations + 1):
        print(f"\n>>> Iteration {i} of {args.iterations}")
        print("-" * 35)

        run_claude_streaming(prompt, args.model)

        if not has_incomplete_stories():
            print("\n===================")
            print(f"Ralph completed all stories after {i} iteration(s)")
            print("===================")
            return 0

        print(f"\n>>> Iteration {i} complete, continuing...")

    print("\n===================")
    print(f"Ralph reached max iterations ({args.iterations}) without completing")
    print("Check progress.txt and prd.json for status")
    print("===================")
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Ralph - Autonomous Coding Agent Loop",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./ralph.py init              Initialize a new project
  ./ralph.py run               Run coding loop (10 iterations)
  ./ralph.py run -n 5          Run 5 iterations
  ./ralph.py run --model sonnet  Use sonnet model
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init command
    subparsers.add_parser("init", help="Initialize a new project")

    # run command
    run_parser = subparsers.add_parser("run", help="Run the coding loop")
    run_parser.add_argument(
        "-n", "--iterations",
        type=int,
        default=10,
        help="Maximum iterations (default: 10)",
    )
    run_parser.add_argument(
        "--model",
        default="opus",
        help="Model to use (default: opus)",
    )

    args = parser.parse_args()

    if args.command == "init":
        return cmd_init(args)
    elif args.command == "run":
        return cmd_run(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
