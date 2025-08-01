import asyncio
import aiohttp
import re
import json
from collections import defaultdict
from datetime import datetime
import time
from urllib.parse import urlparse

# Complete categorized proxy sources (all URLs included)
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
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/main/proxies.txt",
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
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/http_proxies.txt",
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
        "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-KangProxy/https.txt",
        "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Tsprnay/https.txt",
        "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Zaeem20/https.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/https_proxies.txt",
        "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/https.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/master/https.txt"
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
        "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks4.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks4.txt",
        "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks4.txt",
        "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks4.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks4_proxies.txt",
        "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks4.txt",
        "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt"
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
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks5_proxies.txt",
        "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks5.txt",
        "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt"
    ],
    "mixed": [
        "https://api.getproxylist.com/proxy?anonymity[]=transparent&anonymity[]=anonymous&anonymity[]=elite",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
        "https://raw.githubusercontent.com/gitrecon1455/fresh-proxy-list/main/proxylist.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-working-checked.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/proxies.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/proxies.txt",
        "https://raw.githubusercontent.com/iplocate/free-proxy-list/refs/heads/main/all-proxies.txt",
        "https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/refs/heads/main/proxies.txt",
        "https://raw.githubusercontent.com/variableninja/proxyscraper/refs/heads/main/proxies/socks.txt",
        "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/refs/heads/main/proxies/all.txt",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/master/connect.txt"
    ]
}

OUTPUT_FILES = {
    "http": "http_proxies.txt",
    "https": "https_proxies.txt",
    "socks4": "socks4_proxies.txt",
    "socks5": "socks5_proxies.txt"
}

class FastProxyScraper:
    def __init__(self):
        self.proxy_sets = {
            "http": set(),
            "https": set(),
            "socks4": set(),
            "socks5": set()
        }
        self.session = None
    
    async def fetch_url(self, url):
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 200:
                    return await response.text()
        except:
            return None
    
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
            return re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', text)
        except:
            return []
    
    async def process_source(self, url, protocol):
        text = await self.fetch_url(url)
        if not text:
            return 0
        
        proxies = self.extract_proxies(text, url)
        if not proxies:
            return 0
        
        new_proxies = 0
        for proxy in proxies:
            if proxy not in self.proxy_sets[protocol]:
                self.proxy_sets[protocol].add(proxy)
                new_proxies += 1
        
        print(f"➕ Added {new_proxies} {protocol.upper()} proxies from {url}")
        return new_proxies
    
    async def process_mixed_source(self, url):
        text = await self.fetch_url(url)
        if not text:
            return 0
        
        proxies = self.extract_proxies(text, url)
        if not proxies:
            return 0
        
        new_proxies = 0
        for proxy in proxies:
            # Try adding to all protocol types
            for protocol in ["http", "socks4", "socks5"]:
                if proxy not in self.proxy_sets[protocol]:
                    self.proxy_sets[protocol].add(proxy)
                    new_proxies += 1
        
        print(f"➕ Added {new_proxies} mixed proxies from {url}")
        return new_proxies
    
    async def run(self):
        print(f"🚀 Starting fast proxy scraping at {datetime.now()}")
        total_sources = sum(len(urls) for urls in SOURCES.values())
        print(f"📚 Total sources: {total_sources}")
        
        connector = aiohttp.TCPConnector(limit=100, force_close=True)
        async with aiohttp.ClientSession(connector=connector) as self.session:
            # Process protocol-specific sources
            tasks = []
            for protocol, urls in SOURCES.items():
                if protocol == "mixed":
                    continue
                for url in urls:
                    tasks.append(self.process_source(url, protocol))
            
            # Process mixed sources
            for url in SOURCES["mixed"]:
                tasks.append(self.process_mixed_source(url))
            
            await asyncio.gather(*tasks)
        
        # Save results
        total_proxies = 0
        for protocol, proxies in self.proxy_sets.items():
            filename = OUTPUT_FILES[protocol]
            with open(filename, 'w') as f:
                f.write("\n".join(proxies))
            count = len(proxies)
            print(f"💾 Saved {count} {protocol.upper()} proxies to {filename}")
            total_proxies += count
        
        print(f"\n🎉 Completed! Found {total_proxies} total unique proxies")

async def main():
    scraper = FastProxyScraper()
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
