# Bucketed Balance Planner

This is a small static web app that lets you:

- Input your current bank balance
- Define multiple buckets with an allocation percentage (used for initial split), a fixed periodic increase (applied twice monthly), and a goal amount
- Configure a main periodic increase amount and the two dates in the month when increases happen
- Simulate N months ahead to see how bucket balances progress
- See donut charts showing progress vs goal for each bucket

How to run

Open `index.html` in your browser (no server required). For example:

macOS / Linux:
```bash
open index.html
```

Windows (PowerShell):
```powershell
start index.html
```

Files

- `index.html` – app UI
- `styles.css` – basic styles
- `script.js` – main logic and Chart.js usage

Notes & behavior

- Initial allocation: the current balance is split into buckets according to each bucket's `%` field.
- Periodic increases: every month there are two events (the two configured dates). For simulation, the app simply applies the configured main increase amount to the bank balance and adds each bucket's configured `periodic` fixed amount to that bucket on each event.
- Charts: each bucket displays a donut that shows `completed` vs `remaining` toward its goal.

If you'd like, I can:

- Add a proper scheduler that calculates actual calendar dates and partial months
- Allow fixed-amount allocations (instead of percentages)
- Export/import a JSON config or add CSV reports
# SQL-Data-Analytics