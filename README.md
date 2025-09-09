DWTS Fantasy Draft
===================

A minimal FastAPI + SQLite app for collecting and viewing Dancing With The Stars fantasy draft submissions.

Quickstart
----------

1. Python 3.13 is required.
2. Create venv and install deps:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

3. Run the server:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in a browser.

API
---

- GET /api/contestants – list contestants
- POST /api/contestants – create contestant { name, bio? }
- GET /api/submissions – list submissions
- POST /api/submissions – create submission { display_name, email?, picks:[id] }

Server validates:
- Unique picks
- At least DWTS_MIN_PICKS (default 3) picks
- Contestant id existence

Data
----

On startup, contestants seed from /workspace/data/contestants.json if DB empty. Edit that file and restart to change the list.

SQLite DB path: /workspace/data/app.db (override with DWTS_DB_PATH).

Configuration
-------------

- DWTS_MIN_PICKS – minimum number of picks (default: 3)
- DWTS_DB_PATH – SQLite file path (default: /workspace/data/app.db)
- DWTS_CONTESTANTS_PATH – seed file path (default: /workspace/data/contestants.json)

Deployment notes
----------------

- Behind a reverse proxy, run with: uvicorn app.main:app --proxy-headers --forwarded-allow-ips='*'
- For persistence, mount a volume to /workspace/data.
