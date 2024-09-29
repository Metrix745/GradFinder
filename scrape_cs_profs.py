import json
import os
from bs4 import BeautifulSoup
# from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import (
    JsonCssExtractionStrategy,
    LLMExtractionStrategy,
)
from pandas import *
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
    prof = {}
    data = read_csv("umbc_profs.csv")
    scholarids = data['scholarid'].tolist()
    id = scholarids[1]
    # url = "https://scholar.google.com.ua/citations?hl=en&user=" + id + "&view_op=list_works&sortby=pubdate"
    url = input("Enter the url: ")

    # result = await extract_scholar_data(url)
    mode = input("Enter the mode (1 for scholar data, 2 for paper data): ")
    if mode == "1":
        result = await simple_crawl(url)
    else:
        result = await extract_paper_data(url)
    
    with open("ex.txt",'w') as file:
        soup = BeautifulSoup(result.html, 'html.parser')
        prof['name'] = soup.title.string 
        file.write(soup.prettify())


    goodlinks = [];    
    for link in result.links['internal']:
        if id in link["href"] and link['text'] not in ['View all', 'Sort by citations', 'Sort by year', 'Sort by title']:
            goodlinks.append(link['href'])
    
    for link in goodlinks:
        print("https://scholar.google.com/"+link)
    
asyncio.run(main())