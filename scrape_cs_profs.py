import json
import os
import re
from bs4 import BeautifulSoup
# from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import (
    JsonCssExtractionStrategy,
    LLMExtractionStrategy,
)

import asyncio

async def simple_crawl(url):
    print("\n--- Basic Usage ---")  
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        return result

from pandas import *

async def extract_scholar_data(u):
    schema = {
        "name" : "Scholar",
        "baseSelector" : "tr.gsc_a_tr",
        "fields": [
            
        ],
    }
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url=u,
                extraction_strategy=extraction_strategy,
                bypass_cache=True,
            )

            assert result.success, "Failed to crawl the page"
    
            news_teasers = json.loads(result.extracted_content)
    print(result.extracted_content)
    return result

async def extract_paper_data(u):
    schema = {
        "name" : "gsc_oci_title_link",
        "baseSelector": "gsc_oci_table",
        "fields": [
            {
                "name": "authors",
                "selector": "div.gsc_oci_value",
                "type": "text",
            },
            {
                "name": "date",
                "selector": "div.gsc_oci_value",
                "type": "text",
            },
            {
                "name": "book",
                "selector": "div.gsc_oci_value",
                "type": "text",
            },
            {
                "name": "pages",
                "selector": "div.gsc_oci_value",
                "type": "text",
            },
            {
                "name": "description",
                "selector": "div.gsc_oci_value",
                "type": "text",
            },
        ],
    }
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url=u,
                extraction_strategy=extraction_strategy,
                bypass_cache=True,
            )
            assert result.success, "Failed to crawl the page"
    
            news_teasers = json.loads(result.extracted_content)
    print(result.extracted_content)
    return result
     

async def main():
    data = read_csv("umbc_profs.csv")
    scholarids = data['scholarid'].tolist()
    id = scholarids[1]
    url = "https://scholar.google.com.ua/citations?hl=en&user=" + id + "&view_op=list_works&sortby=pubdate"
    result = await extract_scholar_data(url)
    with open("ex.txt",'w') as file:
        print(result.url)
        file.write(result.cleaned_html)
asyncio.run(main())




