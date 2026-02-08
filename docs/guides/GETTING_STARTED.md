# Getting Started with Datarails Finance OS Plugin

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
| **Datarails account** | Active login at your Datarails environment (app.datarails.com, dev.datarails.com, etc.) |
| **Browser session** | Be logged into Datarails in your browser before starting |
| **Claude Cowork** _or_ **Claude Code** | Cowork: no additional setup. Claude Code: install the plugin first (see [README](../../README.md)) |

### Which Track Are You?

| Track | Who It's For | What You Need |
|-------|-------------|---------------|
| **Cowork** | Finance teams, business users | Just a browser - no terminal required |
| **Claude Code** | Developers, power users | Terminal + plugin installed |

Both tracks access the same data and produce the same quality results. Choose the one that matches your workflow.

---

## Step 1: Connect to Datarails

**Time:** ~2 minutes

### Cowork Track

Run the login command in your Cowork conversation:

```
/datarails-finance-os:login
```

Claude will guide you through browser-based authentication. You'll be asked to:
1. Confirm you're logged into Datarails in your browser
2. Provide your session cookies (Claude shows you how to extract them)
3. Verify the connection works

**What you'll see:**

```
Checking authentication status...

You're not currently authenticated. Let's fix that.

Please log into Datarails at https://app.datarails.com in your browser,
then I'll help you extract the session cookies.

[Follow the guided steps to paste your sessionid and csrftoken]

Authentication successful! Connected to Datarails (app).
```

### Claude Code Track

```
/dr-auth --env app
```

This extracts browser cookies automatically from your logged-in session.

**What you'll see:**

```
Authenticating with Datarails (app)...
Extracting session cookies from browser...
  Found sessionid cookie
  Found csrftoken cookie
Verifying JWT token refresh...
  JWT token obtained (expires in 5 min, auto-refreshes)

Connected to Datarails (app.datarails.com)
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Not authenticated" | Make sure you're logged into Datarails in your browser first |
| Cookie extraction fails | Close other browser tabs using Datarails, then retry |
| Wrong environment | Specify explicitly: `--env app` (production) or `--env dev` (development) |

---

## Step 2: Your First Financial Snapshot

**Time:** ~2 minutes

### Cowork Track

```
/datarails-finance-os:financial-summary
```

This fetches live financial totals using the aggregation API (~5 seconds).

**What you'll see:**

```
Fetching financial summary...

FINANCIAL SUMMARY - 2025

Revenue:                   $3,435,270
Cost of Goods Sold:        $1,320,553
Gross Profit:              $2,114,717
Operating Expenses:       $28,452,126
Financial Expenses:          $105,234

Gross Margin:                  61.6%
Operating Margin:            -765.7%

Data covers: Jan - Nov 2025 (9 months with data)
Source: Datarails Finance OS (app) | Scenario: Actuals
```

You just pulled real numbers from your live Datarails environment. These are aggregated totals computed server-side - not samples or estimates.

### Claude Code Track

Start by exploring what data is available:

```
/dr-tables
```

**What you'll see:**

```
Finance OS Tables (app)

ID      Name                    Rows     Last Modified
------  ----------------------  -------  ----------------
TABLE_ID   Financial Records       54,390   2026-02-01
18234   KPI Metrics              2,156   2026-02-01
```

Then pull a quick sample to see the data structure:

```
/dr-query TABLE_ID --sample
```

**What you'll see:**

```
Sample Records from Financial Records (20 random rows)

Reporting Date  | DR_ACC_L0 | DR_ACC_L1         | Amount     | Scenario
----------------|-----------|-------------------|------------|----------
2025-03-01      | P&L       | REVENUE           |  12,450.00 | Actuals
2025-06-01      | P&L       | Operating Expense | -45,230.50 | Actuals
2025-02-01      | P&L       | Cost of Goods Sold|   8,100.00 | Budget
...
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Session expired" | Re-authenticate: `/datarails-finance-os:login` (Cowork) or `/dr-auth` (Claude Code) |
| Empty results | Check that your environment has data for the current year |
| Slow response | First query may take 5-10 seconds; subsequent queries are faster |

---

## Step 3: Deeper Analysis

**Time:** ~5 minutes

Now that you're connected, try three progressively deeper analyses.

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

**What you'll see (Cowork):**

```
EXPENSE ANALYSIS - 2025

TOP EXPENSE CATEGORIES
Rank  Category              Amount          % of Total
----  --------------------  --------------  ----------
1     R&D                   $12,345,678     43.4%
2     Sales & Marketing      $8,234,567     28.9%
3     G&A                    $4,567,890     16.1%
4     Product                $2,345,678      8.2%
5     HR                       $958,313      3.4%

MONTHLY TREND
Month     Total Expenses    MoM Change
--------  ----------------  ----------
2025-01   $2,134,567        --
2025-02   $2,456,789        +15.1%
2025-03   $2,567,890        +4.5%
...
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

**What you'll see (Cowork):**

```
REVENUE TRENDS - 2025

