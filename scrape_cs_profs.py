import json
import os
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
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


async def main():
    prof = {}
    data = read_csv("umbc_profs.csv")
    scholarids = data['scholarid'].tolist()
    id = scholarids[1]
    url = "https://scholar.google.com.ua/citations?hl=en&user=" + id + "&view_op=list_works&sortby=pubdate"
    result = await simple_crawl(url)
    with open("resultlinks.json",'w') as file:
        json.dump(result.links,file,indent=4)
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