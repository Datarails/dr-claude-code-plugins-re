#!/usr/bin/env python3
"""Datarails Finance OS Plugin - Setup Wizard

Interactive setup wizard that guides users through:
1. Checking prerequisites (Python, uv)
2. Verifying skills are configured
3. Authenticating with Datarails
4. Testing the connection
5. Showing next steps

Usage:
    python setup.py
    # or
    ./setup.py
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_step(num, text):
    print(f"\n{Colors.BOLD}Step {num}: {text}{Colors.END}")
    print("-" * 40)

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}!{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.BLUE}•{Colors.END} {text}")

def run_command(cmd, capture=True, check=False):
    """Run a shell command and return result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def prompt_yes_no(question, default=True):
    """Ask a yes/no question."""
    default_str = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{question} [{default_str}]: ").strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print("Please answer 'yes' or 'no'")

def prompt_choice(question, choices):
    """Ask user to choose from a list."""
    print(f"\n{question}")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")
    while True:
        try:
            answer = input(f"Enter choice [1-{len(choices)}]: ").strip()
            idx = int(answer) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
        except ValueError:
            pass
        print(f"Please enter a number between 1 and {len(choices)}")

def get_plugin_dir():
    """Get the plugin directory (where this script is located)."""
    return Path(__file__).parent.resolve()

def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (need 3.10+)")
        return False

