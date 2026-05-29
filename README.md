# Staffwizard Scheduling

Automatic employee scheduling service that builds a weekly schedule by prioritizing:
- lower overtime
- lower pay rate and travel distance (weighted score)
- no overlapping shifts
- continuity for permanent shifts from the previous week

## What This Service Does

This project exposes a Flask API endpoint that:
1. Reads scheduling data for a target week and the prior week from Staffwizard APIs.
2. Detects permanent shifts in the prior week.
3. Maps those permanent shifts to equivalent shifts in the target week.
4. Builds a compatibility map of which employees can work each post/shift.
5. Assigns shifts while minimizing overtime and avoiding overlaps.
6. Computes overtime metrics and generates a summary (optionally using OpenAI).

Main entry point: [src/main.py](src/main.py)

## Project Structure

Core modules under [src](src):
- [src/main.py](src/main.py): Flask app and orchestration pipeline for the scheduling request.
- [src/get_info_from_api.py](src/get_info_from_api.py): Pulls employee/post data for selected and previous week.
- [src/permanent_shifts.py](src/permanent_shifts.py): Finds permanent shifts and maps them into the future week.
- [src/assign_permenent_shifts.py](src/assign_permenent_shifts.py): Pre-assigns mapped permanent shifts if no overlap exists.
- [src/compatible_employees_for_posts.py](src/compatible_employees_for_posts.py): Builds candidates per shift and score = pay_rate + beta * distance.
- [src/shift_times.py](src/shift_times.py): Shift duration and overtime helper calculations.
- [src/rate_and_distance.py](src/rate_and_distance.py): Secondary sorting by score inside overtime groups.
- [src/overlapp.py](src/overlapp.py): Shift overlap validation.
- [src/assign_shifts.py](src/assign_shifts.py): Main assignment algorithm and empty-shift tracking.
- [src/empty_posts.py](src/empty_posts.py): Removes posts with zero candidate shifts.
- [src/calculate_overtime.py](src/calculate_overtime.py): Weekly and repeated-day overtime extraction.
- [src/summary.py](src/summary.py): Name mapping, summary text generation, and optional OpenAI summary.
- [src/duplicates.py](src/duplicates.py): Helper for repeated-day detection.

Utilities:
- [test_api.py](test_api.py): Quick local client for calling the endpoint.
- [restart_flask.sh](restart_flask.sh): Restarts the Flask process on port 5000.

## API

### POST /get_schedule

Endpoint: `http://127.0.0.1:5000/get_schedule`

Request JSON:

```json
{
	"subdomain": "ATZS",
	"branch": "61",
	"start": "2024-12-02",
	"end": "2024-12-09",
	"mode": "formal"
}
```

Fields:
- `subdomain`: Staffwizard subdomain.
- `branch`: Branch identifier.
- `start`: Week start date in `YYYY-MM-DD`.
- `end`: Week end date in `YYYY-MM-DD`.
- `mode`: Summary style (`formal` or `informal`).

Success response contains:
- `Posts`: Post/shift structure with assignments (`Assigned_to`).
- `Employees`: Assigned shifts grouped by employee id.
- `Summary`: Tuple-like payload of raw overtime text + generated summary.
- `Empty`: Shifts that could not be assigned.

Potential error responses:
- Invalid or missing JSON body.
- Missing schedule data for prior or selected week.
- Unexpected runtime exception.

## Scheduling Logic (High Level)

For each request, the service performs:
1. Data fetch for target week and previous week.
2. Permanent shift detection from prior-week employee shifts.
3. Permanent shift mapping by day/start/end/post.
4. Candidate generation by post compatibility and non-overlap with permanent shifts.
5. Assignment strategy:
	 - sort candidates by lower weekly overtime first
	 - break ties by lower score (`pay_rate + beta * distance`)
	 - enforce overlap checks with already assigned shifts
	 - fallback to first non-overlapping candidate when needed
6. Overtime and summary generation.

## Setup

From project root [Staffwizard_scheduling](.):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or use your existing environment in [sched](../sched) if preferred.

## Run Locally

The app file is in [src/main.py](src/main.py), so run from the [src](src) directory:

```bash
cd src
python3 main.py
```

Flask starts on `0.0.0.0:5000`.

Then test with:

```bash
python3 test_api.py
```

Or via curl:

```bash
curl -X POST http://127.0.0.1:5000/get_schedule \
	-H "Content-Type: application/json" \
	-d '{
		"subdomain": "ATZS",
		"branch": "61",
		"start": "2024-12-02",
		"end": "2024-12-09",
		"mode": "formal"
	}'
```

## Notes and Limitations

- The code currently sets an OpenAI API key directly in [src/main.py](src/main.py). Move this to an environment variable before production use.
- The OpenAI summary call in [src/summary.py](src/summary.py) uses model `gpt-3.5-turbo`.
- Several module and function names include typos (`permenent`, `compatibile`, `overlapp`). They are kept as-is to match imports.
- Overlap handling is day-based and time-window based; verify behavior for overnight edge cases with your real data.

## Troubleshooting

- If imports fail when launching, make sure you are running from [src](src).
- If API calls fail, verify network access and that your Staffwizard endpoints are reachable.
- If summary generation fails, scheduling still returns data, but summary may include an OpenAI error string.
