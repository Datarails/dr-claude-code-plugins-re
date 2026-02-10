#!/bin/bash
# ============================================================================
# Datarails Finance OS Plugin - Installer / Updater for Mac
# ============================================================================
# Double-click this file to install or update the plugin.
# Safe to run multiple times - it will update to the latest version.
# ============================================================================

set -euo pipefail

REPO="Datarails/dr-claude-code-plugins-re"
PLUGIN_NAME="datarails-finance-os"
CLAUDE_SUPPORT_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG="$CLAUDE_SUPPORT_DIR/claude_desktop_config.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Datarails Finance OS Plugin Installer${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# -------------------------------------------------------------------
# 1. Check prerequisites
# -------------------------------------------------------------------
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is not installed. Please install it first.${NC}"
    exit 1
fi

if ! command -v unzip &> /dev/null; then
    echo -e "${RED}Error: unzip is not installed. Please install it first.${NC}"
    exit 1
fi

# Check for uv (needed to run the MCP server)
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}Warning: 'uv' is not installed.${NC}"
    echo "The MCP server needs 'uv' to run. Install it with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Continuing with plugin installation..."
    echo ""
fi

# -------------------------------------------------------------------
# 2. Download latest release
# -------------------------------------------------------------------
echo -e "${BLUE}Fetching latest release...${NC}"

