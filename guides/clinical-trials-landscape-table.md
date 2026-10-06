---
title: "Build a clinical trials landscape table"
description: "List every trial for a condition, drug or sponsor from ClinicalTrials.gov as a flat table for competitor and pipeline research."
---
# Build a clinical trials landscape table

ClinicalTrials.gov lists hundreds of thousands of studies. For pipeline or competitor research, you usually want a table: who is running what, in which phase, with how many participants, and where.

## A workable method
1. Start with a condition (and synonyms) or a drug name.
2. Narrow by phase and status (for example Phase 3, recruiting).
3. Add columns you'll compare: sponsor, enrollment, start and completion dates, interventions, countries.
4. Sort by sponsor to see who is concentrated in the area, and by completion date to see what reads out soon.

## Get the table
Our [ClinicalTrials.gov Actor](../tools/clinical-trials-search) queries the official NLM API and returns flat rows with no personal contact details.

## Caveats
Registry entries are self-reported and sometimes stale. Statuses and dates change, so re-run before you rely on them. This is research data, not medical advice.

_Pay per result; Apify's free credit covers a trial. Written by AI agents (Claude) for Northpine Studio._
