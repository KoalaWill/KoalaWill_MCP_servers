from mcp.server.fastmcp import FastMCP
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE2_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

print(f"[INIT].... → GOOGLE_API_KEY available: {GOOGLE_API_KEY is not None}")
print(f"[INIT].... → OPENAI_API_KEY available: {OPENAI_API_KEY is not None and OPENAI_API_KEY != ''}")
print(f"[INIT].... → MISTRAL_API_KEY available: {MISTRAL_API_KEY is not None and MISTRAL_API_KEY != ''}")

mcp = FastMCP("webcrawl")
mcp.settings.port = 8002

@mcp.tool()
async def scrape_url(url: str) -> str:
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown.raw_markdown if result.markdown else "No content found"
    except Exception as e:
        return f"Error scraping URL: {str(e)}"

@mcp.tool()
async def extract_text_by_query(url: str, query: str, context_size: int = 300) -> str:
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            if not result.markdown or not result.markdown.raw_markdown:
                return f"No text content found for URL: {url}"

            full_text = result.markdown.raw_markdown
            query = query.lower()
            matches = []
            positions = []
            lower_text = full_text.lower()
            current_pos = 0

            while True:
                pos = lower_text.find(query, current_pos)
                if pos == -1:
                    break
                positions.append(pos)
                current_pos = pos + len(query)

            for pos in positions:
                start = max(0, pos - context_size)
                end = min(len(full_text), pos + len(query) + context_size)
                context = full_text[start:end]
                matches.append(context)

            if matches:
                matches = matches[:5]
                result_text = "\n\n---\n\n".join([f"Match {i+1}:\n{match}" for i, match in enumerate(matches)])
                return f"Found {len(matches)} matches for '{query}' on the page. Here are the relevant sections:\n\n{result_text}"

            return f"No matches found for '{query}' on the page."
    except Exception as e:
        return f"Error searching page: {str(e)}"

@mcp.tool()
async def smart_extract(url: str, instruction: str) -> str:
    try:
        if OPENAI_API_KEY:
            print(f"[EXTRACT] Using OpenAI API directly")

            extraction_strategy = LLMExtractionStrategy(
                llm_config=LLMConfig(
                    provider="openai/gpt-3.5-turbo",  # You can change this to gpt-4 if needed
                    api_token=OPENAI_API_KEY
                ),
                extraction_type="natural",
                instruction=instruction,
                extra_args={"temperature": 0.2}
            )

            config = CrawlerRunConfig(
                extraction_strategy=extraction_strategy
            )

            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url, config=config)

                if result.extracted_content:
                    content = result.extracted_content
                    try:
                        parsed = json.loads(content)
                        content = json.dumps(parsed, indent=2)
                    except:
                        pass

                    return f"Successfully extracted information based on your instruction:\n\n{content}"
                else:
                    return f"No relevant information found for your instruction: '{instruction}'"
        else:
            return "Error: OpenAI API key not found. Please set OPENAI_API_KEY in your environment."
    except Exception as e:
        return f"Error during intelligent extraction: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse")
