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


<img width="1944" height="1276" alt="image" src="https://github.com/user-attachments/assets/76d71fce-f185-4fd7-aac8-bb43ac2cc6c7" />



<img width="2560" height="1665" alt="image" src="https://github.com/user-attachments/assets/95d11107-753a-49a5-9acd-655c0d3a46ec" />




