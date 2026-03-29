# Questions for Team

## 1. JFrog access for installing core SDK locally

I need to install `dr-financeos-sdk` (the Python async wrapper from dr-finance-os) locally so I can develop `dr-datarails-sdk` on top of it.

**What I tried:**
- `uv auth login` with my JFrog token for `dr-pypi` and `dr-financeos-sdk-python-async` repos
- Credentials inline in the URL
- All return 401 Unauthorized

**What I need:**
- Either: JFrog credentials/token that has read access to the `dr-financeos-sdk-python-async` repo
- Or: the correct repo URL and auth method to install `dr-financeos-sdk` locally
- Or: just the pip/uv install command that works (someone on the team must have this working)

**Who to ask:** DevOps or whoever set up the `sdk-publish.yml` CI pipeline in `dr-finance-os`.

## 2. Publishing `dr-datarails-sdk` to JFrog

Once I can install the core SDK, I need to publish our new `dr-datarails-sdk` package to JFrog so the Claude Code plugin can install it.

**What I need:**
- A new JFrog repo for the package (e.g., `dr-datarails-sdk-python`), or permission to publish to an existing repo
- CI/CD setup similar to `dr-finance-os/sdk-publish.yml`

**Who to ask:** Same as above.

## 3. OAuth client_id registration

The `/dr-auth` skill in the Claude Code plugin needs a `client_id` registered with `auth.datarails.com`.

**What I need:**
- Register client_id `claude-code` (or similar) with allowed callback URL `http://localhost:9876/callback`
- Same OAuth PKCE flow that `Lovable-app` uses

**Who to ask:** Whoever manages auth.datarails.com / Descope configuration.
