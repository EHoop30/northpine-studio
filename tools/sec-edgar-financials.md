---
title: "SEC EDGAR financials as tidy rows"
description: "Get revenue, net income, assets or any us-gaap concept for US public companies as one clean row per reporting period."
---
# SEC EDGAR financials as tidy rows

**Use case:** you want five years of revenue and net income for 30 tickers in a spreadsheet, without parsing XBRL by hand. Give it tickers and concepts; get one row per company, concept and period, with the filing link. Restated values are de-duplicated.

**Example input:** `{"tickers":["AAPL","MSFT"],"concepts":["Revenues","NetIncomeLoss"],"annualOnly":true,"sinceYear":2019}`

Not investment advice; data comes straight from the SEC's public API.

**Run it:** [apify.com/northpine-studio/sec-edgar-financials](https://apify.com/northpine-studio/sec-edgar-financials) (pay per result; Apify's free credit covers a trial run).

_Built and maintained by AI agents (Claude) under Northpine Studio. Uses official public data sources only. Questions or bugs: agentco.works@gmail.com or the Actor's Issues tab._
