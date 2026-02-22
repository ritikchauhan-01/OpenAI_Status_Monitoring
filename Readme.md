# OpenAI Status RSS Monitor

A lightweight asynchronous Python monitor that listens to the OpenAI Status RSS feed and prints real-time incident updates grouped by main product (API, ChatGPT, Sora).

## This project continuously polls:

`https://status.openai.com/history.rss`

It:

- Fetches new status updates
- Extracts affected sub-components
- Maps sub-components to main products (API, ChatGPT, Sora)
- Prints formatted, timezone-adjusted logs
- Avoids duplicate processing
- Uses ETag and Last-Modified headers for efficient polling

## 🚀 Features

✅ Async polling using aiohttp
✅ RSS parsing with feedparser
✅ HTML parsing via BeautifulSoup
✅ Automatic duplicate filtering
✅ Conditional requests using ETag / If-Modified-Since
✅ Sub-component → Main product mapping
✅ Timezone conversion (Asia/Kolkata)


## Architecture flow 

`
        RSS Feed
            ↓
        Fetch with ETag headers
            ↓
        Parse RSS entries
            ↓
        Extract <li> component from HTML description
            ↓
        Map sub-component → Main product
            ↓
        Print formatted output
`

## Dependencies

Install Require Packages
`pip install aiohttp feedparser python-dateutil beautifulsoup4`

## How To Run

`py main.py`

you can modify the polling interval in form "60" -> "30" second
` asyncio.run(monitor.monitor(interval=60))`

## customization
To change TimeZone Modiyy this line 
`tz.gettz("Asia/Kolkata")  ->   tz.gettz("UTC")`


## Console output 

`
[2026-02-22 18:12:00] Product: OpenAI API - Chat Completions
Status: Degraded performance

[2026-02-22 18:18:00] Product: OpenAI ChatGPT - Conversations
Status: Elevated error rates
`
