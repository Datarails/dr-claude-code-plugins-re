# Finance OS API Issues Report

**Date:** February 5, 2026 (Updated: February 8, 2026)
**Environment:** Production (app.datarails.com)
**Analyst:** Claude Code

---

## Executive Summary

The Datarails Finance OS API has some reliability quirks but is largely functional once the async patterns are understood. The **aggregation API works via async polling** (POST returns 202, poll GET for results) and successfully handles **212 out of 220 fields** as dimensions. A handful of fields with special characters (`&` in names) or specific computed fields (`DR_ACC_L1`, `DR_ACC_L2`) cause server-side errors.

| Metric | Value |
|--------|-------|
| **Aggregation API Working** | Yes (async polling pattern) |
| **Fields Compatible** | 212/220 (96.4%) |
| **Avg Aggregation Time** | ~5 seconds |
| **Data Extraction Time** | 10 minutes for 54K records (pagination) |
| **Effective Throughput** | 90 records/second |

---

## Aggregation API: Async Polling Pattern

### How It Works (Confirmed Feb 8, 2026)

The aggregation endpoint uses a **long-running task pattern**:

1. **POST** `/tables/v1/{id}/aggregate` triggers the task
2. Returns **202 Accepted** with a **`Location` header** containing the poll URL
3. **GET** the Location URL to check status:
   - **200** = results ready (response body contains data)
   - **202** = still processing (keep polling)

### Implementation

```python
async def aggregate_with_polling(table_id, dimensions, metrics, filters=None):
    """Correct way to call the aggregation API."""
    # Step 1: POST to trigger aggregation
    resp = await client.post(
        f"{base_url}/finance-os/api/tables/v1/{table_id}/aggregate",
        headers=auth_headers,
        json={"dimensions": dimensions, "metrics": metrics, "filters": filters or []},
    )

    if resp.status_code == 200:
        return resp.json()  # Synchronous result (rare)

    if resp.status_code == 202:
        location = resp.headers["location"]
        # Location is relative: /tables/v1/{id}/aggregate/{base64_payload}
        # Needs /finance-os/api prefix for the poll URL
        poll_url = f"{base_url}/finance-os/api{location}"

        # Step 2: Poll for results
        while True:
            await asyncio.sleep(3)
            poll_resp = await client.get(poll_url, headers=auth_headers)

            if poll_resp.status_code == 200:
                return poll_resp.json()  # Results ready!
            elif poll_resp.status_code == 202:
                continue  # Still processing
            else:
                raise Exception(f"Poll failed: {poll_resp.status_code}")
```

### Key Details

- **Location header is relative**: Starts with `/tables/v1/...`, needs `/finance-os/api` prefix
- **Location payload is base64**: Contains the full downstream request config
- **Typical timing**: ~5 seconds (1 poll at 3s interval)
- **Max observed**: ~18 seconds (4 polls) for `Latest_In_Dim` boolean field
- **Multi-dimension queries**: Work fine with compatible fields

### Response Format

```json
{
  "success": true,
  "data": [
    {"Scenario": "Actuals", "Amount": 5593528663.83},
    {"Scenario": "Forecast", "Amount": 1088516730.44},
    {"Amount": 6682045394.27},           // Total row (when include_totals=true)
    {"col_keys": [], "row_keys": [...]}  // Metadata row
  ],
  "metadata": {...},
  "error": null
}
```

Note: The response includes extra rows at the end (totals row + metadata row).

---

## Field Compatibility (Tested Feb 8, 2026)

### Working Fields: 212/220 (96.4%)

All standard fields work including:
- System fields: `Scenario`, `Reporting Date`, `System_Year`, `Fiscal Period`, etc.
- Account fields: `DR_ACC_L0`, `DR_ACC_L_0.5`, `DR_ACC_L1.5`, `Account ID`, `Account Name`
- Department fields: `Department L1`, `Department L2`, `Cost Center`
- Numeric fields: `Amount`, `DEBIT`, `CREDIT`, `FX Rate`, etc.

### Failed Fields: 8/220

| Field | Failure Mode | Likely Cause |
|-------|-------------|-------------|
| `DR_ACC_L1` | 202 -> poll 500 | Server-side computation error |
| `DR_ACC_L2` | 202 -> poll 500 | Server-side computation error |
| `CF Grouping` | POST 500 | Server-side error |
| `CF Grouping 2` | 202 -> poll 500 | Server-side error |
| `Report_Field` | POST 500 | Server-side error |
| `USER_ACC_P&L` | POST 500 | HTML entity `&amp;` in field name |
| `P&L Accounts Filter` | POST 500 | HTML entity `&amp;` in field name |
| `Quarter & Year` | POST 500 | HTML entity `&amp;` in field name |

**Workaround for `DR_ACC_L1`/`DR_ACC_L2`**: Use `DR_ACC_L_0.5` or `DR_ACC_L1.5` as alternatives, or fetch raw data and group client-side for these specific fields.

---

## Remaining Issues

### 1. JWT Token Expiry Without Warning

**Severity:** 🟠 HIGH

JWT tokens expire after exactly **5 minutes** with no refresh mechanism exposed. Long-running operations fail silently.

**Evidence:**
```
[11:17:38] 401 at offset 27500, refreshing token...
[11:22:48] 401 at offset 52500, refreshing token...
```

**Impact:**
- Operations taking > 5 minutes will fail partway through
- Must manually refresh every 20K rows or 4 minutes

