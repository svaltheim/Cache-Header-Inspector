#!/usr/bin/env python3
"""
HTTP Headers Inspector - Batch mode with cache HIT detection
Usage: python http_inspector.py <domains_file> [output_file]

  domains_file : text file containing one domain or URL per line
  output_file   : optional, default "headers_result.txt"

Workflow:
  - Request 1 (warm-up): warms the cache and is discarded
  - Request 2 (probe): headers are collected and HIT/MISS is detected

Supported CDNs: Incapsula, Akamai, Fastly, Cloudflare, Varnish
"""

import sys
import time
import urllib.request
import urllib.error
from datetime import datetime


# ── CDN fingerprints ────────────────────────────────────
CDN_FINGERPRINTS = {
    "Incapsula":  ["x-iinfo", "x-cdn"],
    "Akamai":     ["x-check-cacheable", "akamai-cache-status", "x-akamai-cache-status"],
    "Fastly":     ["x-cache-hits", "fastly-debug-digest", "x-served-by"],
    "Cloudflare": ["cf-cache-status", "cf-ray"],
    "Varnish":    ["x-varnish", "x-varnish-cache"],
}

# ── Cache HIT detection rules ───────────────────────────────────────────────
# NOTE: x-iinfo (Incapsula) is used ONLY to identify the CDN, no para
# detect HIT. It is always present regardless of cache status,
# which would generate false positives.
CACHE_HIT_RULES = {
    # Generic
    "x-cache":               lambda v: "hit" in v.lower(),
    "x-cache-status":        lambda v: "hit" in v.lower(),

    # Akamai
    "x-check-cacheable":     lambda v: v.strip().lower() == "yes",
    "akamai-cache-status":   lambda v: "hit" in v.lower(),
    "x-akamai-cache-status": lambda v: "hit" in v.lower(),

    # Fastly  →  X-Cache-Hits es un contador (puede ser "1" o "1, 0" multi-nodo)
    "x-cache-hits":          lambda v: any(
                                 int(n.strip()) > 0
                                 for n in v.split(",")
                                 if n.strip().isdigit()
                             ),

    # Cloudflare
    "cf-cache-status":       lambda v: v.strip().lower() == "hit",

    # Varnish
    "x-varnish-cache":       lambda v: "hit" in v.lower(),
}

CACHE_AGE_HEADER = "age"   # Age > 0 también indica HIT


def detect_cdn(headers: dict) -> str:
    """Attempts to identify the CDN/proxy from the response headers."""
    lower_h = {k.lower() for k in headers}
    found = [cdn for cdn, fps in CDN_FINGERPRINTS.items() if any(fp in lower_h for fp in fps)]
    return ", ".join(found) if found else "Desconocido"


def detect_cache_status(headers: dict) -> tuple[bool, str]:
    """
    Returns (is_hit, details) by analyzing cache headers.
    Supports Incapsula, Akamai, Fastly, Cloudflare y Varnish.
    """
    lower_headers = {k.lower(): v for k, v in headers.items()}

    for header, check in CACHE_HIT_RULES.items():
        value = lower_headers.get(header, "")
        if value:
            try:
                if check(value):
                    return True, f"{header}: {value}"
            except Exception:
                pass

    # Fallback: Age > 0
    age = lower_headers.get(CACHE_AGE_HEADER, "0")
    try:
        if int(age) > 0:
            return True, f"age: {age}s"
    except ValueError:
        pass

    return False, "MISS / not cached"


