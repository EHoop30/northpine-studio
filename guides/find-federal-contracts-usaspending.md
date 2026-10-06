---
title: "Find federal contracts and grants on USAspending"
description: "A practical way to list who won US federal contracts or grants for a topic, agency or amount, as a spreadsheet-ready table."
---
# Find federal contracts and grants on USAspending

USAspending.gov publishes every US federal award. It's useful for small contractors sizing a market, grant writers researching who funds what, and journalists following the money. Its search screen is fine for one-off lookups; a table is better for comparison.

## What to decide first
1. **Award type:** contracts, grants, loans or direct payments behave differently, so pick one per search.
2. **Date range:** use fiscal-year-sized windows to keep results comparable.
3. **Floor amount:** a minimum such as $1M filters out noise.
4. **Keywords:** use the vocabulary agencies use ("photovoltaic" as well as "solar").

## Get it as rows
Our [USAspending Actor](../tools/usaspending-awards) wraps the official API and returns awards largest first, with recipient, amount, agency, dates and a link back to the record.

Example input:
```json
{"keywords":["solar"],"awardType":"contracts","startDate":"2024-01-01","endDate":"2024-12-31","minAmount":1000000,"maxItems":100}
```
Open the result in a spreadsheet, group by recipient or sub-agency, and you can see where the money concentrates.

## Caveats
Amounts are as reported and can lag or be revised. Descriptions are short and inconsistent, so check the linked award page before you rely on a figure.

_Pay per result; Apify's free credit covers a trial. Written by AI agents (Claude) for Northpine Studio. Not affiliated with the US government._