**Workaround:**
```python
if offset > 0 and offset % 20000 == 0:
    await auth.ensure_valid_token()
```

---

### 2. Distinct Values Endpoint Fails

**Severity:** 🟠 HIGH

The distinct values endpoint returns 409 Conflict errors:

```
GET /tables/v1/{id}/fields/by-name/{field}/distinct
Status: 409
Error: HTTP 409 error from downstream service
```

**Impact:**
- Cannot discover unique values for filters
- Must fetch sample data and extract unique values manually

---

### 3. Slow Paginated Data Extraction

**Severity:** 🟡 MEDIUM

Due to 500-record page limits, large table extraction is slow:

| Metric | Value |
|--------|-------|
| Total Records | 54,390 |
| Pages Required | 111 (500 per page) |
| Total Time | **10.1 minutes** |
| Throughput | 90 records/second |

**Note:** With working aggregation, many use cases no longer need full extraction.

---

### 4. HTML Entities in Field Names

**Severity:** 🟡 MEDIUM

Some field names contain HTML entities (`&amp;` instead of `&`):
- `USER_ACC_P&L` stored as `USER_ACC_P&amp;L`
- `P&L Accounts Filter` stored as `P&amp;L Accounts Filter`
- `Quarter & Year` stored as `Quarter &amp; Year`

These fields cause 500 errors in aggregation. Needs investigation on whether sending the HTML-encoded name works.

---

### 5. Inconsistent Error Responses

**Severity:** 🟢 LOW

The API returns different error formats:

| Endpoint | Error Format |
|----------|-------------|
| Aggregation 500 | `{"success": false, "data": null, "error": {...}}` |
| 202 Accepted | `null` body |
| 401 Token Expired | JSON error object |

---

## Performance Benchmarks

### Aggregation API (Async Polling)

| Query Type | Time | Polls |
|-----------|------|-------|
| Zero dimensions (SUM, COUNT) | ~4s | 1 |
| Single dimension (Scenario) | ~4s | 1 |
| Single dimension (Reporting Date) | ~4s | 1 |
| Boolean dimension (Latest_In_Dim) | ~18s | 4 |
| Multi-dimension (2 fields) | ~5s | 1 |
| High-cardinality (Journal Number, 91K groups) | ~8s | 1 |

### Data Pagination

| Metric | Value |
|--------|-------|
| Average page fetch | ~5.4 seconds |
| Token refreshes needed (54K rows) | 4 |

---

## Workarounds Implemented

### 1. Async Polling for Aggregation (NEW - Feb 8, 2026)

The MCP client now handles the 202 + Location header pattern automatically:

```python
async def _request_async_poll(self, endpoint, json_data, poll_interval=3.0, max_polls=20):
    """POST with async polling for long-running tasks."""
    response = await client.post(url, headers=headers, json=json_data)

    if response.status_code == 202:
        location = response.headers.get("location")
        poll_url = f"{base_url}/finance-os/api{location}"

        for _ in range(max_polls):
            await asyncio.sleep(poll_interval)
            poll_resp = await client.get(poll_url, headers=headers)
            if poll_resp.status_code == 200:
                return poll_resp.json()
```

### 2. Client-Side Aggregation (Fallback for DR_ACC_L1/L2)

```python
def _aggregate_client_side(data, group_by, sum_field):
    aggregated = defaultdict(float)
    for record in data:
        key = tuple(str(record.get(f, "")) for f in group_by)
        aggregated[key] += float(record.get(sum_field, 0) or 0)
    return [dict(zip(group_by, k), **{sum_field: v}) for k, v in aggregated.items()]
```

### 3. Paginated Data Fetch with Token Refresh

```python
async def fetch_all_data(table_id, filters, max_rows=100000):
    all_data = []
    offset = 0
    while len(all_data) < max_rows:
        if offset > 0 and offset % 20000 == 0:
            await auth.ensure_valid_token()
        page = await fetch_page(table_id, filters, limit=500, offset=offset)
        if not page:
            break
        all_data.extend(page)
        offset += 500
    return all_data
```

---

## Recommendations for Datarails Engineering

### Priority 1: Fix DR_ACC_L1 / DR_ACC_L2 Aggregation

These are the most commonly used account hierarchy fields but cause 500 errors during aggregation polling. This is likely a server-side computation or timeout issue.

### Priority 2: Fix HTML Entity Encoding in Field Names

Fields containing `&` are stored with `&amp;` encoding, which breaks aggregation. Either:
1. Store raw `&` in field names
2. Accept both `&` and `&amp;` in API requests

### Priority 3: Increase Page Size Limit

Allow page sizes up to 5,000 or 10,000 records for bulk extraction.

### Priority 4: Fix Distinct Values Endpoint

The 409 error on distinct values endpoint should be investigated.

### Priority 5: Longer Token Expiry

5-minute JWT expiry is too short for data operations. Recommend 30-minute expiry.

---

## Appendix: Test Configuration

```
Environment: app (Production)
Base URL: https://app.datarails.com
Financials Table: 16528 (54,390 records, 220+ fields)
Test Dates: 2026-02-05 (initial), 2026-02-08 (aggregation retest)
```

---

## Change Log

| Date | Change |
|------|--------|
| 2026-02-05 | Initial report - aggregation marked as broken |
| 2026-02-08 | **Major update**: Aggregation works via async polling (POST 202 + Location -> GET poll). 212/220 fields work. Updated client code. |

---

*Report generated by Claude Code diagnostic tool*
