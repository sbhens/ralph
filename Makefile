# iOS App Makefile Template
# Update PROJECT_DIR, SCHEME, and SIMULATOR for your project

PROJECT_DIR = MyApp
PROJECT = $(PROJECT_DIR)/$(PROJECT_DIR).xcodeproj
SCHEME = $(PROJECT_DIR)
SIMULATOR = iPhone 16
DESTINATION = platform=iOS Simulator,name=$(SIMULATOR)

.PHONY: build test run clean deploy devices help

# Default target
all: build

# Build the project for simulator
build:
	@echo "Building $(SCHEME)..."
	@xcodebuild -project $(PROJECT) \
		-scheme $(SCHEME) \
		-destination '$(DESTINATION)' \
		-quiet \
		build

# Run unit tests
test:
	@echo "Running tests..."
	@xcodebuild -project $(PROJECT) \
		-scheme $(SCHEME) \
		-destination '$(DESTINATION)' \
		-quiet \
		test

# Build and run in simulator
run: build
	@echo "Launching simulator..."
	@xcrun simctl boot "$(SIMULATOR)" 2>/dev/null || true
	@open -a Simulator
	@echo "Installing app..."
	@xcrun simctl install booted "$$(find ~/Library/Developer/Xcode/DerivedData -name '$(SCHEME).app' -type d | head -1)"
	@echo "Launching app..."
	@xcrun simctl launch booted com.$(shell echo $(SCHEME) | tr '[:upper:]' '[:lower:]').app

# Clean build artifacts
clean:
	@echo "Cleaning..."
	@xcodebuild -project $(PROJECT) \
		-scheme $(SCHEME) \
		-quiet \
		clean
	@rm -rf ~/Library/Developer/Xcode/DerivedData/$(PROJECT_DIR)-*

# Build for release
release:
	@echo "Building release..."
	@xcodebuild -project $(PROJECT) \
		-scheme $(SCHEME) \
		-destination '$(DESTINATION)' \
		-configuration Release \
		-quiet \
		build

# Show available simulators
simulators:
	@xcrun simctl list devices available | grep -E "iPhone|iPad"

# List connected iOS devices
devices:
	@echo "Connected devices:"
	@xcrun xctrace list devices 2>/dev/null | sed -n '/== Devices ==/,/== Simulators ==/p' | grep -v "==" | grep -v "MacBook" | grep -v "^$$" || echo "No devices connected"

# Deploy to connected iOS device
deploy:
	@echo "Building and deploying to connected device..."
	@DEVICE_ID=$$(xcrun xctrace list devices 2>/dev/null | sed -n '/== Devices ==/,/== Simulators ==/p' | grep -v "==" | grep -v "MacBook" | grep -v "^$$" | head -1 | sed 's/.*(\([^)]*\))$$/\1/'); \
	if [ -z "$$DEVICE_ID" ]; then \
		echo "Error: No iOS device connected"; \
		exit 1; \
	fi; \
	echo "Building for device: $$DEVICE_ID"; \
	xcodebuild -project $(PROJECT) \
		-scheme $(SCHEME) \
		-destination "id=$$DEVICE_ID" \
		-allowProvisioningUpdates \
		build && \
	echo "Installing on device..." && \
	APP_PATH=$$(find ~/Library/Developer/Xcode/DerivedData/$(PROJECT_DIR)-*/Build/Products/Debug-iphoneos -name "$(SCHEME).app" -type d 2>/dev/null | head -1) && \
	xcrun devicectl device install app --device "$$DEVICE_ID" "$$APP_PATH"

# Help
help:
	@echo "iOS App Makefile"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build       Build the app for simulator (default)"
	@echo "  test        Run unit tests"
	@echo "  run         Build and run in simulator"
	@echo "  deploy      Build and deploy to connected iOS device"
	@echo "  devices     List connected iOS devices"
	@echo "  clean       Clean build artifacts"
	@echo "  release     Build release configuration"
	@echo "  simulators  List available simulators"
	@echo "  help        Show this help message"
