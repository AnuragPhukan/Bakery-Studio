# Bakery Quotation Agent

FastAPI app that gathers job details, calculates the BOM in-process, prices materials from SQLite, applies markup/VAT, and generates a ready-to-send quote.

## Prerequisites

- Python 3
- `python-multipart` (installed via `requirements.txt`) for FastAPI form handling in the UI

## Run (UI)

```bash
python3 -m uvicorn ui:app --reload --port 8080
```

Open `http://localhost:8080`.

The quote is saved to `out/quote_<id>.md`.
The app also generates `out/quote_<id>.txt` and `out/quote_<id>.pdf`.

## Chat UI (Mistral)

Provide your Mistral API key in `.env`:

```
MISTRAL_API_KEY=your_mistral_key
MISTRAL_BASE_URL=https://codestral.mistral.ai/v1
MISTRAL_MODEL=mistral-large-latest
```

Then run:

```bash
python3 -m uvicorn ui:app --reload --port 8080
```

Open `http://localhost:8080/chat`.

## Configuration

Defaults are baked in, but you can override with environment variables (in `.env` or inline):

- `MATERIALS_DB_PATH` (default `assets/materials.sqlite`)
- `TEMPLATE_PATH` (default `assets/quote_template.md`)
- `OUTPUT_DIR` (default `out`)
- `LABOR_RATE` (default `15.00`)
- `MARKUP_PCT` (default `30` or `0.30`)
- `VAT_PCT` (default `20` or `0.20`)
- `CURRENCY` (default `GBP`)
- `QUOTE_VALID_DAYS` (default `14`)
- `FX_RATES_JSON` (optional JSON mapping like `{"GBP":1,"USD":1.27,"EUR":1.17}`)
- `WORLD_TIME_API_URL` (optional, defaults to London time via WorldTimeAPI)
- `SENDER_NAME` (optional, used for email sign-off; default `Bakery Nation`)

Example:

```bash
LABOR_RATE=18 MARKUP_PCT=35 VAT_PCT=20 python3 -m uvicorn ui:app --reload --port 8080
```

## Temp API keys (for reviewers)

I have created temporary API keys for reviewers and will share them separately.  
Please add them to your local `.env` (do not commit them), and remove/revoke them after review.

## Email delivery (optional)

If you want the UI to email the quote to the customer, use Resend (recommended on Render) or SMTP.

### Resend (recommended)

Set env vars:

- `RESEND_API_KEY` (required)
- `RESEND_FROM` (required, verified sender like `Bakery Nation <no-reply@yourdomain.com>`)

Example:

```bash
RESEND_API_KEY=your_resend_key RESEND_FROM="Bakery Nation <no-reply@yourdomain.com>" python3 -m uvicorn ui:app --reload --port 8080
```

### SMTP

Set SMTP env vars:

- `SMTP_HOST` (required)
- `SMTP_PORT` (default `587`)
- `SMTP_USER`
- `SMTP_PASS`
- `SMTP_FROM` (defaults to `SMTP_USER`)
- `SMTP_TLS` (default `true`)
- `SMTP_SSL` (default `false`)

Example:

```bash
SMTP_HOST=smtp.gmail.com SMTP_PORT=587 SMTP_USER=you@gmail.com SMTP_PASS=app_password SMTP_FROM=you@gmail.com python3 -m uvicorn ui:app --reload --port 8080
```

### Using a .env file

You can place SMTP and config values in a `.env` file in the project root:

```
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=you@yahoo.com
SMTP_PASS=app_password
SMTP_FROM=you@yahoo.com
```

Then just run:

```bash
python3 -m uvicorn ui:app --reload --port 8080
```

## Google Sheets logging (optional)

Log each quote to a Google Sheet using a Service Account.

1) Create a Service Account and download the JSON key.  
2) Share your Google Sheet with the service account email (Editor).  
3) Set env vars:

```
SHEET_ID=your_sheet_id
SHEET_TAB=Sheet1
SHEETS_CREDENTIALS_PATH=/path/to/service_account.json
```

Restart the UI server and each confirmed quote will append a row.

## How to add materials or job types

- Materials: insert new rows into `materials` in `assets/materials.sqlite`.
- Job types: update `BOM_PER_UNIT` in `bom.py`.

## Notes / Limitations

- Template rendering is minimal and supports the current `quote_template.md` placeholders.
- Live FX depends on external APIs and may fail without network access; set `FX_RATES_JSON` for offline runs.
- Google Sheets logging and email sending require external credentials and will be skipped if not configured.
- Render blocks outbound SMTP; use Resend there.
