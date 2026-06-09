"""Fetch job postings for the Southwest Valley from the Adzuna API and store
them in the SQLite database at workforce-dashboard/data/jobs.db.

Requires two environment variables (free at https://developer.adzuna.com/):
    ADZUNA_APP_ID
    ADZUNA_APP_KEY

If they are not set, the script exits gracefully so the rest of the pipeline
can still run on whatever data is already in the database (or on the bundled
sample data the first time).

Run from the repository root or anywhere:
    python workforce-dashboard/scripts/fetch_jobs.py
"""

import os
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "jobs.db"

# Southwest Valley cities to search. "distance" is the search radius in km.
CITIES = [
    {"name": "Avondale", "where": "Avondale, AZ", "distance": 8},
    {"name": "Goodyear", "where": "Goodyear, AZ", "distance": 10},
    {"name": "Buckeye", "where": "Buckeye, AZ", "distance": 12},
    {"name": "Tolleson", "where": "Tolleson, AZ", "distance": 6},
    {"name": "Litchfield Park", "where": "Litchfield Park, AZ", "distance": 6},
    {"name": "Laveen", "where": "Laveen, AZ", "distance": 6},
]

PAGES_PER_CITY = 2          # 2 pages x 50 results = up to 100 postings per city per run
RESULTS_PER_PAGE = 50
API_BASE = "https://api.adzuna.com/v1/api/jobs/us/search"

# Keep the dashboard strictly southwest Phoenix valley: a radius search near a
# city boundary can return postings from neighboring areas (west Phoenix,
# Glendale, etc.), so any posting whose own location text names somewhere
# outside these communities is rejected. Postings with no location text are
# kept, since they were found by a tight search around one of our cities.
ALLOWED_AREAS = [
    "avondale", "goodyear", "buckeye", "tolleson",
    "litchfield park", "litchfield", "laveen", "cashion",
]


def in_southwest_valley(job: dict) -> bool:
    location = ((job.get("location") or {}).get("display_name") or "").lower()
    if not location:
        return True
    return any(area in location for area in ALLOWED_AREAS)


def ensure_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id          TEXT PRIMARY KEY,   -- Adzuna posting id
            title       TEXT NOT NULL,
            company     TEXT,
            city        TEXT,               -- search city the posting was found under
            location    TEXT,               -- location string from the posting itself
            category    TEXT,
            description TEXT,
            salary_min  REAL,
            salary_max  REAL,
            posted_date TEXT,               -- ISO date the posting went up
            url         TEXT,
            first_seen  TEXT NOT NULL,      -- when this pipeline first saw it
            last_seen   TEXT NOT NULL       -- most recent run that still saw it
        )
        """
    )
    conn.commit()


def fetch_page(app_id: str, app_key: str, where: str, distance_km: int, page: int) -> dict:
    params = urllib.parse.urlencode(
        {
            "app_id": app_id,
            "app_key": app_key,
            "where": where,
            "distance": distance_km,
            "results_per_page": RESULTS_PER_PAGE,
            "sort_by": "date",
            "content-type": "application/json",
        }
    )
    url = f"{API_BASE}/{page}?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


def upsert_job(conn: sqlite3.Connection, job: dict, city: str, now: str) -> bool:
    """Insert a posting or refresh its last_seen. Returns True if it was new."""
    job_id = str(job.get("id", ""))
    if not job_id or not job.get("title"):
        return False
    existing = conn.execute("SELECT 1 FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if existing:
        conn.execute("UPDATE jobs SET last_seen = ? WHERE id = ?", (now, job_id))
        return False
    conn.execute(
        """INSERT INTO jobs (id, title, company, city, location, category, description,
                             salary_min, salary_max, posted_date, url, first_seen, last_seen)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            job_id,
            job.get("title", "").strip(),
            (job.get("company") or {}).get("display_name"),
            city,
            (job.get("location") or {}).get("display_name"),
            (job.get("category") or {}).get("label"),
            job.get("description", ""),
            job.get("salary_min"),
            job.get("salary_max"),
            (job.get("created") or "")[:10] or None,
            job.get("redirect_url"),
            now,
            now,
        ),
    )
    return True


def main() -> int:
    app_id = os.environ.get("ADZUNA_APP_ID", "").strip()
    app_key = os.environ.get("ADZUNA_APP_KEY", "").strip()
    if not app_id or not app_key:
        print("ADZUNA_APP_ID / ADZUNA_APP_KEY not set -- skipping fetch.")
        print("The dashboard will be built from existing or sample data instead.")
        return 0

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    total_new = 0
    for spec in CITIES:
        city_new = 0
        for page in range(1, PAGES_PER_CITY + 1):
            try:
                payload = fetch_page(app_id, app_key, spec["where"], spec["distance"], page)
            except Exception as exc:  # noqa: BLE001 - keep going for other cities
                print(f"  ! {spec['name']} page {page} failed: {exc}")
                break
            results = payload.get("results", [])
            for job in results:
                if not in_southwest_valley(job):
                    continue
                if upsert_job(conn, job, spec["name"], now):
                    city_new += 1
            conn.commit()
            if len(results) < RESULTS_PER_PAGE:
                break
            time.sleep(1)  # be polite to the API
        print(f"  {spec['name']}: {city_new} new postings")
        total_new += city_new

    total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    print(f"Done. {total_new} new postings this run; {total} total in the database.")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
