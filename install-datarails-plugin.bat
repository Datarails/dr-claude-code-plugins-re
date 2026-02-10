@echo off
REM ============================================================================
REM Datarails Finance OS Plugin - Installer / Updater for Windows
REM ============================================================================
REM Double-click this file to install or update the plugin.
REM Safe to run multiple times - it will update to the latest version.
REM ============================================================================

title Datarails Finance OS Plugin Installer

echo.
echo ============================================
echo   Datarails Finance OS Plugin Installer
echo ============================================
echo.

REM Run the main logic in PowerShell (for proper JSON/zip handling)
powershell -ExecutionPolicy Bypass -Command ^
"& {" ^
"$ErrorActionPreference = 'Stop';" ^
"$repo = 'Datarails/dr-claude-code-plugins-re';" ^
"$pluginName = 'datarails-finance-os';" ^
"$claudeSupport = Join-Path $env:APPDATA 'Claude';" ^
"$claudeConfig = Join-Path $claudeSupport 'claude_desktop_config.json';" ^
"" ^
"# 1. Check for uv" ^
"$uvPath = Get-Command uv -ErrorAction SilentlyContinue;" ^
"if (-not $uvPath) {" ^
"    Write-Host 'Warning: uv is not installed.' -ForegroundColor Yellow;" ^
"    Write-Host 'The MCP server needs uv to run. Install it from: https://astral.sh/uv';" ^
"    Write-Host '';" ^
"}" ^
"" ^
"# 2. Download latest release" ^
"Write-Host 'Fetching latest release...' -ForegroundColor Cyan;" ^
"try {" ^
"    $release = Invoke-RestMethod -Uri \"https://api.github.com/repos/$repo/releases/latest\" -UseBasicParsing;" ^
"} catch {" ^
"    Write-Host 'Error: Could not fetch release info from GitHub.' -ForegroundColor Red;" ^
"    Write-Host 'Make sure you have internet access.';" ^
"    Read-Host 'Press Enter to exit';" ^
"    exit 1;" ^
"}" ^
"" ^
"$zipAsset = $release.assets | Where-Object { $_.name -like '*.zip' -and $_.name -like '*datarails*' } | Select-Object -First 1;" ^
"if (-not $zipAsset) {" ^
"    Write-Host 'Error: No plugin zip found in the latest release.' -ForegroundColor Red;" ^
"    Read-Host 'Press Enter to exit';" ^
"    exit 1;" ^
"}" ^
"" ^
"Write-Host \"Found release: $($release.tag_name)\" -ForegroundColor Green;" ^
"" ^
"# Download to temp directory" ^
"$tmpDir = Join-Path $env:TEMP ('datarails-plugin-' + [guid]::NewGuid().ToString('N').Substring(0,8));" ^
"New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null;" ^
"$zipPath = Join-Path $tmpDir 'plugin.zip';" ^
"" ^
"Write-Host 'Downloading plugin...';" ^
"Invoke-WebRequest -Uri $zipAsset.browser_download_url -OutFile $zipPath -UseBasicParsing;" ^
"" ^
"Write-Host 'Extracting...';" ^
"$extractDir = Join-Path $tmpDir 'extracted';" ^
"Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force;" ^
"" ^
"# Find plugin root" ^
"$pluginJson = Get-ChildItem -Path $extractDir -Recurse -Filter 'plugin.json' | Where-Object { $_.Directory.Name -eq '.claude-plugin' } | Select-Object -First 1;" ^
"if (-not $pluginJson) {" ^
"    Write-Host 'Error: Could not find plugin files in the downloaded zip.' -ForegroundColor Red;" ^
"    Remove-Item -Path $tmpDir -Recurse -Force -ErrorAction SilentlyContinue;" ^
"    Read-Host 'Press Enter to exit';" ^
"    exit 1;" ^
"}" ^
"$pluginSrc = $pluginJson.Directory.Parent.FullName;" ^
"" ^
"# 3. Find Cowork plugin directory" ^
"Write-Host '';" ^
"Write-Host 'Finding Cowork plugin directory...' -ForegroundColor Cyan;" ^
"" ^
"$coworkBase = Join-Path $claudeSupport 'local-agent-mode-sessions';" ^
"$pluginDest = $null;" ^
"" ^
"if (Test-Path $coworkBase) {" ^
"    $uploadsDir = Get-ChildItem -Path $coworkBase -Recurse -Directory -Filter 'local-desktop-app-uploads' | Select-Object -First 1;" ^
"    if ($uploadsDir) {" ^
"        $pluginDest = Join-Path $uploadsDir.FullName $pluginName;" ^
"    }" ^
"}" ^
"" ^
"if (-not $pluginDest) {" ^
"    Write-Host 'Cowork plugin directory not found.' -ForegroundColor Yellow;" ^
"    Write-Host 'Open Claude Desktop with Cowork enabled, then run this installer again.';" ^
"    Remove-Item -Path $tmpDir -Recurse -Force -ErrorAction SilentlyContinue;" ^
"    Read-Host 'Press Enter to exit';" ^
"    exit 1;" ^
"}" ^
"" ^
"# 4. Install / Update" ^
"Write-Host \"Installing to: $pluginDest\" -ForegroundColor Green;" ^
"" ^
"# Backup client profiles" ^
"$profilesBackup = $null;" ^
"$profilesDir = Join-Path $pluginDest 'config\client-profiles';" ^
"if (Test-Path $profilesDir) {" ^
"    $profilesBackup = Join-Path $tmpDir 'profiles-backup';" ^
"    Copy-Item -Path $profilesDir -Destination $profilesBackup -Recurse -Force;" ^
"    Write-Host 'Backed up client profiles';" ^
"}" ^
"" ^
"# Remove old plugin" ^
"if (Test-Path $pluginDest) {" ^
"    Remove-Item -Path $pluginDest -Recurse -Force;" ^
"    Write-Host 'Removed old version';" ^
"}" ^
"" ^
"# Copy new plugin" ^
"Copy-Item -Path $pluginSrc -Destination $pluginDest -Recurse -Force;" ^
"Write-Host 'Installed new version';" ^
"" ^
"# Restore client profiles" ^
"if ($profilesBackup -and (Test-Path $profilesBackup)) {" ^
"    $destProfiles = Join-Path $pluginDest 'config\client-profiles';" ^
"    if (-not (Test-Path $destProfiles)) { New-Item -ItemType Directory -Path $destProfiles -Force | Out-Null }" ^
"    Copy-Item -Path (Join-Path $profilesBackup '*') -Destination $destProfiles -Recurse -Force;" ^
"    Write-Host 'Restored client profiles';" ^
"}" ^
"" ^
"# 5. Update claude_desktop_config.json" ^
"Write-Host '';" ^
"Write-Host 'Checking MCP server configuration...' -ForegroundColor Cyan;" ^
"" ^
"$mcpDir = (Join-Path $pluginDest 'mcp-server') -replace '\\', '/';" ^
"$configDir = (Join-Path $pluginDest 'config') -replace '\\', '/';" ^
"" ^
"$mcpEntry = @{" ^
"    command = 'uv';" ^
"    args = @('--directory', $mcpDir, 'run', 'datarails-mcp', 'serve');" ^
"    env = @{ DATARAILS_CONFIG_DIR = $configDir }" ^
"};" ^
"" ^
"if (Test-Path $claudeConfig) {" ^
"    $config = Get-Content $claudeConfig -Raw | ConvertFrom-Json;" ^
"    if (-not $config.mcpServers) {" ^
"        $config | Add-Member -NotePropertyName 'mcpServers' -NotePropertyValue @{} -Force;" ^
"    }" ^
"    $config.mcpServers | Add-Member -NotePropertyName $pluginName -NotePropertyValue $mcpEntry -Force;" ^
"    $config | ConvertTo-Json -Depth 10 | Set-Content $claudeConfig -Encoding UTF8;" ^
"    Write-Host 'MCP server configured' -ForegroundColor Green;" ^
"} else {" ^
"    if (-not (Test-Path $claudeSupport)) { New-Item -ItemType Directory -Path $claudeSupport -Force | Out-Null }" ^
"    $config = @{ mcpServers = @{ $pluginName = $mcpEntry } };" ^
"    $config | ConvertTo-Json -Depth 10 | Set-Content $claudeConfig -Encoding UTF8;" ^
"    Write-Host 'Created config with MCP server' -ForegroundColor Green;" ^
"}" ^
"" ^
"# Cleanup" ^
"Remove-Item -Path $tmpDir -Recurse -Force -ErrorAction SilentlyContinue;" ^
"" ^
"# 6. Done!" ^
"Write-Host '';" ^
"Write-Host '============================================' -ForegroundColor Green;" ^
"Write-Host \"  Installation complete! ($($release.tag_name))\" -ForegroundColor Green;" ^
"Write-Host '============================================' -ForegroundColor Green;" ^
"Write-Host '';" ^
"Write-Host 'Next steps:';" ^
"Write-Host '  1. Restart Claude Desktop';" ^
"Write-Host '  2. Open a Cowork conversation';" ^
"Write-Host '  3. Ask: \"What can you do with Datarails?\"';" ^
"Write-Host '';" ^
"Write-Host 'To update later, just double-click this installer again.';" ^
"}"

echo.
pause