MONTHLY REVENUE
Month     Revenue       MoM Growth
--------  -----------   ----------
2025-01   $245,678      --
2025-02   $312,456      +27.2%
2025-03   $356,789      +14.2%
...

REVENUE BY SOURCE
Source            Amount         % of Total
----------------  -----------   ----------
Subscriptions     $2,567,890    74.8%
Professional Svcs   $567,890    16.5%
Other               $299,490     8.7%
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

**What you'll see (Cowork):**

```
BUDGET VS ACTUAL - 2025

Category              Actual          Budget          Variance     %
--------------------  --------------  --------------  ----------   ------
Revenue               $3,435,270      $4,200,000     ($764,730)   -18.2%
COGS                  $1,320,553      $1,500,000      $179,447    +12.0%
Operating Expenses   $28,452,126     $25,000,000    ($3,452,126)  -13.8%

Overall: Tracking 18.2% below revenue target
         OpEx 13.8% over budget
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

**What you'll see:**

```
API FIELD COMPATIBILITY TEST

Testing aggregation API with your environment...

Field                Status    Time
-------------------  --------  ------
Amount               PASS      0.8s
Reporting Date       PASS      0.9s
DR_ACC_L0            PASS      1.1s
DR_ACC_L1            FAIL      --     (500 error)
Account L1 (alt)     PASS      1.0s
Scenario             PASS      0.7s
Department L1        PASS      1.2s
...

Result: 210/220 fields compatible
Alternatives found for 8/10 failed fields
```

### Claude Code Track

First, discover your table structure and create a profile:

```
/dr-learn --env app
```

**What you'll see:**

```
Discovering table structure for app environment...

Found 2 tables:
  Financial Records (ID: TABLE_ID) - 54,390 rows
  KPI Metrics (ID: 18234) - 2,156 rows

Analyzing field mappings...
  Amount field: Amount
  Date field: Reporting Date
  Account hierarchy: DR_ACC_L0 > DR_ACC_L1 > DR_ACC_L2
  Scenario field: Scenario

Detecting account categories...
  P&L accounts: REVENUE, Cost of Goods Sold, Operating Expense, Financial Expenses
  KPI metrics: ARR, LTV, CAC, Churn, Revenue

Profile saved: config/client-profiles/app.json
```

Then test field compatibility and update the profile:

```
/dr-test --env app
```

**What you'll see:**

```
Testing API field compatibility (app)...

Aggregation API: SUPPORTED (async polling)
Testing 220 fields...

Results:
  212 fields: PASS
    8 fields: FAIL (500 errors)
   10 alternatives found for failed fields

Profile updated: config/client-profiles/app.json
  - aggregation.supported = true
  - aggregation.failed_fields = [8 fields]
  - aggregation.field_alternatives = {mapped}
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
/dr-intelligence --year 2025 --env app
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

**What you'll see in the terminal:**

```
Generating FP&A Intelligence Workbook (2025)...

Phase 1: Loading profile (app)
  Using aggregation API (fast path)
  Account field: Account L1 (alternative for DR_ACC_L1)

Phase 2: Fetching data
  P&L by month...          done (5.2s)
  P&L by account...        done (4.8s)
  Department breakdown...   done (5.1s)
  KPI metrics...           done (3.2s)

Phase 3: Analyzing
  Detecting insights...     5 findings
  Computing variances...    done
  Identifying anomalies...  3 flagged

Phase 4: Building workbook
  10 sheets created
  Professional formatting applied

Saved: tmp/FPA_Intelligence_Workbook_2025_20260208.xlsx
```

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

### Multi-Environment Support

Work across environments simultaneously:

```
/dr-auth --env dev          # Connect to development
/dr-auth --env app          # Connect to production
/dr-auth --list             # See all connections
```

All skills accept `--env` to target a specific environment.

### Documentation

| Resource | Location |
|----------|----------|
| Full skill reference | [README.md](../../README.md) |
| API limitations | [FINANCE_OS_API_ISSUES_REPORT.md](../analysis/FINANCE_OS_API_ISSUES_REPORT.md) |
| FP&A report guide | [COMPREHENSIVE_FPA_REPORT_GUIDE.md](COMPREHENSIVE_FPA_REPORT_GUIDE.md) |
| Setup & troubleshooting | [SETUP.md](../../SETUP.md) |
| Plugin architecture | [CLAUDE.md](../../CLAUDE.md) |

---

## Quick Reference Card

| I want to... | Cowork Command | Claude Code Skill |
|--------------|----------------|-------------------|
| **Connect to Datarails** | `/datarails-finance-os:login` | `/dr-auth --env app` |
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

**Status:** Ready for use
**Last updated:** February 8, 2026
