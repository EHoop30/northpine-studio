---
title: "Get SEC financial statement data into a spreadsheet"
description: "Pull revenue, net income and assets for US public companies from SEC XBRL data as one row per period, ready for Excel or Google Sheets."
---
# Get SEC financial statement data into a spreadsheet

Every US public company files financial statements with the SEC in XBRL, and the SEC serves them through a free API (`data.sec.gov`, "companyfacts"). The raw JSON is awkward: one blob per company, many concepts, restated values repeated across filings.

## What you need to handle
- **Concept names differ by company.** Revenue may be `Revenues` or `RevenueFromContractWithCustomerExcludingAssessedTax`. Request several.
- **Restatements:** the same period appears in several filings; keep the latest filed value.
- **Annual vs quarterly:** filter on form (10-K or 10-Q) and fiscal period.
- **Courtesy:** the SEC requires a descriptive User-Agent and asks for under 10 requests per second.

## Skip the plumbing
Our [SEC EDGAR Actor](../tools/sec-edgar-financials) does this and returns one row per company, concept and period, with a link to the filing.

```json
{"tickers":["AAPL","MSFT"],"concepts":["Revenues","NetIncomeLoss","Assets"],"forms":["10-K"],"annualOnly":true,"sinceYear":2019}
```
Export the dataset as CSV, then pivot by fiscal year in your spreadsheet.

_Not investment advice. Pay per result; Apify's free credit covers a trial. Written by AI agents (Claude) for Northpine Studio._
