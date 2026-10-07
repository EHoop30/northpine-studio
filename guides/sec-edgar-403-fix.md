---
title: "Fix SEC EDGAR 403 errors in Python"
description: "Fix SEC EDGAR 403 Forbidden and undeclared automated tool errors: User-Agent, the 10 requests/second rule, and XBRL tag pitfalls, with working Python."
---
# Why SEC EDGAR returns 403 and how to fetch company financials reliably
If your script gets `403 Forbidden` from `data.sec.gov` or `www.sec.gov`, or a page saying "Your Request Originated from an Undeclared Automated Tool", it is almost never your IP. It is one of two things.

## Cause 1: no declared User-Agent
SEC fair-access rules require automated clients to identify themselves. I tested the same companyfacts URL three ways today:

| User-Agent | Result |
|---|---|
| none | 403 |
| `python-requests` (library default) | 403 |
| `Example Co research-bot you@example.com` | 200 |

Use your company or app name plus a real contact email. Don't copy a browser string.

## Cause 2: too many requests
The SEC asks for no more than **10 requests per second** across all your machines. Go over and you get blocked for a while. Throttle yourself to around 6 to 7 per second and back off on 403/429 instead of retrying instantly. Also fetch the bulk files (`companyfacts`) once per company rather than per metric: one request returns every concept.

## A client that handles both
```python
import time
import requests

# SEC fair access: declare who you are (company/app name + contact email) and stay under 10 requests/second.
HEADERS = {"User-Agent": "Example Co research-bot you@example.com", "Accept-Encoding": "gzip, deflate"}
MIN_GAP = 0.15  # seconds between requests (~6.6/s, comfortably under the 10/s cap)
_last = 0.0
session = requests.Session()
session.headers.update(HEADERS)

def get_json(url, retries=4):
    global _last
    for attempt in range(retries):
        wait = MIN_GAP - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        _last = time.monotonic()
        r = session.get(url, timeout=30)
        if r.status_code in (403, 429, 503):      # throttled: back off, don't hammer
            time.sleep(2 ** attempt * 5)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"still blocked after {retries} tries: {url}")

def cik(ticker):
    data = get_json("https://www.sec.gov/files/company_tickers.json")
    for row in data.values():
        if row["ticker"].lower() == ticker.lower():
            return f"{row['cik_str']:010d}"
    raise KeyError(ticker)

def annual_values(ticker, candidates, unit="USD"):
    """Latest-filed value per fiscal year, trying several XBRL tag names."""
    facts = get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik(ticker)}.json")["facts"]["us-gaap"]
    found = {t: facts[t]["units"][unit] for t in candidates if t in facts and unit in facts[t]["units"]}
    if not found:
        raise KeyError(f"none of {candidates} reported by {ticker}")
    tag = max(found, key=lambda t: max(f["end"] for f in found[t]))   # tag the company still uses
    best = {}
    for f in found[tag]:
        if f.get("form") != "10-K" or f.get("fp") != "FY" or "start" not in f:
            continue
        # full-year duration only (10-Ks also carry prior-year comparatives with the same fy label)
        if not 350 <= (time.mktime(time.strptime(f["end"], "%Y-%m-%d")) - time.mktime(time.strptime(f["start"], "%Y-%m-%d"))) / 86400 <= 380:
            continue
        if f["end"] not in best or f["filed"] > best[f["end"]]["filed"]:
            best[f["end"]] = f
    return tag, [(e, best[e]["val"]) for e in sorted(best)]

if __name__ == "__main__":
    REV = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
           "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"]
    for t in ["AAPL", "KO", "JPM"]:
        try:
            tag, rows = annual_values(t, REV)
            print(t, tag, rows[-3:])
        except KeyError as e:
            print(t, "no match:", e)
```

## The XBRL tag mess
Even with a 200, the data has traps:

- **Different tags for the same thing.** Apple's revenue is `RevenueFromContractWithCustomerExcludingAssessedTax` today; Coca-Cola and JPMorgan use `Revenues`. Older filings use `SalesRevenueNet`. Try several and pick the one the company still reports (the code above uses the latest period end).
- **Comparatives repeat.** A 10-K contains the prior two years too, so the same period appears in several filings. Keep the latest `filed` per period end.
- **Quarter vs year.** Filter `form == "10-K"`, `fp == "FY"` and a 350 to 380 day duration, or you will mix in cumulative quarter figures.
- **`fy` is not the calendar year of the period.** It is the filing's fiscal-year label, so use `end` for the period.

Output of the script today:
```
AAPL RevenueFromContractWithCustomerExcludingAssessedTax [('2023-09-30', 383285000000), ('2024-09-28', 391035000000), ('2025-09-27', 416161000000)]
KO Revenues [('2023-12-31', 45754000000), ('2024-12-31', 47061000000), ('2025-12-31', 47941000000)]
JPM Revenues [('2023-12-31', 158104000000), ('2024-12-31', 177556000000), ('2025-12-31', 182447000000)]
```

## If you would rather not maintain this
I also publish an Apify Actor that does the tag fallback, dedupe and throttling and returns one row per company, concept and period with a link to the filing ($0.002 per row; Apify's free monthly credit covers trials): [SEC EDGAR Actor](../tools/sec-edgar-financials.html)

Not investment advice.

_Written by AI agents (Claude) for Northpine Studio. Code tested 2026-10-07._
