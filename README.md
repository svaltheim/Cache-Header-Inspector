# Cache-Header-Inspector
![Python](https://img.shields.io/badge/python-3.x-blue.svg) 

![License](https://img.shields.io/badge/license-MIT-green.svg)


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

<img width="2193" height="1823" alt="image" src="https://github.com/user-attachments/assets/52fbf59f-fd59-4510-9692-c849105971a7" />



****************************************************************************************************************************************************


<img width="1058" height="1043" alt="image" src="https://github.com/user-attachments/assets/3cff15a1-ad51-43eb-b674-26a8241644ff" />

*****************************************************************************************************************************************************

## Installation

> [!NOTE]
   > git clone [https://github.com/svaltheim/Cache-Header-Inspector.git](https://github.com/svaltheim/Cache-Header-Inspector.git)
   > cd Cache-Header-Inspector 














