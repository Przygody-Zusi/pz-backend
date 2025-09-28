# Przygody Zusi Backend

## Prerequisites

- Python 3.11+
- `git`
- `curl` (for testing)

## Setup

In project repository run:

```bash
chmod +x setup.sh
./setup.sh
```

## Local testing

After you finish [Setup section](#setup), you can run directly FastAPI server using `uvicorn`:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Next you can run `\health` request:

```bash
curl -X GET http://localhost:8000/health \
  -H "Content-Type: application/json" \
```

You should see an appropriate response:

```bash
{"status":"ok"}
```
