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
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/http.txt",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/http.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/http.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/http.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http_proxies.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/http.txt",
  "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
  "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/proxies.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/http.txt",
  "https://raw.githubusercontent.com/HyperBeast/proxy-list/main/http.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/http.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/http.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/http.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/http.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/http.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/http.txt",
  "http://multiproxy.org/txt_all/proxy.txt",
  "http://promicom.by/tools/proxy/proxy.txt",
  "http://www.socks24.org/feeds/posts/default",
  "http://globalproxies.blogspot.de/feeds/posts/default",
  "http://www.caretofun.net/free-proxies-and-socks/"
     ],
    "https": [
   "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/https.txt",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/https",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/https.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/https.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
  "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-working-checked.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-KangProxy/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Tsprnay/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Zaeem20/https.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/https.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/https_proxies.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/https.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/https_proxies.txt"
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/https.txt"
        # ... all other HTTPS sources ...
    ],
    "socks4": [
  "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks4.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks4.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks4.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/socks4.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4_proxies.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks4.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks4.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks4.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks4.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks4.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks4.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks4.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks4_proxies.txt"
  # ... all other SOCKS4 sources ...
    ],
    "socks5": [
  "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks5.txt",
  "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
  "https://raw.githubusercontent.com/hookzof/socks5_list/refs/heads/master/proxy.txt",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks5.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks5.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/socks5.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5_proxies.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks5.txt",
  "https://raw.githubusercontent.com/HyperBeast/proxy-list/main/socks5.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks5.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks5.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks5.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks5.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks5_proxies.txt"
  # ... all other SOCKS5 sources ...
    ],
    "mixed": [
  "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http,socks4,socks5",
  "https://api.getproxylist.com/proxy?anonymity[]=transparent&anonymity[]=anonymous&anonymity[]=elite",
  "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
  "https://raw.githubusercontent.com/gitrecon1455/fresh-proxy-list/main/proxylist.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt",
  "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE-PROXY-LIST/master/proxy_list.txt",
  "https://raw.githubusercontent.com/sunny9577/proxy-scraper/main/proxies.txt",
  "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/proxies.txt",
  "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/proxies.txt",
  "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
  "https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/refs/heads/main/proxies.txt",
  "https://raw.githubusercontent.com/variableninja/proxyscraper/refs/heads/main/proxies/socks.txt",
  "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/refs/heads/main/proxies/all.txt",
  "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/connect.txt",
  "https://raw.githubusercontent.com/iplocate/free-proxy-list/refs/heads/main/all-proxies.txt",
  "https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/proxies.txt"
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
