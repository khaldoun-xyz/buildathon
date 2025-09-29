## Cologne AI Buildathon — Oct 18

This is a simple Streamlit app for presenting and collecting RSVPs for the Cologne AI Buildathon, inspired by the Menlo Park buildathon.

- Event: October 18, 2025 — Cologne, Germany
- RSVP submissions are saved to `data/rsvps.csv`

### Getting started

1. Create a virtual environment (recommended)
2. Install dependencies
3. Run the app

```bash
python -m venv ~/virtualenvs/[name_of_venv]
source ~/virtualenvs/[name_of_venv]/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Configuration

- Theme can be adjusted in `.streamlit/config.toml`
- Registration limit is set via `REGISTRATION_LIMIT` in `streamlit_app.py`

### Notes

- RSVP CSV file is created automatically on first submission.
- To clear RSVPs, delete `data/rsvps.csv`.

### Docker

Build and run locally:

```bash
docker build -t cologne-buildathon .
docker run --rm -p 8080:8080 cologne-buildathon
```

Visit http://localhost:8080

### DigitalOcean App Platform

- Select “Container” and point to this repo; it will autodetect `Dockerfile`.
- Ensure HTTP port is set to `8080` (App Platform injects `$PORT`, which the image respects).
- No custom start command needed. Health checks will pass once Streamlit is up.

