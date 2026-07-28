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


```Usage: python cacheheader_inspector.py <domains_file> [output_file]```



**Example**

<img width="2237" height="1825" alt="image" src="https://github.com/user-attachments/assets/1f97d5eb-4a7b-4dd2-8031-32fbcb3eced6" />

****************************************************************************************************************************************************


<img width="1058" height="1043" alt="image" src="https://github.com/user-attachments/assets/3cff15a1-ad51-43eb-b674-26a8241644ff" />














