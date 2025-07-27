# Auto Proxy Scraper

This repository automatically collects and verifies proxies from various sources every hour.

## Files Generated
- `http_proxies.txt` - Working HTTP proxies
- `https_proxies.txt` - Working HTTPS proxies  
- `socks4_proxies.txt` - Working SOCKS4 proxies
- `socks5_proxies.txt` - Working SOCKS5 proxies

## How It Works
1. Runs automatically every hour via GitHub Actions
2. Fetches proxies from multiple sources
3. Verifies each proxy by testing connection to Google
4. Saves working proxies in categorized files

## Manual Trigger
Go to Actions → "Auto Proxy Scraper" → "Run workflow"