def fetch(url: str) -> tuple[dict, int, str, str]:
    """Performs an HTTP request and returns (headers, status, reason, final_url)."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent":    "Mozilla/5.0 (HTTP-Inspector/1.0)",
            "Cache-Control": "no-cache",
            "Pragma":        "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return dict(resp.headers), resp.status, resp.reason, resp.url


def probe_url(url: str) -> tuple[str, bool]:
    """
    Performs two requests to the URL:
      1ª warm-up  → warms the cache (discarded)
      2ª probe    → analyzes HIT/MISS and stores the headers
    Returns (output_text, is_hit).
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    lines = []
    is_hit = False

    lines.append(f"{'='*62}")
    lines.append(f"  URL  : {url}")
    lines.append(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"{'='*62}")

    try:
        # Warm-up request
        fetch(url)
        time.sleep(0.5)

        # Probe request
        headers, status, reason, final_url = fetch(url)

        cdn = detect_cdn(headers)
        is_hit, cache_detail = detect_cache_status(headers)
        cache_label = "HIT" if is_hit else "MISS"

        lines.append(f"\n  Status      : {status} {reason}")
        lines.append(f"  CDN/Proxy   : {cdn}")
        lines.append(f"  Cache       : {cache_label}  ({cache_detail})")
        if final_url != url:
            lines.append(f"  Redirected to: {final_url}")

        lines.append(f"\n{'─'*62}")
        lines.append(f"  {'HEADER':<40} VALUE")
        lines.append(f"{'─'*62}")
        for key, value in sorted(headers.items()):
            lines.append(f"  {key:<40} {value}")

    except urllib.error.HTTPError as e:
        lines.append(f"\n  Status : {e.code} {e.reason}")
        if e.headers:
            hdrs = dict(e.headers)
            cdn = detect_cdn(hdrs)
            is_hit, cache_detail = detect_cache_status(hdrs)
            cache_label = "HIT" if is_hit else "MISS"
            lines.append(f"  CDN/Proxy: {cdn}")
            lines.append(f"  Cache    : {cache_label}  ({cache_detail})")
            lines.append(f"\n{'─'*62}")
            lines.append(f"  {'HEADER':<40} VALUE")
            lines.append(f"{'─'*62}")
            for key, value in sorted(hdrs.items()):
                lines.append(f"  {key:<40} {value}")

    except urllib.error.URLError as e:
        lines.append(f"\n  Connection error: {e.reason}")

    except Exception as e:
        lines.append(f"\n  Unexpected error: {e}")

    lines.append(f"{'='*62}")
    return "\n".join(lines), is_hit


def process_file(input_file: str, output_file: str) -> None:
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            domains = [
                line.strip()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        sys.exit(1)

    if not domains:
        print("The input file is empty or contains no valid domains.")
        sys.exit(1)

    total  = len(domains)
    hits   = 0
    misses = 0

    print(f"Processing {total} domain(s) [2 requests per URL]...")
    print(f"Supported CDNs: Incapsula, Akamai, Fastly, Cloudflare, Varnish")
    print(f"Saving results to: {output_file}\n")

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("HTTP Headers Inspector - Detection de cache HIT\n")
        out.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"Domains : {total}\n")
        out.write(f"CDNs     : Incapsula, Akamai, Fastly, Cloudflare, Varnish\n")
        out.write(f"{'#'*62}\n")

        for i, domain in enumerate(domains, 1):
            print(f"  [{i}/{total}] {domain} ... ", end="", flush=True)

            block, is_hit = probe_url(domain)

            if is_hit:
                hits += 1
                print("HIT")
                out.write("\n\n")
                out.write(block)
                out.write("\n")
            else:
                misses += 1
                print("")  # clean line break without printing "MISS"

    # Summary
    summary = (
        f"\n\n{'#'*62}\n"
        f"SUMMARY\n"
        f"  Total processed : {total}\n"
        f"  HIT  (cacheable) : {hits}\n"
        f"  MISS (not cached) : {misses}\n"
        f"{'#'*62}\n"
    )
    with open(output_file, "a", encoding="utf-8") as out:
        out.write(summary)

    print(f"\n{'─'*42}")
    print(f"  Total: {total}  |  HIT: {hits}  |  MISS: {misses}")
    print(f"Results saved to '{output_file}'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "headers_result.txt"

    process_file(input_file, output_file)
