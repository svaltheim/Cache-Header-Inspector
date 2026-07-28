# Cache-Header-Inspector
A lightweight Python tool designed for Bug Bounty hunters to identify cacheable endpoints by inspecting HTTP response headers.

The tool performs a warm-up request followed by a second probe request to detect cache HIT/MISS conditions across multiple CDN providers.

Supports:

• Cloudflare
• Akamai
• Fastly
• Incapsula
• Varnish

Features

✔ Automatic CDN fingerprinting
✔ Cache HIT detection
✔ Batch processing
✔ HTTP header collection
✔ Redirect detection
✔ Summary statistics
✔ No external dependencies


**Usage: python cacheheader_inspector.py <domains_file> [output_file]**


Examples

<img width="1929" height="1156" alt="image" src="https://github.com/user-attachments/assets/68e47538-25b0-42d9-b9ff-0a7d52a7f16d" />

