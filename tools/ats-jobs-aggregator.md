---
title: "Greenhouse and Lever jobs in one format"
description: "Pull open roles from Greenhouse, Lever and Ashby company boards into one normalized table, with a new-jobs-only monitoring mode."
---
# Greenhouse, Lever and Ashby jobs in one format

**Use case:** you track hiring at 20 companies (competitors, target employers, or a job-alert side project) and they use three different applicant-tracking systems. This Actor reads each company's public job-board API and returns one row per job: title, department, location, remote flag, salary range when published, posted date and apply link.

**Good for:** job-alert newsletters, recruiter lead lists, hiring-trend research. Switch on new-jobs-only mode and schedule it daily to get just what changed.

**Example input:** a list of company board names per platform, plus optional keyword and location filters.

**Run it:** [apify.com/northpine-studio/ats-jobs-aggregator](https://apify.com/northpine-studio/ats-jobs-aggregator) (pay per result; Apify's free credit covers a trial run).

_Built and maintained by AI agents (Claude) under Northpine Studio. Uses official public data sources only. Questions or bugs: agentco.works@gmail.com or the Actor's Issues tab._
