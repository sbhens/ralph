#!/bin/bash
# iOS Project - Dependency Installation Script
# This script is generated/updated by `./ralph.py init`

set -e

echo "=== iOS Development Setup ==="
echo ""

# Check Xcode
echo "Checking Xcode..."
if ! command -v xcodebuild &> /dev/null; then
    echo "ERROR: Xcode is not installed. Please install from the App Store."
    exit 1
fi

XCODE_VERSION=$(xcodebuild -version | head -1)
echo "  Found: $XCODE_VERSION"

# Check for Xcode command line tools
echo "Checking Xcode Command Line Tools..."
if ! xcode-select -p &> /dev/null; then
    echo "Installing Xcode Command Line Tools..."
    xcode-select --install
fi
echo "  OK"

# Accept Xcode license if needed
echo "Checking Xcode license..."
sudo xcodebuild -license accept 2>/dev/null || true
echo "  OK"

# Check for iOS Simulator
echo "Checking iOS Simulator..."
if ! xcrun simctl list devices | grep -q "iPhone"; then
    echo "WARNING: No iPhone simulators found. Please install via Xcode > Settings > Platforms"
fi
echo "  OK"

# Check macOS version
echo "Checking macOS version..."
MACOS_VERSION=$(sw_vers -productVersion)
echo "  Found: macOS $MACOS_VERSION"

# Check Node.js for XcodeBuildMCP
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "  Found: Node.js $NODE_VERSION"
else
    echo "WARNING: Node.js not found. Install for XcodeBuildMCP support."
fi

# Verify XcodeBuildMCP is configured
echo "Checking XcodeBuildMCP..."
if claude mcp list 2>/dev/null | grep -q "XcodeBuildMCP"; then
    echo "  OK"
else
    echo "  Installing XcodeBuildMCP..."
    claude mcp add XcodeBuildMCP -- npx -y xcodebuildmcp@latest
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To build:  make build"
echo "To test:   make test"
echo "To run:    make run"
echo ""