# Get the latest release info from GitHub API
RELEASE_JSON=$(curl -sf "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null || true)

if [ -z "$RELEASE_JSON" ]; then
    echo -e "${RED}Error: Could not fetch release info from GitHub.${NC}"
    echo "Make sure you have internet access."
    echo "If this is a private repo, install the 'gh' CLI and run: gh auth login"
    exit 1
fi

# Extract the zip download URL (asset named datarails-finance-os-*.zip)
ZIP_URL=$(echo "$RELEASE_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for asset in data.get('assets', []):
    if asset['name'].endswith('.zip') and 'datarails' in asset['name'].lower():
        print(asset['browser_download_url'])
        break
" 2>/dev/null || true)

if [ -z "$ZIP_URL" ]; then
    echo -e "${RED}Error: No plugin zip found in the latest release.${NC}"
    echo "Check: https://github.com/$REPO/releases"
    exit 1
fi

RELEASE_TAG=$(echo "$RELEASE_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tag_name', 'unknown'))" 2>/dev/null || echo "unknown")
echo -e "Found release: ${GREEN}$RELEASE_TAG${NC}"

# Download to temp directory
TMPDIR_PATH=$(mktemp -d)
trap "rm -rf '$TMPDIR_PATH'" EXIT

echo "Downloading plugin..."
curl -sL "$ZIP_URL" -o "$TMPDIR_PATH/plugin.zip"

echo "Extracting..."
unzip -qo "$TMPDIR_PATH/plugin.zip" -d "$TMPDIR_PATH/extracted"

# Find the plugin root (the directory containing .claude-plugin/)
PLUGIN_SRC=$(find "$TMPDIR_PATH/extracted" -name "plugin.json" -path "*/.claude-plugin/*" -print -quit 2>/dev/null | xargs dirname 2>/dev/null | xargs dirname 2>/dev/null || true)

if [ -z "$PLUGIN_SRC" ] || [ ! -d "$PLUGIN_SRC" ]; then
    echo -e "${RED}Error: Could not find plugin files in the downloaded zip.${NC}"
    exit 1
fi

# -------------------------------------------------------------------
# 3. Find Cowork plugin directory
# -------------------------------------------------------------------
echo ""
echo -e "${BLUE}Finding Cowork plugin directory...${NC}"

COWORK_BASE="$CLAUDE_SUPPORT_DIR/local-agent-mode-sessions"
PLUGIN_DEST=""

if [ -d "$COWORK_BASE" ]; then
    # Find the uploads directory (may have UUID-based paths)
    UPLOADS_DIR=$(find "$COWORK_BASE" -type d -name "local-desktop-app-uploads" -print -quit 2>/dev/null || true)
    if [ -n "$UPLOADS_DIR" ]; then
        PLUGIN_DEST="$UPLOADS_DIR/$PLUGIN_NAME"
    fi
fi

if [ -z "$PLUGIN_DEST" ]; then
    echo -e "${YELLOW}Cowork plugin directory not found.${NC}"
    echo "This usually means Claude Desktop hasn't been used with Cowork yet."
    echo ""
    echo "Options:"
    echo "  1. Open Claude Desktop, enable Cowork, then run this installer again"
    echo "  2. Or install manually: copy the plugin to the Cowork uploads directory"
    echo ""
    echo "The downloaded plugin is at: $PLUGIN_SRC"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# -------------------------------------------------------------------
# 4. Install / Update plugin
# -------------------------------------------------------------------
echo -e "Installing to: ${GREEN}$PLUGIN_DEST${NC}"

# Backup client profiles if they exist (user's auth/config data)
PROFILES_BACKUP=""
if [ -d "$PLUGIN_DEST/config/client-profiles" ]; then
    PROFILES_BACKUP="$TMPDIR_PATH/profiles-backup"
    mkdir -p "$PROFILES_BACKUP"
    cp -R "$PLUGIN_DEST/config/client-profiles/"* "$PROFILES_BACKUP/" 2>/dev/null || true
    echo "Backed up client profiles"
fi

# Remove old plugin (if updating)
if [ -d "$PLUGIN_DEST" ]; then
    rm -rf "$PLUGIN_DEST"
    echo "Removed old version"
fi

# Copy new plugin
cp -R "$PLUGIN_SRC" "$PLUGIN_DEST"
echo "Installed new version"

# Restore client profiles
if [ -n "$PROFILES_BACKUP" ] && [ -d "$PROFILES_BACKUP" ]; then
    mkdir -p "$PLUGIN_DEST/config/client-profiles"
    cp -R "$PROFILES_BACKUP/"* "$PLUGIN_DEST/config/client-profiles/" 2>/dev/null || true
    echo "Restored client profiles"
fi

# -------------------------------------------------------------------
# 5. Update claude_desktop_config.json with MCP server entry
# -------------------------------------------------------------------
echo ""
echo -e "${BLUE}Checking MCP server configuration...${NC}"

# Determine the MCP server directory path
MCP_DIR="$PLUGIN_DEST/mcp-server"

if [ -f "$CLAUDE_CONFIG" ]; then
    # Check if datarails-finance-os MCP server is already configured
    if python3 -c "
import json, sys
with open('$CLAUDE_CONFIG') as f:
    config = json.load(f)
servers = config.get('mcpServers', {})
if '$PLUGIN_NAME' in servers:
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
        echo "MCP server already configured - updating path"
        # Update the directory path in case it changed
        python3 -c "
import json
config_path = '$CLAUDE_CONFIG'
with open(config_path) as f:
    config = json.load(f)
config.setdefault('mcpServers', {})
config['mcpServers']['$PLUGIN_NAME'] = {
    'command': 'uv',
    'args': ['--directory', '$MCP_DIR', 'run', 'datarails-mcp', 'serve'],
    'env': {
        'DATARAILS_CONFIG_DIR': '$PLUGIN_DEST/config'
    }
}
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null
        echo -e "${GREEN}MCP server path updated${NC}"
    else
        echo "Adding MCP server to config..."
        python3 -c "
import json
config_path = '$CLAUDE_CONFIG'
with open(config_path) as f:
    config = json.load(f)
config.setdefault('mcpServers', {})
config['mcpServers']['$PLUGIN_NAME'] = {
    'command': 'uv',
    'args': ['--directory', '$MCP_DIR', 'run', 'datarails-mcp', 'serve'],
    'env': {
        'DATARAILS_CONFIG_DIR': '$PLUGIN_DEST/config'
    }
}
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null
        echo -e "${GREEN}MCP server added to config${NC}"
    fi
else
    echo "Creating claude_desktop_config.json..."
    mkdir -p "$CLAUDE_SUPPORT_DIR"
    python3 -c "
import json
config = {
    'mcpServers': {
        '$PLUGIN_NAME': {
            'command': 'uv',
            'args': ['--directory', '$MCP_DIR', 'run', 'datarails-mcp', 'serve'],
            'env': {
                'DATARAILS_CONFIG_DIR': '$PLUGIN_DEST/config'
            }
        }
    }
}
with open('$CLAUDE_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null
    echo -e "${GREEN}Created config with MCP server${NC}"
fi

# -------------------------------------------------------------------
# 6. Done!
# -------------------------------------------------------------------
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Installation complete! ($RELEASE_TAG)${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Desktop"
echo "  2. Open a Cowork conversation"
echo "  3. Ask: \"What can you do with Datarails?\""
echo ""
echo "To update later, just double-click this installer again."
echo ""
read -p "Press Enter to close..."
