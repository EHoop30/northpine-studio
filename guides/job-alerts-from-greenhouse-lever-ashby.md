---
title: "Free job alert for Greenhouse and Lever"
description: "How to watch company career pages for new openings and get only the jobs you haven't seen, using public ATS job-board APIs and a scheduled Apify run."
---
# Build a job alert for Greenhouse, Lever and Ashby boards

Many startups post jobs through Greenhouse, Lever or Ashby. Each offers a public job-board API (the same data that powers the company's careers page), so you can watch a list of employers without scraping anything.

## The manual way
- Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs`
- Lever: `https://api.lever.co/v0/postings/<slug>?mode=json`
- Ashby: `https://api.ashbyhq.com/posting-api/job-board/<slug>`

Three APIs, three response shapes. For one or two companies, a short script is fine. Remember to store the job IDs you've seen, so each run reports only what's new.

## The shortcut
If you'd rather not maintain the glue code, our [ATS jobs Actor](../tools/ats-jobs-aggregator.html) does the normalizing: one row per job with title, department, location, remote flag, salary range when published, posted date and apply link.

Example input:
```json
{"companies":["greenhouse:stripe","lever:spotify","ashby:ashby"],"keywords":["engineer"],"remoteOnly":true,"maxItems":100}
```
Turn on new-jobs-only mode and put the run on an Apify schedule (daily is plenty). Send the dataset to email or a webhook with Apify's integrations.

## Tips
- Missing salary usually means the company didn't publish one; don't treat null as zero.
- Respect each board's terms and be gentle with request rates.
- Slugs are the part of the careers URL after the platform's domain.

_Pay per result; Apify's free credit covers a trial. Written by AI agents (Claude) for Northpine Studio._
