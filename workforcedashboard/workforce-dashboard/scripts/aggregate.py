"""Build dashboard.json from the jobs database.

Reads workforce-dashboard/data/jobs.db (or, if the database doesn't exist or
is empty, the bundled sample data) and writes the aggregated statistics that
the dashboard page renders.

Run:
    python workforce-dashboard/scripts/aggregate.py
"""

import json
import re
import sqlite3
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from skills import SKILLS

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "jobs.db"
SAMPLE_PATH = DATA_DIR / "sample_jobs.json"
OUT_PATH = DATA_DIR / "dashboard.json"

TOP_TITLES = 15
TOP_SKILLS = 20
TREND_WEEKS = 12

# Compile the lexicon once: skill -> (category, [compiled patterns])
COMPILED = {
    name: (info["category"], [re.compile(p, re.IGNORECASE) for p in info["patterns"]])
    for name, info in SKILLS.items()
}

# Noise stripped from titles so "RN - Med Surg Nights $5k Sign-On!" and
# "Registered Nurse Med/Surg" group more sensibly.
TITLE_NOISE = re.compile(
    r"""\$[\d,.]+[kK]?(\s*sign[- ]?on)?(\s*bonus)?   # pay/bonus mentions
        |\b(immediate(ly)?|urgent(ly)?|hiring|now|asap)\b
        |\b(full[- ]?time|part[- ]?time|ft|pt|prn|per\s+diem)\b
        |\b(day|night|swing|weekend|1st|2nd|3rd)\s+shifts?\b
        |[!*#]+
    """,
    re.IGNORECASE | re.VERBOSE,
)


def load_jobs() -> tuple[list[dict], str]:
    """Return (jobs, source_label). Prefers the live database."""
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = [dict(r) for r in conn.execute("SELECT * FROM jobs")]
        conn.close()
        if rows:
            return rows, "live"
    if not SAMPLE_PATH.exists():
        import make_sample_data
        make_sample_data.main()
    return json.loads(SAMPLE_PATH.read_text()), "sample"


ACRONYMS = {"It": "IT", "Rn": "RN", "Lpn": "LPN", "Cna": "CNA", "Cdl": "CDL",
            "Cdl-A": "CDL-A", "Cdl-B": "CDL-B", "Hvac": "HVAC", "Cnc": "CNC",
            "Er": "ER", "Icu": "ICU", "Emt": "EMT", "Hr": "HR", "Qa": "QA"}


def normalize_title(title: str) -> str:
    t = TITLE_NOISE.sub(" ", title)
    t = re.split(r"\s*[-–|/(]\s*", t, maxsplit=1)[0]  # keep text before a dash/pipe/paren
    t = re.sub(r"\s+", " ", t).strip()
    t = t.title() if t else title.strip().title()
    return " ".join(ACRONYMS.get(w, w) for w in t.split())


def extract_skills(text: str) -> set[str]:
    found = set()
    for name, (_category, patterns) in COMPILED.items():
        if any(p.search(text) for p in patterns):
            found.add(name)
    return found


def main() -> None:
    jobs, source = load_jobs()

    title_counts: Counter = Counter()
    title_salaries: defaultdict = defaultdict(list)
    skill_counts: Counter = Counter()
    category_counts: Counter = Counter()
    city_counts: Counter = Counter()
    week_counts: Counter = Counter()
    skill_category: dict = {}

    dates = [j["posted_date"] for j in jobs if j.get("posted_date")]
    anchor = max(datetime.fromisoformat(d) for d in dates) if dates else datetime.now()

    for job in jobs:
        norm = normalize_title(job["title"])
        title_counts[norm] += 1
        if job.get("salary_min") and job.get("salary_max"):
            title_salaries[norm].append((job["salary_min"] + job["salary_max"]) / 2)

        text = f"{job['title']} {job.get('description') or ''}"
        for skill in extract_skills(text):
            skill_counts[skill] += 1
            cat = COMPILED[skill][0]
            skill_category[skill] = cat
            category_counts[cat] += 1

        city_counts[job.get("city") or "Other"] += 1

        if job.get("posted_date"):
            posted = datetime.fromisoformat(job["posted_date"])
            weeks_ago = (anchor - posted).days // 7
            if 0 <= weeks_ago < TREND_WEEKS:
                week_start = (anchor - timedelta(days=weeks_ago * 7 + anchor.weekday())).date()
                week_counts[week_start.isoformat()] += 1

    n_jobs = len(jobs)
    top_titles = [
        {
            "title": t,
            "count": c,
            "median_salary": round(statistics.median(title_salaries[t])) if title_salaries[t] else None,
        }
        for t, c in title_counts.most_common(TOP_TITLES)
    ]
    top_skills = [
        {
            "skill": s,
            "category": skill_category[s],
            "count": c,
            "pct": round(100 * c / n_jobs, 1),
        }
        for s, c in skill_counts.most_common(TOP_SKILLS)
    ]

    dashboard = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "data_source": source,
        "total_postings": n_jobs,
        "total_employers": len({j.get("company") for j in jobs if j.get("company")}),
        "distinct_titles": len(title_counts),
        "top_titles": top_titles,
        "top_skills": top_skills,
        "skills_by_category": [
            {"category": c, "count": n} for c, n in category_counts.most_common()
        ],
        "jobs_by_city": [
            {"city": c, "count": n} for c, n in city_counts.most_common()
        ],
        "postings_by_week": [
            {"week": w, "count": week_counts[w]} for w in sorted(week_counts)
        ],
    }

    OUT_PATH.write_text(json.dumps(dashboard, indent=1))
    print(
        f"Wrote {OUT_PATH.name}: {n_jobs} postings ({source} data), "
        f"{len(title_counts)} distinct titles, {len(skill_counts)} skills detected."
    )


if __name__ == "__main__":
    main()
