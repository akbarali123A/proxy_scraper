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
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http
https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt
https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/http.txt
https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/http.txt
https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/http.txt
https://raw.githubusercontent.com/shiftytr/proxy-list/master/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/proxylist-to/update-list/main/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt
https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http_proxies.txt
https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/http.txt
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
https://raw.githubusercontent.com/sunny9577/proxy-scraper/main/proxies.txt
https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/proxies.txt
https://raw.githubusercontent.com/Anonymaron/free-proxy/main/http.txt
https://raw.githubusercontent.com/HyperBeast/proxy-list/main/http.txt
https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt
https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/http.txt
https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/http.txt
https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/http.txt
https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt
https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/http.txt
https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt
https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/http_proxies.txt
https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/http.txt
https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/master/http.txt
http://multiproxy.org/txt_all/proxy.txt
http://promicom.by/tools/proxy/proxy.txt
http://www.socks24.org/feeds/posts/default
http://globalproxies.blogspot.de/feeds/posts/default
http://www.caretofun.net/free-proxies-and-socks/",
        # Add all other HTTP-specific sources
    ],
    "https": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https
https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/https.txt
https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/https
https://raw.githubusercontent.com/shiftytr/proxy-list/master/https.txt
https://raw.githubusercontent.com/proxylist-to/update-list/main/https.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt
https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-KangProxy/https.txt
https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Tsprnay/https.txt
https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Zaeem20/https.txt
https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/https_proxies.txt
https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/https.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/master/https.txt",
        # Add all other HTTPS-specific sources
    ],
    "socks4": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4
https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt
https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks4.txt
https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks4.txt
https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks4.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt
https://raw.githubusercontent.com/proxylist-to/update-list/main/socks4.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt
https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4_proxies.txt
https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks4.txt
https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks4.txt
https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt
https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks4.txt
https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks4.txt
https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks4.txt
https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks4.txt
https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks4.txt
https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks4.txt
https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks4_proxies.txt
https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks4.txt
https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt",
        # Add all other SOCKS4-specific sources
    ],
    "socks5": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5
https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt
https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks5.txt
https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
https://raw.githubusercontent.com/hookzof/socks5_list/refs/heads/master/proxy.txt
https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt
https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks5.txt
https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks5.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt
https://raw.githubusercontent.com/proxylist-to/update-list/main/socks5.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt
https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5_proxies.txt
https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks5.txt
https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks5.txt
https://raw.githubusercontent.com/HyperBeast/proxy-list/main/socks5.txt
https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt
https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks5.txt
https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt
https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks5.txt
https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks5.txt
https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt
https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks5.txt
https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt
https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks5_proxies.txt
https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks5.txt
https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt",
        # Add all other SOCKS5-specific sources
    ],
    "mixed": [
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        https://api.getproxylist.com/proxy?anonymity[]=transparent&anonymity[]=anonymous&anonymity[]=elite
https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc
https://raw.githubusercontent.com/gitrecon1455/fresh-proxy-list/main/proxylist.txt
https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-working-checked.txt
https://raw.githubusercontent.com/zevtyardt/proxy-list/main/proxies.txt
https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/proxies.txt
https://raw.githubusercontent.com/iplocate/free-proxy-list/refs/heads/main/all-proxies.txt
https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/refs/heads/main/proxies.txt
https://raw.githubusercontent.com/variableninja/proxyscraper/refs/heads/main/proxies/socks.txt
https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/refs/heads/main/proxies/all.txt
https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/master/connect.txt
    ],
    "api": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http,socks4,socks5",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1",
        # Add all other API sources
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
CONCURRENT_CHECKS = 200
MAX_RETRIES = 2

def determine_proxy_type_from_url(url):
    """Determine proxy type from URL pattern"""
    parsed = urlparse(url.lower())
    path = parsed.path
    
    if 'http' in path and 'https' not in path:
        return 'http'
    elif 'https' in path:
        return 'https'
    elif 'socks4' in path:
        return 'socks4'
    elif 'socks5' in path:
        return 'socks5'
    return None

async def fetch_url(session, url):
    for attempt in range(MAX_RETRIES + 1):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            if attempt == MAX_RETRIES:
                print(f"❌ Failed to fetch {url} after {MAX_RETRIES} attempts")
                return None
            await asyncio.sleep(1)

def extract_proxies(text, url, source_type):
    """Extract proxies based on source type"""
    try:
        if source_type == "api":
            if "api.proxyscrape.com" in url:
                return text.splitlines(), None  # None means protocol not specified
            elif "geonode.com" in url:
                data = json.loads(text)
                return [f"{item['ip']}:{item['port']}" for item in data['data']], None
        
        # For mixed format files
        if source_type == "mixed":
            # Try to extract protocol from line if available (proxy:port:type)
            proxies = []
            for line in text.splitlines():
                parts = line.split(':')
                if len(parts) >= 2:
                    if len(parts) >= 3:  # Format: ip:port:type
                        ip, port, ptype = parts[0], parts[1], parts[2].lower()
                        if ptype in ['http', 'https', 'socks4', 'socks5']:
                            proxies.append((f"{ip}:{port}", ptype))
                    else:  # Format: ip:port
                        proxies.append((f"{parts[0]}:{parts[1]}", None))
            return proxies
        
        # For simple IP:PORT format
        proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', text)
        return [(p, None) for p in proxies] if proxies else []
    
    except Exception as e:
        print(f"⚠️ Error parsing {url}: {str(e)}")
        return []

