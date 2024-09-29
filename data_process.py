import csv
import json
import os
import asyncio

from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import (
    JsonCssExtractionStrategy,
    LLMExtractionStrategy,
)
import pandas as pd

CSV_DEST = 'umbc_profs.csv'

async def simple_crawl(url):
    print("\n--- Basic Usage ---")  
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        return result.links
    
async def extract_paper_data(url):
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
                url=url,
                extraction_strategy=extraction_strategy,
                bypass_cache=True,
            )
            assert result.success, "Failed to crawl the page"
    
            news_teasers = json.loads(result.extracted_content)
    print(result.extracted_content)
    return result

def load_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def extract_scholar_id(data):
    return [row[-1] for row in data if row[-1] != 'NOSCHOLARPAGE'][1:]

async def read_scholar_page(scholar_id):
    url = f'https://scholar.google.com/citations?user={scholar_id}&view_op=list_works&sortby=pubdate'
    links = await simple_crawl(url)
    
    filtered_links = filter_links(links, scholar_id)

    return filtered_links

def filter_links(links, scholar_id):
    flattened_links = []
    for pair in links['internal']:
        if scholar_id in list(pair.values())[0]:
            if pair['text'] not in ['View all', 'Sort by citations', 'Sort by year', 'Sort by title']:
                flattened_links.append(list(pair.values())[0])
    return flattened_links

async def process_link(link):
    url = f"https://scholar.google.com{link}"
    info = await extract_paper_data(url)
    

    soup = BeautifulSoup(info.html, 'html.parser')

    extracted_data = [div.get_text() for div in soup.find_all('div', class_='gsc_oci_value')]

    return extracted_data

async def main():
    raw_csv = load_csv(CSV_DEST)
    scholar_ids = extract_scholar_id(raw_csv)
    # adam = await read_scholar_page(scholar_ids[0])
    # # print(adam)
    # extracted_paper = await process_link(adam[0])
    # print(extracted_paper)
    
    dictionary = {}

    for scholar_id in scholar_ids:
        dictionary[scholar_id] = {
            'authors': [],
            'date': [],
            'book': [],
            'pages': [],
            'description': []
        }
        links = await read_scholar_page(scholar_id)
        for link in links:
            extracted_data = await process_link(link)
            dictionary[scholar_id]['authors'].append(extracted_data[0])
            dictionary[scholar_id]['date'].append(extracted_data[1])
            dictionary[scholar_id]['book'].append(extracted_data[2])
            dictionary[scholar_id]['pages'].append(extracted_data[3])
            dictionary[scholar_id]['description'].append(extracted_data[4])



    

asyncio.run(main())
