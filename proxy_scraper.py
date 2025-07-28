import asyncio
import aiohttp
import re
import json
from collections import defaultdict
from datetime import datetime
import time
from urllib.parse import urlparse

# Categorized proxy sources
SOURCES = {
    "http": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        # ... all other HTTP sources ...
        "http://www.caretofun.net/free-proxies-and-socks/"
    ],
    "https": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https",
        "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/https.txt",
        # ... all other HTTPS sources ...
    ],
    "socks4": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
        # ... all other SOCKS4 sources ...
    ],
    "socks5": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        # ... all other SOCKS5 sources ...
    ],
    "mixed": [
        "https://api.getproxylist.com/proxy?anonymity[]=transparent&anonymity[]=anonymous&anonymity[]=elite",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
        # ... all other mixed sources ...
        "https://raw.githubusercontent.com/zloi-user/hideip.me/master/connect.txt"
    ]
}

OUTPUT_FILES = {
    "http": "http_proxies.txt",
    "https": "https_proxies.txt",
    "socks4": "socks4_proxies.txt",
    "socks5": "socks5_proxies.txt"
}

TEST_URL = "http://www.google.com"
TIMEOUT = 10
CONCURRENT_CHECKS = 250
MAX_RETRIES = 2
BATCH_SIZE = 100

class ProxyScraper:
    def __init__(self):
        self.checked_proxies = set()
        self.results = defaultdict(set)
        self.session = None
        self.start_time = time.time()
    
    async def fetch_url(self, url):
        for attempt in range(MAX_RETRIES + 1):
            try:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        return await response.text()
            except Exception as e:
                if attempt == MAX_RETRIES:
                    print(f"❌ Failed to fetch {url} after {MAX_RETRIES} attempts")
                    return None
                await asyncio.sleep(1)
    
    def extract_proxies(self, text, url):
        try:
            # Handle JSON APIs
            if "api.proxyscrape.com" in url:
                return text.splitlines()
            elif "geonode.com" in url:
                data = json.loads(text)
                return [f"{item['ip']}:{item['port']}" for item in data['data']]
            elif "getproxylist.com" in url:
                data = json.loads(text)
                return [f"{data['ip']}:{data['port']}"]
            
            # Default pattern for IP:PORT
            return list(set(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', text)))
        except Exception as e:
            print(f"⚠️ Error parsing {url}: {str(e)}")
            return []
    
    async def check_proxy(self, proxy, proxy_type):
        if proxy in self.checked_proxies:
            return False
            
        try:
            proxy_url = f"{proxy_type}://{proxy}"
            async with aiohttp.ClientSession() as test_session:
                try:
                    async with test_session.get(
                        TEST_URL,
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=TIMEOUT),
                        headers={'User-Agent': 'Mozilla/5.0'}
                    ) as response:
                        if response.status == 200:
                            self.checked_proxies.add(proxy)
                            return True
                except:
                    return False
        except:
            return False
    
    async def process_source(self, url, protocol):
        text = await self.fetch_url(url)
        if not text:
            return
        
        proxies = self.extract_proxies(text, url)
        if not proxies:
            return
        
        print(f"🔍 Found {len(proxies)} proxies from {url}")
        
        valid_proxies = set()
        
        for i in range(0, len(proxies), BATCH_SIZE):
            batch = proxies[i:i + BATCH_SIZE]
            tasks = [self.check_proxy(proxy, protocol) for proxy in batch]
            checked = await asyncio.gather(*tasks)
            
            for proxy, is_valid in zip(batch, checked):
                if is_valid:
                    valid_proxies.add(proxy)
        
        if valid_proxies:
            self.results[protocol].update(valid_proxies)
            print(f"✅ Valid {len(valid_proxies)}/{len(proxies)} {protocol.upper()} proxies from {url}")
    
    async def process_mixed_source(self, url):
        text = await self.fetch_url(url)
        if not text:
            return
        
        proxies = self.extract_proxies(text, url)
        if not proxies:
            return
        
        print(f"🔍 Found {len(proxies)} mixed proxies from {url}")
        
        # Check each proxy with all protocol types
        for protocol in ['http', 'socks4', 'socks5']:
            valid_proxies = set()
            
            for i in range(0, len(proxies), BATCH_SIZE):
                batch = proxies[i:i + BATCH_SIZE]
                tasks = [self.check_proxy(proxy, protocol) for proxy in batch]
                checked = await asyncio.gather(*tasks)
                
                for proxy, is_valid in zip(batch, checked):
                    if is_valid:
                        valid_proxies.add(proxy)
            
            if valid_proxies:
                self.results[protocol].update(valid_proxies)
                print(f"✅ Valid {len(valid_proxies)} {protocol.upper()} proxies from mixed source {url}")
    
    async def run(self):
        print(f"🚀 Starting proxy scraping at {datetime.now()}")
        print(f"📚 Total sources: {sum(len(v) for v in SOURCES.values())}")
        
        connector = aiohttp.TCPConnector(limit=CONCURRENT_CHECKS, force_close=True)
        async with aiohttp.ClientSession(connector=connector) as self.session:
            # Process protocol-specific sources
            for protocol, urls in SOURCES.items():
                if protocol == "mixed":
                    continue
                
                tasks = [self.process_source(url, protocol) for url in urls]
                await asyncio.gather(*tasks)
            
            # Process mixed sources
            tasks = [self.process_mixed_source(url) for url in SOURCES['mixed']]
            await asyncio.gather(*tasks)
        
        # Save results
        total_proxies = 0
        for protocol, proxies in self.results.items():
            filename = OUTPUT_FILES[protocol]
            with open(filename, 'w') as f:
                f.write("\n".join(proxies))
            print(f"💾 Saved {len(proxies)} {protocol.upper()} proxies to {filename}")
            total_proxies += len(proxies)
        
        elapsed = time.time() - self.start_time
        print(f"\n🎉 Completed! Found {total_proxies} working proxies in {elapsed:.2f} seconds")

async def main():
    scraper = ProxyScraper()
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