async def check_proxy(session, proxy, proxy_type):
    """Check if proxy is working"""
    try:
        test_url = TEST_URL
        proxy_url = f"{proxy_type}://{proxy}" if proxy_type else f"http://{proxy}"
        
        async with session.get(
            test_url,
            proxy=proxy_url,
            timeout=aiohttp.ClientTimeout(total=TIMEOUT),
            headers={'User-Agent': 'Mozilla/5.0'}
        ) as response:
            return response.status == 200
    except:
        return False

async def process_source(session, url, results):
    """Process each source URL"""
    source_type = (
        "api" if "api." in url else
        "mixed" if any(x in url.lower() for x in ["proxies.txt", "proxy-list", "all.txt"]) else
        determine_proxy_type_from_url(url) or "mixed"
    )
    
    text = await fetch_url(session, url)
    if not text:
        return
    
    extracted = extract_proxies(text, url, source_type)
    if not extracted:
        return
    
    print(f"🔍 Found {len(extracted)} proxies from {url}")
    
    # Process proxies in batches
    batch_size = CONCURRENT_CHECKS
    valid_proxies = defaultdict(set)
    
    for i in range(0, len(extracted), batch_size):
        batch = extracted[i:i + batch_size]
        
        # Determine proxy types for this batch
        check_tasks = []
        for proxy, ptype in batch:
            actual_type = ptype or determine_proxy_type_from_url(url) or "http"
            check_tasks.append((proxy, actual_type, check_proxy(session, proxy, actual_type)))
        
        # Run checks concurrently
        checked = await asyncio.gather(*[task[2] for task in check_tasks])
        
        # Collect results
        for (proxy, ptype, _), is_valid in zip(check_tasks, checked):
            if is_valid:
                valid_proxies[ptype].add(proxy)
    
    # Update final results
    for ptype, proxies in valid_proxies.items():
        if proxies:
            results[ptype].update(proxies)
            print(f"✅ Valid {len(proxies)} {ptype.upper()} proxies from {url}")

async def main():
    start_time = time.time()
    results = defaultdict(set)
    
    print(f"🚀 Starting proxy scraping at {datetime.now()}")
    print(f"📚 Total sources: {sum(len(v) for v in SOURCES.values())}")
    
    connector = aiohttp.TCPConnector(limit=CONCURRENT_CHECKS, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Process all sources by category
        tasks = []
        for category, urls in SOURCES.items():
            for url in urls:
                tasks.append(process_source(session, url, results))
        
        await asyncio.gather(*tasks)
    
    # Save results
    total_proxies = 0
    for proxy_type in OUTPUT_FILES:
        filename = OUTPUT_FILES[proxy_type]
        with open(filename, 'w') as f:
            f.write("\n".join(results[proxy_type]))
        count = len(results[proxy_type])
        print(f"💾 Saved {count} {proxy_type.upper()} proxies to {filename}")
        total_proxies += count
    
    elapsed = time.time() - start_time
    print(f"\n🎉 Completed! Found {total_proxies} working proxies in {elapsed:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import aiohttp
import re
from datetime import datetime
from collections import defaultdict

SOURCES = [
    
  "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http,socks4,socks5&timeout=10000&country=all&anonymity=all",
  "https://api.getproxylist.com/proxy?anonymity[]=transparent&anonymity[]=anonymous&anonymity[]=elite",
  "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/http.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/https.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks4.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks5.txt",
  "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
  "https://raw.githubusercontent.com/hookzof/socks5_list/refs/heads/master/proxy.txt",
  "https://raw.githubusercontent.com/gitrecon1455/fresh-proxy-list/main/proxylist.txt",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/http.txt",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/https",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/http.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks4.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks5.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/http.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/https.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks4.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks5.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/http.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/https.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/socks4.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/socks5.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http_proxies.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4_proxies.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5_proxies.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/http.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE-PROXY-LIST/master/proxy_list.txt",
  "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
  "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-working-checked.txt",
  "https://raw.githubusercontent.com/sunny9577/proxy-scraper/main/proxies.txt",
  "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/proxies.txt",
  "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/proxies.txt",
  "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/proxies.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/http.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks4.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks5.txt",
  "https://raw.githubusercontent.com/HyperBeast/proxy-list/main/http.txt",
  "https://raw.githubusercontent.com/HyperBeast/proxy-list/main/socks5.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/http.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks4.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks5.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
  "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/http.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/https.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks4.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks5.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/http.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/proxylist.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/https.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks4.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/http.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks4.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks5.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-KangProxy/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Tsprnay/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Zaeem20/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-hendrikbgr/proxy_list.txt",
  "https://raw.githubusercontent.com/iplocate/free-proxy-list/refs/heads/main/all-proxies.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks4.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt",
  "https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/refs/heads/main/proxies.txt",
  "https://raw.githubusercontent.com/variableninja/proxyscraper/refs/heads/main/proxies/http.txt",
  "https://raw.githubusercontent.com/variableninja/proxyscraper/refs/heads/main/proxies/socks.txt",
  "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/refs/heads/main/proxies/all.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/http_proxies.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/https_proxies.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks4_proxies.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks5_proxies.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/http.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/https.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/proxies.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
  "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/connect.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/http.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/https.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt",
  "http://multiproxy.org/txt_all/proxy.txt",
  "http://promicom.by/tools/proxy/proxy.txt",
  "http://www.socks24.org/feeds/posts/default",
  "http://globalproxies.blogspot.de/feeds/posts/default",
  "http://www.caretofun.net/free-proxies-and-socks/"
];

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
