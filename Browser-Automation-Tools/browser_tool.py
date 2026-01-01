"""
Browser Automation Tool - Python Playwright

This script provides browser automation capabilities that can be 
called from the command line or imported as a module.

Usage:
    python browser_tool.py search "query"
    python browser_tool.py screenshot "url" "output.png"
    python browser_tool.py get_text "url"
    python browser_tool.py fill_form "url" "selector" "value"

Requirements:
    pip install playwright
    playwright install chromium
"""

import sys
import asyncio
import json
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright")
    sys.exit(1)


async def search_google(query: str) -> dict:
    """Search Google and return top results"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(f"https://www.google.com/search?q={query}")
        await page.wait_for_load_state("networkidle")
        
        # Extract search results
        results = await page.evaluate("""
            () => {
                const items = document.querySelectorAll('div.g');
                return Array.from(items).slice(0, 5).map(item => {
                    const title = item.querySelector('h3')?.textContent || '';
                    const link = item.querySelector('a')?.href || '';
                    const snippet = item.querySelector('.VwiC3b')?.textContent || '';
                    return { title, link, snippet };
                });
            }
        """)
        
        await browser.close()
        
        return {
            "query": query,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }


async def take_screenshot(url: str, output_path: str) -> dict:
    """Take a screenshot of a webpage"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        await page.screenshot(path=output_path, full_page=True)
        
        await browser.close()
        
        return {
            "url": url,
            "screenshot": output_path,
            "timestamp": datetime.now().isoformat()
        }


async def get_page_text(url: str) -> dict:
    """Get all text content from a webpage"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        # Get page title and main text
        title = await page.title()
        text = await page.evaluate("() => document.body.innerText")
        
        await browser.close()
        
        return {
            "url": url,
            "title": title,
            "text": text[:5000],  # Limit to 5000 chars
            "timestamp": datetime.now().isoformat()
        }


async def get_page_html(url: str) -> dict:
    """Get HTML content from a webpage"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        html = await page.content()
        
        await browser.close()
        
        return {
            "url": url,
            "html": html[:10000],  # Limit size
            "timestamp": datetime.now().isoformat()
        }


async def click_and_extract(url: str, click_selector: str, extract_selector: str) -> dict:
    """Click an element and extract text from another"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        # Click element
        await page.click(click_selector)
        await page.wait_for_load_state("networkidle")
        
        # Extract text
        text = await page.locator(extract_selector).text_content()
        
        await browser.close()
        
        return {
            "url": url,
            "clicked": click_selector,
            "extracted": text,
            "timestamp": datetime.now().isoformat()
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python browser_tool.py <command> [args...]")
        print("Commands: search, screenshot, get_text, get_html")
        return
    
    command = sys.argv[1]
    
    if command == "search" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        result = asyncio.run(search_google(query))
        print(json.dumps(result, indent=2))
        
    elif command == "screenshot" and len(sys.argv) >= 4:
        url = sys.argv[2]
        output = sys.argv[3]
        result = asyncio.run(take_screenshot(url, output))
        print(json.dumps(result, indent=2))
        
    elif command == "get_text" and len(sys.argv) >= 3:
        url = sys.argv[2]
        result = asyncio.run(get_page_text(url))
        print(json.dumps(result, indent=2))
        
    elif command == "get_html" and len(sys.argv) >= 3:
        url = sys.argv[2]
        result = asyncio.run(get_page_html(url))
        print(json.dumps(result, indent=2))
        
    else:
        print(f"Unknown command or missing arguments: {command}")
        print("Commands: search, screenshot, get_text, get_html")


if __name__ == "__main__":
    main()
