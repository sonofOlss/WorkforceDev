# Southwest Valley Workforce Dashboard

An automatically updating dashboard of job postings, in-demand job titles, and
in-demand skills for the **southwest Phoenix valley only**: Avondale, Goodyear,
Buckeye, Tolleson, Litchfield Park, and Laveen. Each city is searched with a
small radius, and any posting whose location names somewhere outside these
communities is filtered out, so jobs from central/west Phoenix, Glendale, and
the rest of the metro never enter the database.

## How it works

```
Adzuna jobs API ──> fetch_jobs.py ──> data/jobs.db (growing SQLite database)
                                          │
                                    aggregate.py  (skill matching from scripts/skills.py)
                                          │
                                  data/dashboard.json
                                          │
                                   site/index.html  ──>  GitHub Pages
```

A GitHub Actions workflow (`.github/workflows/update-dashboard.yml`) runs
**every day at 6:00 AM Phoenix time**. It:

1. Pulls fresh job postings for each Southwest Valley city from the
   [Adzuna API](https://developer.adzuna.com/) and adds new ones to
   `data/jobs.db` (duplicates are skipped, so the database grows over time).
2. Re-counts job titles, extracts skills from posting titles/descriptions
   using the lexicon in `scripts/skills.py`, and writes `data/dashboard.json`.
3. Commits the updated data back to the repo and republishes the dashboard
   to GitHub Pages.

Until API credentials are added, the pipeline runs on the bundled sample data
(`data/sample_jobs.json`) so the dashboard still renders — it will show a
yellow **SAMPLE DATA** badge.

## One-time setup (about 10 minutes)

1. **Get free Adzuna API credentials.** Sign up at
   <https://developer.adzuna.com/signup>. You'll receive an **App ID** and an
   **App Key**.
2. **Add them as repository secrets.** In this repo on GitHub go to
   *Settings → Secrets and variables → Actions → New repository secret* and
   create two secrets:
   - `ADZUNA_APP_ID`
   - `ADZUNA_APP_KEY`
3. **Turn on GitHub Pages.** Go to *Settings → Pages* and set **Source** to
   **GitHub Actions**.
4. **Run it once by hand.** Go to the *Actions* tab, pick
   *Update workforce dashboard*, and click *Run workflow*. When it finishes,
   your dashboard is live at `https://<your-username>.github.io/<repo-name>/`
   and will refresh itself every morning.

## Customizing

- **Cities / search radius:** edit the `CITIES` list in `scripts/fetch_jobs.py`.
- **Skills tracked:** add or edit entries in `scripts/skills.py`. Changes apply
  retroactively to everything already in the database on the next run.
- **Update schedule:** change the `cron` line in
  `.github/workflows/update-dashboard.yml`
  (current: `0 13 * * *` = 13:00 UTC = 6 AM Phoenix).
- **Charts / look and feel:** everything is in `site/index.html`.

## Running locally

No installs needed beyond Python 3.10+ (everything uses the standard library):

```bash
python workforce-dashboard/scripts/make_sample_data.py   # optional: regenerate sample data
python workforce-dashboard/scripts/fetch_jobs.py         # needs ADZUNA_APP_ID / ADZUNA_APP_KEY env vars
python workforce-dashboard/scripts/aggregate.py          # builds data/dashboard.json

# view the dashboard
cp workforce-dashboard/data/dashboard.json workforce-dashboard/site/
cd workforce-dashboard/site && python -m http.server 8000
# then open http://localhost:8000
```

## Notes & limits

- Skill counts come from keyword matching, so they're estimates of demand,
  not exact figures.
- Adzuna's free tier allows plenty of calls for this schedule (~12 requests/day).
- Salary figures are *advertised* salaries and only appear when a posting
  includes them.
- The database keeps every posting it has ever seen (`first_seen`/`last_seen`
  columns), which makes longer-term trend analysis possible later.
