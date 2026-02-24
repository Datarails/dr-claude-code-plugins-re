#!/bin/bash
# Build Cowork ZIP plugin package
#
# Usage: ./build-cowork-zip.sh [version]
# Output: datarails-finance-os-cowork-plugin.zip

set -e

VERSION="${1:-2.0.0}"
OUTPUT="datarails-finance-os-cowork-plugin.zip"
STAGING_DIR="datarails-finance-os-cowork-plugin"

echo "Building Cowork plugin ZIP v${VERSION}..."

# Clean previous build
rm -rf "$STAGING_DIR" "$OUTPUT"

# Create staging directory
mkdir -p "$STAGING_DIR"

# Copy plugin files
cp -r .claude-plugin "$STAGING_DIR/"
cp -r skills "$STAGING_DIR/"
cp -r commands "$STAGING_DIR/"
cp -r agents "$STAGING_DIR/"
cp -r config "$STAGING_DIR/"
cp CLAUDE.md "$STAGING_DIR/"
cp README.md "$STAGING_DIR/"

# Remove client-specific profiles from the package
rm -f "$STAGING_DIR/config/client-profiles/"*.json
touch "$STAGING_DIR/config/client-profiles/.gitkeep"

# Create ZIP
zip -r "$OUTPUT" "$STAGING_DIR/" -x "*.DS_Store" "*__pycache__*"

# Clean up staging
rm -rf "$STAGING_DIR"

echo ""
echo "Built: $OUTPUT"
echo "Size: $(du -h "$OUTPUT" | cut -f1)"
echo ""
echo "Upload this ZIP to Cowork via the plugin upload UI."