def check_uv():
    """Check if uv is installed."""
    success, output, _ = run_command("uv --version")
    if success:
        print_success(f"uv {output.split()[-1] if output else 'installed'}")
        return True
    else:
        print_error("uv not found")
        print_info("Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

def check_claude_code():
    """Check if Claude Code is installed."""
    success, _, _ = run_command("which claude")
    if success:
        print_success("Claude Code installed")
        return True
    else:
        print_warning("Claude Code not found in PATH")
        print_info("Install from: https://claude.ai/code")
        return False

def check_skills_setup(plugin_dir):
    """Check if skills are properly configured."""
    skills_dir = plugin_dir / ".claude" / "skills"

    if skills_dir.exists():
        # Check if symlinks are valid
        expected_skills = ["dr-auth", "dr-tables", "dr-profile", "dr-anomalies", "dr-query", "dr-extract", "dr-learn"]
        all_valid = True
        for skill in expected_skills:
            skill_path = skills_dir / skill
            if skill_path.exists():
                print_success(f"Skill: /{skill}")
            else:
                print_error(f"Skill missing: /{skill}")
                all_valid = False
        return all_valid
    else:
        print_error("Skills directory not found")
        return False

def setup_skills(plugin_dir):
    """Set up skills symlinks if needed."""
    claude_dir = plugin_dir / ".claude"
    skills_dir = claude_dir / "skills"
    source_skills = plugin_dir / "skills"

    # Create .claude directory if needed
    claude_dir.mkdir(exist_ok=True)

    # Remove old skills symlink/directory if it exists
    if skills_dir.exists() or skills_dir.is_symlink():
        if skills_dir.is_symlink():
            skills_dir.unlink()
        else:
            shutil.rmtree(skills_dir)

    # Create skills directory
    skills_dir.mkdir(exist_ok=True)

    # Create individual skill symlinks
    skill_names = {
        "auth": "dr-auth",
        "tables": "dr-tables",
        "profile": "dr-profile",
        "anomalies": "dr-anomalies",
        "query": "dr-query",
        "extract": "dr-extract",
        "learn": "dr-learn"
    }

    for source_name, target_name in skill_names.items():
        source = source_skills / source_name
        target = skills_dir / target_name
        if source.exists():
            # Create relative symlink
            rel_path = os.path.relpath(source, skills_dir)
            target.symlink_to(rel_path)
            print_success(f"Created symlink: {target_name} -> {rel_path}")

    return True

def check_authentication(plugin_dir):
    """Check if user is authenticated with Datarails."""
    success, output, _ = run_command("uvx datarails-finance-os-mcp status --json")

    if success and output:
        try:
            status = json.loads(output)
            if status.get("authenticated"):
                env = status.get("environment", "unknown")
                print_success(f"Authenticated to {env}")
                return True, env
        except json.JSONDecodeError:
            pass

    print_warning("Not authenticated")
    return False, None

def run_authentication(plugin_dir, env="dev"):
    """Run the authentication flow."""
    print_info(f"Authenticating to {env} environment...")
    print_info("Make sure you're logged into Datarails in your browser!")
    print()

    # Run auth command interactively
    result = subprocess.run(
        f"uvx datarails-finance-os-mcp auth --env {env}",
        shell=True
    )

    return result.returncode == 0

def test_connection(plugin_dir):
    """Test the connection by listing tables."""
    print_info("Testing connection by listing tables...")

    success, output, error = run_command(
        "uvx datarails-finance-os-mcp status --json"
    )

    if success and "True" in output:
        print_success("Connection test passed!")
        return True
    else:
        print_warning("Connection test failed - but auth may still work")
        return False

def show_next_steps(plugin_dir):
    """Show next steps to the user."""
    print_header("Setup Complete!")

    print(f"""
{Colors.GREEN}You're all set!{Colors.END} Here's how to use the plugin:

{Colors.BOLD}1. Start Claude Code from this directory:{Colors.END}
   cd {plugin_dir}
   claude

{Colors.BOLD}2. Learn your data structure (first time):{Colors.END}
   /dr-learn               # Discover tables and create client profile

{Colors.BOLD}3. Try these commands:{Colors.END}
   /dr-tables              # List all Finance OS tables
   /dr-profile <table_id>  # Profile a table
   /dr-query <table_id> --sample  # Get sample data
   /dr-extract --year 2025 # Extract financial data to Excel

{Colors.BOLD}4. Multi-environment:{Colors.END}
   /dr-auth --list         # See all environments
   /dr-auth --env app      # Authenticate to production

{Colors.BOLD}Documentation:{Colors.END}
   - README.md   - Overview and commands
   - SETUP.md    - Detailed setup guide
   - CLAUDE.md   - Plugin instructions

{Colors.BOLD}Need help?{Colors.END}
   - GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
""")

def main():
    """Main setup wizard flow."""
    print_header("Datarails Finance OS Plugin Setup")

    plugin_dir = get_plugin_dir()
    print_info(f"Plugin directory: {plugin_dir}")

    # Step 1: Check prerequisites
    print_step(1, "Checking Prerequisites")

    python_ok = check_python()
    uv_ok = check_uv()
    claude_ok = check_claude_code()

    if not python_ok or not uv_ok:
        print()
        print_error("Missing required prerequisites. Please install them and run setup again.")
        sys.exit(1)

    if not claude_ok:
        if not prompt_yes_no("Continue without Claude Code?", default=False):
            sys.exit(1)

    # Step 2: Check/setup skills
    print_step(2, "Checking Skills Configuration")

    skills_ok = check_skills_setup(plugin_dir)

    if not skills_ok:
        print()
        if prompt_yes_no("Set up skills now?"):
            setup_skills(plugin_dir)
            print()
            check_skills_setup(plugin_dir)

    # Step 3: Authentication
    print_step(3, "Authentication")

    auth_ok, current_env = check_authentication(plugin_dir)

    if not auth_ok:
        print()
        if prompt_yes_no("Authenticate now?"):
            # Choose environment
            env = prompt_choice(
                "Which environment?",
                ["dev (Development)", "app (Production)", "demo (Demo)", "testapp (Test App)"]
            ).split()[0]

            print()
            print_info("Opening browser authentication...")
            print_info("Make sure you're logged into Datarails in your browser!")
            input("\nPress Enter when you're logged in...")

            if run_authentication(plugin_dir, env):
                print()
                auth_ok, current_env = check_authentication(plugin_dir)

    # Step 4: Test connection (optional)
    if auth_ok:
        print_step(4, "Testing Connection")

        if prompt_yes_no("Test the connection?"):
            test_connection(plugin_dir)

    # Step 5: Show next steps
    show_next_steps(plugin_dir)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(1)
