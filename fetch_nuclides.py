#!/usr/bin/env python3
"""
Download IAEA Livechart ground-state data with the required User-Agent header.
Saves the result to ground_states.csv in the same directory.
"""
import urllib.request, urllib.error, pathlib, sys, ssl

# macOS often lacks system CA certs for Python; create an unverified context
# as a fallback (data is public/read-only, no credentials involved).
_ssl_ctx = ssl.create_default_context()
try:
    urllib.request.urlopen("https://nds.iaea.org", context=_ssl_ctx, timeout=5)
except Exception:
    _ssl_ctx = ssl._create_unverified_context()

URL = "https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=all"
OUT = pathlib.Path(__file__).parent / "ground_states.csv"

req = urllib.request.Request(URL)
req.add_header(
    "User-Agent",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
)

print("Fetching ground states from IAEA Livechart…", flush=True)
try:
    with urllib.request.urlopen(req, context=_ssl_ctx) as resp:
        data = resp.read()
    OUT.write_bytes(data)
    rows = data.count(b"\n")
    print(f"✓ Saved {rows} rows → {OUT}")
except Exception as e:
    print(f"✗ Error: {e}", file=sys.stderr)
    sys.exit(1)
