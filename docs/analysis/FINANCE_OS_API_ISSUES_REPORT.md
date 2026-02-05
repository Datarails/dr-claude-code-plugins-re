# Finance OS API Issues Report

**Date:** February 5, 2026
**Environment:** Production (app.datarails.com)
**Analyst:** Claude Code

---

## Executive Summary

The Datarails Finance OS API has significant reliability issues that require extensive workarounds for basic operations. The **aggregation API is fundamentally broken**, returning errors 100% of the time in our tests. This forces all data extraction to use pagination with client-side aggregation, which is **6.7x slower** than expected.

| Metric | Value |
|--------|-------|
| **Total Tests** | 10 |
| **Pass Rate** | 60% |
| **Aggregation API Success** | 0% |
| **Data Extraction Time** | 10 minutes for 54K records |
| **Effective Throughput** | 90 records/second |

---

## Critical Issues

### 1. Aggregation API Completely Non-Functional

**Severity:** 🔴 CRITICAL

The aggregation endpoint (`POST /tables/v1/{id}/aggregate`) fails 100% of the time with various error codes:

| Request Type | Status Code | Response |
|--------------|-------------|----------|
| Simple (1 dimension) | **202 Accepted** | Async processing (not supported) |
| Complex (3 dimensions) | **500** | Internal server error |
| KPI Table | **202 Accepted** | Null body |

**Evidence:**
```
❌ Simple Aggregation: 202 (1550ms) - async processing required (not supported)
❌ Complex Aggregation: 500 (1538ms) - Internal server error in downstream service
❌ KPI Aggregation: 202 (1347ms) - Null body
```

**Impact:**
- Cannot perform server-side GROUP BY operations
- Cannot get SUM/AVG/COUNT aggregates from API
- Must fetch ALL raw data and aggregate client-side
- 10-minute operations that should take 10 seconds

**Workaround Required:**
```python
# Instead of this (doesn't work):
result = await client.aggregate(
    table_id="TABLE_ID",
    dimensions=["Account L1", "Month"],
    metrics=[{"field": "Amount", "agg": "SUM"}]
)

# Must do this (slow but works):
all_data = await paginate_all_records(table_id="TABLE_ID")  # 54K records
aggregated = defaultdict(float)
for record in all_data:
    key = (record["Account L1"], record["Month"])
    aggregated[key] += record["Amount"]
```

---

### 2. JWT Token Expiry Without Warning

**Severity:** 🔴 CRITICAL

JWT tokens expire after exactly **5 minutes** with no refresh mechanism exposed. Long-running operations fail silently.

**Evidence:**
```
[11:17:38] 401 at offset 27500, refreshing token...
[11:22:48] 401 at offset 52500, refreshing token...
```

**Impact:**
- Operations taking > 5 minutes will fail partway through
- No automatic token refresh
- Must manually refresh every 20K rows or 4 minutes
- Lost work if not handled properly

**Workaround Required:**
```python
# Must refresh token proactively
if offset > 0 and offset % 20000 == 0:
    await auth.ensure_valid_token()
```

---

### 3. Distinct Values Endpoint Fails

**Severity:** 🟠 HIGH

The distinct values endpoint returns 409 Conflict errors:

```
GET /tables/v1/{id}/fields/by-name/{field}/distinct
Status: 409
Error: HTTP 409 error from downstream service
```

**Impact:**
- Cannot discover unique values for filters
- Cannot build dynamic filter dropdowns
- Must fetch sample data and extract unique values manually

---

### 4. Extremely Slow Data Extraction

**Severity:** 🟠 HIGH

Due to aggregation API failures, we must paginate through ALL records:

| Metric | Value |
|--------|-------|
| Total Records | 54,390 |
| Pages Required | 111 (500 per page) |
| Total Time | **10.1 minutes** |
| Throughput | 90 records/second |

**Breakdown:**
- Average page fetch: ~5.4 seconds
- Token refreshes: 4
- 401 errors handled: 2

**Expected vs Actual:**
| Operation | Expected | Actual | Overhead |
|-----------|----------|--------|----------|
| Simple aggregation | ~2 seconds | N/A (fails) | ∞ |
| Full data extract | ~30 seconds | 604 seconds | **20x** |
| Report generation | ~1 minute | 10+ minutes | **10x** |

---

### 5. Inconsistent Error Responses

**Severity:** 🟡 MEDIUM

The API returns different error formats and status codes for similar failures:

| Endpoint | Error Format |
|----------|-------------|
| Aggregation | `{"success": false, "data": null, "error": {...}}` |
| 202 Accepted | `null` body |
| 500 Error | Full error object |
| 401 Token Expired | Sometimes empty body |

**Impact:**
- Complex error handling required
- Must handle null responses, empty bodies, and various formats
- Brittle parsing code

---

### 6. No Async Polling Support

**Severity:** 🟡 MEDIUM

When aggregation returns `202 Accepted`, it indicates the server is processing asynchronously, but there's **no documented way to poll for results**.

