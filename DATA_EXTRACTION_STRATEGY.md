# Data Extraction Strategy: Caching & Incremental Updates
**Discovery Date:** February 4, 2026
**Status:** Records are FIXED and STABLE

---

## Critical Discovery

**Records are not dynamic - they are FIXED and STABLE.**

- Record at offset 5000 today = same record tomorrow
- Order is preserved across fetches
- Records are loosely segmented by account type
- **You can cache records and only fetch new ones**

---

## Extraction Architecture

### Phase 1: Initial Full Extract (ONE TIME)

```python
async def initial_extract():
    """Fetch all 54,390 records once"""
    all_records = []

    for offset in range(0, 54390, 500):
        records = await api.fetch(offset=offset, limit=500)
        all_records.extend(records)

    # Cache the results
    cache = {
        'total_records': len(all_records),
        'last_offset': 54390,
        'last_sync': datetime.now(),
        'records': all_records  # Or save to disk
    }

    return cache
```

**Time:** ~3-5 minutes (54K records at 184.8 rec/sec)
**Cost:** One full API traversal
**Benefit:** Complete historical data

### Phase 2: Daily Updates (INCREMENTAL)

```python
async def daily_update(cache):
    """Only fetch new records since last sync"""
    last_offset = cache['last_offset']

    # Check if there are new records
    new_records = await api.fetch(offset=last_offset, limit=1)

    if not new_records:
        print("✓ No new data")
        return cache  # Nothing new

    # Fetch from last known offset
    new_records = []
    offset = last_offset

    while True:
        batch = await api.fetch(offset=offset, limit=500)
        if not batch:
            break
        new_records.extend(batch)
        offset += 500

    # Append to cache
    cache['records'].extend(new_records)
    cache['last_offset'] = offset
    cache['last_sync'] = datetime.now()

    return cache
```

**Time:** Seconds to minutes (only new records)
**Cost:** Minimal API calls
**Benefit:** Fresh data without re-fetching everything

### Phase 3: Analysis (FROM CACHE)

```python
async def analyze():
    """Work from cached records"""
    records = load_cache()  # Load from disk or memory

    # Sort client-side
    sorted_records = sorted(records, key=lambda r: r.get('Reporting Date'))

    # Build P&L
    pnl = build_pnl(sorted_records)

    # Generate Excel
    export_to_excel(pnl)
```

**Time:** Instant (no API calls)
**Cost:** Zero API overhead
**Benefit:** Fast analysis and reporting

---

## Cache Structure

### Option A: Memory Cache (Fast)
```python
cache = {
    'version': '1.0',
    'environment': 'app',
    'table_id': '16528',
    'total_records': 54390,
    'last_offset': 54390,
    'last_sync': '2026-02-04T12:00:00Z',
    'records': [  # Array of all 54K records
        {'DR_ACC_L1': 'Revenue', 'Amount': 1000, ...},
        {'DR_ACC_L1': 'OpEx', 'Amount': 500, ...},
        ...
    ]
}
```

### Option B: Disk Cache (Persistent)
```
cache/
├── metadata.json        # Version, last_sync, total_records
├── records.jsonl        # One record per line (streaming)
└── index.json           # Offset mapping
```

### Option C: Hybrid (Best)
```
Memory: Cache of last 5,000 records (hot data)
Disk: Full archive (54K records)
```

---

## Record Segmentation Pattern

Since records are loosely segmented by account type, you can optimize:

```
Offsets     Dominant Account       % Records
0-5000      Operating Expense      ~84%
5000-15000  Mix (REVENUE, OpEx)    ~50/50
15000-30000 REVENUE + OpEx         Mixed
30000-40000 REVENUE                ~70%
40000-45000 Financial Expenses     ~83%
45000-54390 Operating Expense      ~82%
```

**Benefit:** Can pre-fetch certain ranges based on what you're analyzing
- Analyzing OpEx? Fetch 0-5000 and 45000-54390
- Analyzing Revenue? Fetch 5000-30000 and 30000-40000
- Analyzing Financial? Fetch 40000-45000

---

## Incremental Update Strategy

### Option 1: Time-Based (Recommended)
```python
# Run daily at 8 AM
if datetime.now().hour == 8:
    new_records = fetch_since(last_sync_time)
    cache.extend(new_records)
```

**Pros:** Predictable, works for daily reporting
**Cons:** Doesn't catch mid-day updates

### Option 2: Change-Triggered
```python
# Check if new records were added
new_count = await api.get_total_count()  # 54390 today

if new_count > cache['total_records']:
    # New data added
    new_records = fetch_from(cache['last_offset'])
    cache.extend(new_records)
    cache['total_records'] = new_count
```

**Pros:** Catches all updates immediately
**Cons:** Needs new API method or polling

### Option 3: Hybrid
```python
# Daily update + on-demand refresh
- Run daily update at 8 AM
- Allow manual refresh button
- Check for new records on report generation
```

---

## Extraction Performance

### Current (Fetch everything)
```
Total time to fetch 54K: ~5 minutes
Speed: 184.8 records/second
Batch size: 500 (optimal)
API calls: 109 calls
```

### Optimized (Cache + incremental)
```
First run: 5 minutes (one-time)
Daily update:
  - If no new data: <1 second (1 API call)
  - If new data: 30-60 seconds (depends on volume)
Annual savings:
  - Skip 364 full extractions = 30+ hours saved
  - Save 39,876 API calls (out of 40,000 budget)
```

---

## Implementation Checklist

- [ ] Implement cache structure
- [ ] Add cache persistence (save to disk)
- [ ] Implement initial full extract
- [ ] Implement incremental update logic
- [ ] Add cache validation (check for corrupted data)
- [ ] Add cache versioning (handle schema changes)
- [ ] Add cache TTL (expire old data)
- [ ] Monitor cache size
- [ ] Add cache reset/refresh command
- [ ] Document cache location and format

---

## Key Insights

1. **Records are stable** → Can rely on offsets
2. **Loosely segmented** → Can optimize ranges
3. **Not dynamic** → Don't need constant updates
4. **Incremental possible** → Huge efficiency gains
5. **Time-based updates** → Fit daily/weekly workflows

---

## What Changed

| Aspect | Before | After |
|--------|--------|-------|
| Extraction strategy | Full refetch each time | Cache + incremental |
| Frequency needed | Every analysis | Once daily |
| Time per report | 5 minutes | Instant |
| API calls | 109 per run | 1-2 per run |
| Annual API cost | High | Low |

**Bottom line:** Records being FIXED unlocks major efficiency gains through caching and incremental updates.
