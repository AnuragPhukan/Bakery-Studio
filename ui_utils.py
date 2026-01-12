import hashlib
import hmac
import html
import os


ADMIN_COOKIE_NAME = "bakery_admin"


def admin_token(secret):
    # Build a signed token for admin auth.
    return hmac.new(secret.encode("utf-8"), b"admin", hashlib.sha256).hexdigest()


def admin_cookie_valid(request):
    # Validate the admin cookie against the configured secret.
    secret = os.environ.get("ADMIN_PASSWORD", "").strip()
    if not secret:
        return False
    token = request.cookies.get(ADMIN_COOKIE_NAME, "")
    return hmac.compare_digest(token, admin_token(secret))


def page_template(title, body, show_header=True, body_class=""):
    # Wrap page content in the shared HTML shell.
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
      <link rel="stylesheet" href="/styles.css" />
</head>
<body class="{body_class}">
  {"<header><h1>Bakery Quotation Studio</h1><p>Turn a quick conversation into a polished quote, fast.</p></header>" if show_header else ""}
  <div class="wrap">
    <div class="card">
      {body}
    </div>
  </div>
</body>
</html>"""