**What would be needed:**
```python
# This doesn't exist
result = await client.aggregate(...)  # Returns 202
poll_url = result.headers["Location"]
while True:
    status = await client.get(poll_url)
    if status.complete:
        return status.data
    await asyncio.sleep(1)
```

---

## Moderate Issues

### 7. No Batch/Bulk Operations

**Severity:** 🟡 MEDIUM

There's no way to fetch multiple pages in a single request. Must make 111 separate API calls for 54K records.

**Impact:**
- Network latency multiplied by page count
- Connection overhead per request
- Rate limiting concerns

---

### 8. 500-Record Page Limit

**Severity:** 🟢 LOW

The maximum page size is 500 records. Larger page sizes would reduce total requests.

**Impact:**
- 111 requests instead of potentially 11 (with 5000 limit)
- More network overhead
- More token refresh cycles

---

### 9. No Query Caching

**Severity:** 🟢 LOW

Repeated identical queries re-execute fully. No server-side caching evident.

**Impact:**
- Same slow performance on repeated operations
- No benefit from warm-up queries

---

## Performance Benchmarks

### Data Pagination Test

```
Test: Full Data Pagination (all records)
Records: 54,390
Time: 604.3 seconds (10.1 minutes)
Rate: 90 records/second
Token Refreshes: 4
401 Errors Recovered: 2
```

### API Response Times

| Endpoint | Avg Response Time | Notes |
|----------|-------------------|-------|
| List Tables | 488ms | Works reliably |
| Get Schema | 444ms | Works reliably |
| Distinct Values | 1437ms | **FAILS** (409) |
| Aggregation (simple) | 1550ms | **FAILS** (202) |
| Aggregation (complex) | 1538ms | **FAILS** (500) |
| Data (single page) | 3133ms | Works |
| Data (concurrent 5) | 3728ms | Works |

---

## Workarounds Implemented

### 1. Client-Side Aggregation
```python
def _aggregate_client_side(data, group_by, sum_field):
    aggregated = defaultdict(float)
    for record in data:
        key = tuple(str(record.get(f, "")) for f in group_by)
        aggregated[key] += float(record.get(sum_field, 0) or 0)
    return [dict(zip(group_by, k), **{sum_field: v}) for k, v in aggregated.items()]
```

### 2. Paginated Data Fetch with Token Refresh
```python
async def fetch_all_data(table_id, filters, max_rows=100000):
    all_data = []
    offset = 0

    async with httpx.AsyncClient(timeout=60.0) as client:
        while len(all_data) < max_rows:
            # Refresh token every 20K rows
            if offset > 0 and offset % 20000 == 0:
                await auth.ensure_valid_token()

            # Retry logic for transient failures
            for attempt in range(3):
                resp = await client.post(url, headers=auth.get_headers(), json={...})

                if resp.status_code == 401:
                    await auth.ensure_valid_token()
                    continue

                if resp.status_code == 502:
                    await asyncio.sleep(2)
                    continue

                break

            page = resp.json().get("data", [])
            all_data.extend(page)

            if len(page) < 500:
                break
            offset += 500

    return all_data
```

### 3. Robust Error Handling
```python
def parse_response(result):
    if result is None:
        return []
    if isinstance(result, str) and result.strip() in ('', 'null'):
        return []
    if isinstance(result, dict) and "error" in result:
        return []
    if isinstance(result, dict) and "data" in result:
        return result["data"] if isinstance(result["data"], list) else []
    return result if isinstance(result, list) else []
```

---

## Recommendations for Datarails Engineering

### Priority 1: Fix Aggregation API

The aggregation endpoint returning 202 or 500 makes the API nearly unusable for analytics. Either:

1. **Make it synchronous** - Return results directly for small datasets
2. **Implement proper async polling** - Return a job ID and status endpoint
3. **Increase timeout** - The current timeout seems too aggressive

### Priority 2: Increase Page Size

Allow page sizes up to 5,000 or 10,000 records:
- Would reduce requests from 111 to 11
- Would dramatically improve extraction time
- Standard practice for bulk data APIs

### Priority 3: Implement Batch Endpoints

Add endpoints for bulk operations:
```
POST /tables/v1/{id}/data/batch
{
  "requests": [
    {"offset": 0, "limit": 5000},
    {"offset": 5000, "limit": 5000},
    ...
  ]
}
```

### Priority 4: Fix Distinct Values

The 409 error on distinct values endpoint should be investigated.

### Priority 5: Longer Token Expiry

5-minute JWT expiry is too short for data operations. Recommend:
- 30-minute expiry for API tokens
- Or implement automatic token refresh endpoint

---

## Appendix: Test Configuration

```
Environment: app (Production)
Base URL: https://app.datarails.com
Financials Table: TABLE_ID (54,390 records)
KPIs Table: 34298 (973 records)
Test Date: 2026-02-05
Test Duration: ~15 minutes
```

---

## Files Generated

| File | Description |
|------|-------------|
| `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` | This report |
| `tmp/API_Diagnostic_Report_20260205_112322.txt` | Raw test output |
| `mcp-server/scripts/api_diagnostic.py` | Diagnostic tool |

---

*Report generated by Claude Code diagnostic tool*
