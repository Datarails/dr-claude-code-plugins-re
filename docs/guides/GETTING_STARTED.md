# Getting Started with Datarails FinanceOS Plugin

**Your first 15 minutes: from installation to your first financial report.**

---

## What You'll Accomplish

By the end of this guide, you will have:

1. Connected to your Datarails environment
2. Pulled your first live financial snapshot
3. Run deeper analysis (expenses, revenue, budget variance)
4. Optionally checked API field compatibility
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

### Cowork / Claude Desktop Track

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

Install the plugin (see [README](../../README.md)). The `datarails-finance-os`
connector is bundled with it and configured automatically — there is no
`claude mcp add` step. A browser window opens for OAuth login the first time you
use a Datarails tool. Use `/mcp` to check connector status or re-authenticate.

**Troubleshooting:**
| Problem | Solution |
|---------|----------|
| "Not authenticated" | Run `/mcp` and reconnect the Datarails connector |
| Browser doesn't open | Check your default browser settings, retry |
| Need different environment | Disconnect and reconnect |

---

## Step 2: Your First Financial Snapshot

**Time:** ~2 minutes

### Cowork Track

```
/datarails-financeos:financial-summary
```

This fetches live financial totals using the aggregation API (~5 seconds).

### Claude Code Track

Start by exploring what data is available:

```
/datarails-financeos:tables
```

Then pull a quick sample to see the data structure:

```
/datarails-financeos:query TABLE_ID --sample
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Session expired" | Reconnect: Claude Desktop → "+" > Connectors > Disconnect/Connect. Claude Code → run `/mcp` and reconnect |
| Empty results | Check that your environment has data for the current year |
| Slow response | First query may take 5-10 seconds; subsequent queries are faster |

---

## Step 3: Deeper Analysis

**Time:** ~5 minutes

### 3a. Expense Breakdown

_Where is money going?_

**Cowork:**
```
/datarails-financeos:expense-analysis
```

**Claude Code:**
```
/datarails-financeos:expense-analysis
```
(For ad-hoc slicing, `/datarails-financeos:query` also supports advanced filters — comparisons, ranges, text matching, null checks, date ranges — on fields discovered at runtime.)

### 3b. Revenue Trends

_How is revenue tracking?_

**Cowork:**
```
/datarails-financeos:revenue-trends
```

**Claude Code:**
```
/datarails-financeos:revenue-trends
```

### 3c. Budget vs Actual

_Are we on plan?_

**Cowork:**
```
/datarails-financeos:budget-comparison
```

**Claude Code:**
```
/datarails-financeos:forecast-variance --year 2026
```
The skill discovers which scenarios your org actually has at runtime (it never assumes a "Budget" scenario exists — plan data may live in a planning-version field). You can still name scenarios explicitly if you know them.

---

## Step 4: Optional — Check Field Compatibility

**Time:** ~5 minutes

There is no setup or profile step. Skills discover your financials table and
field names on their own, each session. This optional diagnostic reports up
front which fields work as aggregation dimensions — handy for large or unusual
environments, but not a prerequisite for any skill.

### Cowork Track

```
/datarails-financeos:test-api
```

This tests which API fields work with your environment and reports compatibility.

### Why This Matters

Skills discover your financials table and field names automatically each session, so there's no setup step. `/datarails-financeos:test` is optional — it reports which fields work as aggregation dimensions up front, but skills also retry a sibling field on their own when an aggregation rejects one.

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Many fields failing | Some environments have restricted fields - this is normal |
| Skill picked the wrong table/field | Tell it which table or field to use; it will continue from there |

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
/datarails-financeos:intelligence --year 2026
```

### What You'll Get

A professionally formatted Excel workbook with up to 10 sheets (conditional
sheets are included only when the underlying data exists in your org, and
omitted rather than fabricated):

| Sheet | What It Contains |
|-------|-----------------|
| **Insights Dashboard** | Top 5 auto-detected findings with severity ratings |
| **Expense Deep Dive** | Top 20 expense accounts, % of total, trends |
| **Variance Waterfall** | What changed and why, waterfall analysis |
| **Trend Analysis** | 12-month P&L trends with growth rates |
| **Anomaly Report** | Auto-detected outliers and data quality flags |
| **Vendor Analysis** | Top vendors, concentration risk *(only when vendor-level data exists)* |
| **SaaS Metrics** | ARR, NRR, CAC, LTV *(only when your org's data sources them; omitted otherwise)* |
| **Sales Performance** | Rep leaderboard and quota attainment *(only when rep/bookings data exists)* |
| **Cost Center P&L** | Department-level income statements *(only when department data exists)* |
| **Raw Data** | Pivot-ready data for your own analysis |

The file is saved to the `tmp/` directory. Open it in Excel to explore.

---

## What's Next

You're up and running. Here's where to go from here:

### Explore More Skills

| Goal | Skill |
|------|-------|
| Check data quality | `/datarails-financeos:anomalies-report` |
| Executive presentation | `/datarails-financeos:insights --year 2026 --quarter Q4` |
| Cross-source consistency checks (pipeline/mapping validation) | `/datarails-financeos:reconciliation --year 2026` |
| Department performance | `/datarails-financeos:departments --year 2026` |
| Audit-support evidence package | `/datarails-financeos:audit --year 2026 --quarter Q4` |
| Export raw data to Excel | `/datarails-financeos:extract --year 2026` |
| Real-time KPI dashboard | `/datarails-financeos:dashboard` |

### Documentation

| Resource | Location |
|----------|----------|
| Full skill reference | [README.md](../../README.md) |
| Setup & troubleshooting | [SETUP.md](../../SETUP.md) |
| Plugin architecture | [CLAUDE.md](../../CLAUDE.md) |

---

## Quick Reference Card

| I want to... | Cowork Command | Claude Code Skill |
|--------------|----------------|-------------------|
| **Connect to Datarails** | "+" > Connectors > Connect | Bundled with the plugin — OAuth opens on first tool use (`/mcp` to check status) |
| **See financial totals** | `/datarails-financeos:financial-summary` | `/datarails-financeos:financial-summary` |
| **Analyze expenses** | `/datarails-financeos:expense-analysis` | `/datarails-financeos:expense-analysis` |
| **Check revenue trends** | `/datarails-financeos:revenue-trends` | `/datarails-financeos:revenue-trends` |
| **Compare budget vs actual** | `/datarails-financeos:budget-comparison` | `/datarails-financeos:forecast-variance` |
| **Test API compatibility** | `/datarails-financeos:test-api` | `/datarails-financeos:test` |
| **Discover tables** | `/datarails-financeos:explore-tables` | `/datarails-financeos:tables` |
| **Check data quality** | `/datarails-financeos:data-check` | `/datarails-financeos:anomalies` |
| **Full intelligence report** | Ask Claude directly | `/datarails-financeos:intelligence --year 2026` |
| **Export to Excel** | Ask Claude directly | `/datarails-financeos:extract --year 2026` |
| **Check field compatibility (optional)** | `/datarails-financeos:test-api` | `/datarails-financeos:test` |

---

**Last updated:** July 2026 · validated against plugin v3.0.3
