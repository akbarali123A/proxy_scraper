
import asyncio
import aiohttp
import re
from datetime import datetime
from collections import defaultdict

SOURCES = [
    # HTTP proxies
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    
    # HTTPS proxies
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    
    # SOCKS4 proxies
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    
    # SOCKS5 proxies
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    
    # Add all your other sources here...
]

async def fetch_proxies(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                text = await response.text()
                return re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', text)
    except:
        return []

async def check_proxy(session, proxy, proxy_type):
    try:
        async with session.get(
            "http://www.google.com",
            proxy=f"{proxy_type}://{proxy}",
            timeout=5
        ) as response:
            return response.status == 200
    except:
        return False

async def main():
    all_proxies = defaultdict(set)
    
    async with aiohttp.ClientSession() as session:
        # Fetch all proxies
        tasks = [fetch_proxies(session, url) for url in SOURCES]
        results = await asyncio.gather(*tasks)
        
        # Check proxies
        for url, proxies in zip(SOURCES, results):
            if proxies:
                proxy_type = "http" if "http" in url.lower() else \
                            "socks4" if "socks4" in url.lower() else \
                            "socks5" if "socks5" in url.lower() else "https"
                
                print(f"Checking {len(proxies)} {proxy_type} proxies from {url}")
                
                check_tasks = [check_proxy(session, proxy, proxy_type) for proxy in proxies]
                checked = await asyncio.gather(*check_tasks)
                
                for proxy, is_valid in zip(proxies, checked):
                    if is_valid:
                        all_proxies[proxy_type].add(proxy)
    
    # Save results
    for proxy_type, proxies in all_proxies.items():
        with open(f"{proxy_type}_proxies.txt", "w") as f:
            f.write("\n".join(proxies))
        print(f"Saved {len(proxies)} working {proxy_type} proxies")

if __name__ == "__main__":
    asyncio.run(main())
