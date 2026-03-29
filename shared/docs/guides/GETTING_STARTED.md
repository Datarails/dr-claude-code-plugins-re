# Getting Started with Datarails FinanceOS Plugin

**Your first 15 minutes: from installation to your first financial report.**

---

## What You'll Accomplish

By the end of this guide, you will have:

1. Connected to your Datarails environment
2. Pulled your first live financial snapshot
3. Run deeper analysis (expenses, revenue, budget variance)
4. Set up your environment profile for advanced features
5. Generated a comprehensive FP&A Intelligence Workbook

**Time estimate:** ~15 minutes for Steps 1-3 (immediate value), ~25 minutes total including Steps 4-5.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Datarails account** | Active login at your Datarails environment |
| **Claude Desktop** _or_ **Claude Code** | Cowork: install plugin via ZIP or marketplace. Claude Code: install the plugin first (see [README](../../README.md)) |

### Which Track Are You?

| Track | Who It's For | What You Need |
|-------|-------------|---------------|
| **Cowork** | Finance teams, business users | Just a browser - no terminal required |
| **Claude Code** | Developers, power users | Terminal + plugin installed |

Both tracks access the same data and produce the same quality results.

---

## Step 1: Connect to Datarails

**Time:** ~2 minutes

### Claude Desktop Track (Cowork and Claude Code)

The plugin automatically configures a Datarails connector when installed. To connect:

1. Click the **"+"** button next to the prompt
2. Select **Connectors**
3. Find **Datarails** and click **Connect**
4. A browser window opens — log in with your Datarails credentials
5. After login, return to Claude Desktop — you're connected

You can also manage connectors from **Settings > Connectors**.

**If the connector doesn't appear:**
1. Go to **Settings > Connectors**
2. Click **Add custom connector**
3. Enter URL: `https://mcp.datarails.com/mcp`
4. Click **Add**, then **Connect**

**Troubleshooting:**
| Problem | Solution |
|---------|----------|
| Connector not showing | Reinstall the plugin (ZIP upload or marketplace) |
| Connection fails | Click **Disconnect**, wait a moment, then **Connect** again |
| Authentication error | Make sure you're using valid Datarails credentials |

### Claude Code Track (Terminal)

Add the Datarails connector:

```
claude mcp add --transport http datarails-mcp https://mcp.datarails.com/mcp
```

A browser window opens for OAuth login when you first use a Datarails tool.

**Troubleshooting:**
| Problem | Solution |
|---------|----------|
| "Not authenticated" | Re-run `claude mcp add` command above |
| Browser doesn't open | Check your default browser settings, retry |
| Need different environment | Disconnect and reconnect |

---

## Step 2: Your First Financial Snapshot

**Time:** ~2 minutes

### Cowork Track

```
/datarails-finance-os:financial-summary
```

This fetches live financial totals using the aggregation API (~5 seconds).

### Claude Code Track

Start by exploring what data is available:

```
/dr-tables
```

Then pull a quick sample to see the data structure:

```
/dr-query TABLE_ID --sample
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Session expired" | Reconnect: Claude Desktop → "+" > Connectors > Disconnect/Connect. Claude Code Terminal → re-run `claude mcp add` |
| Empty results | Check that your environment has data for the current year |
| Slow response | First query may take 5-10 seconds; subsequent queries are faster |

---

## Step 3: Deeper Analysis

**Time:** ~5 minutes

### 3a. Expense Breakdown

_Where is money going?_

**Cowork:**
```
/datarails-finance-os:expense-analysis
```

**Claude Code:**
```
/dr-query TABLE_ID amount > 100000
```

### 3b. Revenue Trends

_How is revenue tracking?_

**Cowork:**
```
/datarails-finance-os:revenue-trends
```

**Claude Code:**
```
/dr-profile TABLE_ID --numeric
```

### 3c. Budget vs Actual

_Are we on plan?_

**Cowork:**
```
/datarails-finance-os:budget-comparison
```

**Claude Code:**
```
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget
```

---

## Step 4: Set Up Your Environment

**Time:** ~5 minutes

This step configures your environment profile, which enables the advanced skills (intelligence workbook, extraction, etc.).

### Cowork Track

```
/datarails-finance-os:test-api
```

This tests which API fields work with your environment and reports compatibility.

### Claude Code Track

First, discover your table structure and create a profile:

```
/dr-learn
```

Then test field compatibility and update the profile:

```
/dr-test
```

### Why This Matters

The client profile tells advanced skills (like `/dr-intelligence`) which fields work and which alternatives to use. Without it, those skills won't know how to query your specific environment.

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Many fields failing | Some environments have restricted fields - this is normal |
| "No profile found" | Run `/dr-learn` first to create the base profile |
| Profile looks wrong | Run `/dr-learn --force` to recreate from scratch |

---

## Step 5: Generate Your First Intelligence Report

**Time:** ~5 minutes

This is the most powerful feature - a comprehensive FP&A Intelligence Workbook with auto-detected insights.

### Cowork Track

Ask Claude directly:

```
Generate an FP&A intelligence workbook for 2025 from my Datarails data.
```

Claude will use the intelligence skill automatically, fetching live data and generating a 10-sheet Excel workbook.

### Claude Code Track

```
/dr-intelligence --year 2025
```

### What You'll Get

A professionally formatted Excel workbook with 10 sheets:

| Sheet | What It Contains |
|-------|-----------------|
| **Insights Dashboard** | Top 5 auto-detected findings with severity ratings |
| **Expense Deep Dive** | Top 20 expense accounts, % of total, trends |
| **Variance Waterfall** | What changed and why, waterfall analysis |
| **Trend Analysis** | 12-month P&L trends with growth rates |
| **Anomaly Report** | Auto-detected outliers and data quality flags |
| **Vendor Analysis** | Top vendors, concentration risk assessment |
| **SaaS Metrics** | ARR, LTV, CAC, efficiency ratios |
| **Sales Performance** | Rep leaderboard and quota attainment |
| **Cost Center P&L** | Department-level income statements |
| **Raw Data** | Pivot-ready data for your own analysis |

The file is saved to the `tmp/` directory. Open it in Excel to explore.

---

## What's Next

You're up and running. Here's where to go from here:

### Explore More Skills

| Goal | Skill |
|------|-------|
| Check data quality | `/dr-anomalies-report` |
| Executive presentation | `/dr-insights --year 2025 --quarter Q4` |
| Validate P&L vs KPIs | `/dr-reconcile --year 2025` |
| Department performance | `/dr-departments --year 2025` |
| SOX compliance audit | `/dr-audit --year 2025 --quarter Q4` |
| Export raw data to Excel | `/dr-extract --year 2025` |
| Real-time KPI dashboard | `/dr-dashboard` |

### Documentation

| Resource | Location |
|----------|----------|
| Full skill reference | [README.md](../../README.md) |
| API limitations | [FINANCE_OS_API_ISSUES_REPORT.md](../analysis/FINANCE_OS_API_ISSUES_REPORT.md) |
| Setup & troubleshooting | [SETUP.md](../../SETUP.md) |
| Plugin architecture | [CLAUDE.md](../../CLAUDE.md) |

---

## Quick Reference Card

| I want to... | Cowork Command | Claude Code Skill |
|--------------|----------------|-------------------|
| **Connect to Datarails** | "+" > Connectors > Connect | `claude mcp add --transport http datarails-mcp https://mcp.datarails.com/mcp` |
| **See financial totals** | `/datarails-finance-os:financial-summary` | `/dr-tables` + `/dr-query` |
| **Analyze expenses** | `/datarails-finance-os:expense-analysis` | `/dr-query` with filters |
| **Check revenue trends** | `/datarails-finance-os:revenue-trends` | `/dr-profile --numeric` |
| **Compare budget vs actual** | `/datarails-finance-os:budget-comparison` | `/dr-forecast-variance` |
| **Test API compatibility** | `/datarails-finance-os:test-api` | `/dr-test` |
| **Discover tables** | `/datarails-finance-os:explore-tables` | `/dr-tables` |
| **Check data quality** | `/datarails-finance-os:data-check` | `/dr-anomalies` |
| **Full intelligence report** | Ask Claude directly | `/dr-intelligence --year 2025` |
| **Export to Excel** | Ask Claude directly | `/dr-extract --year 2025` |
| **Set up environment** | `/datarails-finance-os:test-api` | `/dr-learn` + `/dr-test` |

---

**Last updated:** March 11, 2026
