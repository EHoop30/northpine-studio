"""Regenerate the Northpine data pages from public APIs. Run: python scripts/generate.py"""
import requests, datetime as dt, pathlib
UA = {"User-Agent": "Northpine Studio agentco.works@gmail.com"}
OUT = pathlib.Path(__file__).resolve().parent.parent / "data"
today = dt.date.today()
week_ago = today - dt.timedelta(days=7)

def page(title, desc, intro, header, rows, actor_url, actor_name, source):
    lines = ["---", f'title: "{title}"', f'description: "{desc}"', "---", f"# {title}", "",
             f"_Updated {today.isoformat()}. Source: {source}. Generated automatically; figures are as reported by the source._", "",
             intro, "", "| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]
    lines += ["", f"Want this data for your own filters or on a schedule? Run the [{actor_name}]({actor_url}).", "",
              "_Made by AI agents (Claude) for Northpine Studio._", ""]
    return "\n".join(lines)

def contracts():
    body = {"filters": {"award_type_codes": ["A", "B", "C", "D"],
            "time_period": [{"start_date": week_ago.isoformat(), "end_date": today.isoformat(), "date_type": "new_awards_only"}]},
            "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency", "Start Date"],
            "sort": "Award Amount", "order": "desc", "limit": 15, "page": 1}
    r = requests.post("https://api.usaspending.gov/api/v2/search/spending_by_award/", json=body, headers=UA, timeout=60)
    r.raise_for_status()
    rows = [(a["Recipient Name"], f"${a['Award Amount']:,.0f}", a["Awarding Agency"], a["Start Date"], a["Award ID"])
            for a in r.json()["results"]]
    return page("Largest new federal contracts this week",
        "The 15 largest federal contracts with a start date in the last 7 days, from USAspending.gov.",
        f"Contracts (not grants or loans) that began between {week_ago} and {today}, largest first. Amounts are the current obligated value reported at the time of the query and can change.",
        ["Recipient", "Amount", "Agency", "Start", "Award ID"], rows,
        "https://apify.com/northpine-studio/usaspending-awards", "USAspending awards Actor", "USAspending.gov API")

def trials():
    p = {"filter.overallStatus": "NOT_YET_RECRUITING,RECRUITING", "filter.advanced": "AREA[Phase]PHASE3 AND AREA[StudyFirstPostDate]RANGE[%s,MAX]" % week_ago.isoformat(),
         "sort": "EnrollmentCount:desc", "pageSize": 15, "countTotal": "true"}
    r = requests.get("https://clinicaltrials.gov/api/v2/studies", params=p, headers=UA, timeout=60)
    r.raise_for_status()
    d = r.json()
    rows = []
    for s in d["studies"]:
        x = s["protocolSection"]
        rows.append((x["sponsorCollaboratorsModule"]["leadSponsor"]["name"], x["identificationModule"]["briefTitle"][:90],
                     x.get("designModule", {}).get("enrollmentInfo", {}).get("count", ""), x["identificationModule"]["nctId"]))
    return page("New Phase 3 trials posted this week",
        "Phase 3 trials first posted on ClinicalTrials.gov in the last 7 days, largest enrollment first.",
        f"{d.get('totalCount', len(rows))} Phase 3 studies (including Phase 2/3) were first posted since {week_ago} and are recruiting or about to. The 15 with the largest planned enrollment:",
        ["Sponsor", "Title", "Planned enrollment", "NCT ID"], rows,
        "https://apify.com/northpine-studio/clinical-trials-search", "clinical trials search Actor", "ClinicalTrials.gov API v2")

BOARDS = ["stripe", "airbnb", "databricks", "anthropic", "figma", "cloudflare", "datadog", "coinbase", "discord", "instacart", "reddit", "pinterest", "robinhood", "asana", "gitlab"]

def hiring():
    rows = []
    for slug in BOARDS:
        r = requests.get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs", headers=UA, timeout=30)
        if r.status_code != 200:
            continue
        jobs = r.json()["jobs"]
        ml = [j for j in jobs if any(k in j["title"].lower() for k in ("machine learning", " ml ", "ml engineer", "ai engineer", "research scientist"))]
        rows.append((slug, len(jobs), len(ml), ml[0]["title"] if ml else ""))
    rows.sort(key=lambda r: -r[2])
    return page("Who is hiring ML roles on Greenhouse",
        "Open machine learning and AI roles at 15 well-known companies that publish Greenhouse job boards.",
        f"Counts of open jobs on each company's public Greenhouse board on {today}, and how many titles mention machine learning, ML engineer, AI engineer or research scientist. A title match is a rough filter, not a definition. Only boards that responded are listed.",
        ["Board", "Open jobs", "ML/AI titles", "Example title"], rows,
        "https://apify.com/northpine-studio/ats-jobs-aggregator", "ATS jobs aggregator Actor", "public Greenhouse job-board API")

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "federal-contracts-this-week.md").write_text(contracts(), encoding="utf-8")
    (OUT / "new-phase3-trials-this-week.md").write_text(trials(), encoding="utf-8")
    (OUT / "ml-hiring-greenhouse.md").write_text(hiring(), encoding="utf-8")
    print("ok")
