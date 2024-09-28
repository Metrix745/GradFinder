import json
import os
import re
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
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
        return result;

umbc_faculty_lists = {
    "AFST": ["https://africanastudies.umbc.edu/affilliates/"],
    "AGNG": ["https://lifesciences.umaryland.edu/about/graduate-program-faculty/"],
    "AMST": ["https://amst.umbc.edu/faculty-and-staff/"],
    "ANCS": ["https://ancientstudies.umbc.edu/faculty/"],
    "ANTH": ["https://asianstudies.umbc.edu/faculty/"],
    "ART" : ["https://art.umbc.edu/visual-arts-at-umbc/faculty-staff/"],
    "BIOL": ["https://biology.umbc.edu/directory/faculty/"],
    "CHEM": ["https://chemistry.umbc.edu/faculty/"],
    "CMPE": ["https://www.csee.umbc.edu/tenure-track-faculty/","https://www.csee.umbc.edu/research-affiliate-additional-faculty/"],
    "DANC": ["https://dance.umbc.edu/faculty/"],
    "EDUC": ["https://education.umbc.edu/faculty-list/"],
    "EHS" : ["https://edhs.umbc.edu/faculty/"],
    "ENCH": ["https://cbee.umbc.edu/faculty/"],
    "ENGL": ["https://english.umbc.edu/core-faculty/"],
    "ENME": ["https://me.umbc.edu/directory/"],
    "GES" : ["https://ges.umbc.edu/faculty-pages/"],
    "GLBL": ["https://globalstudies.umbc.edu/home/faculty-and-staff/"],
    "GWST": ["https://gwst.umbc.edu/faculty/"],
    "HIST": ["https://history.umbc.edu/facultystaff/full-time/"],
    "IS"  : ["https://informationsystems.umbc.edu/home/faculty-and-staff/faculty/"],
    "JDST": ["https://judaicstudies.umbc.edu/home/faculty-4/"],
    "LRC" : ["https://llc.umbc.edu/people/language-literacy-and-culture-doctoral-program-faculty/"],
    "MATH": ["https://mathstat.umbc.edu/faculty/"],
    "MBIO": ["https://marinebiotechnology.umbc.edu/faculty/"],
    "MCS" : ["https://mcs.umbc.edu/mcs-faculty-and-staff/"],
    "MLL" : ["https://mlli.umbc.edu/faculty/"],
    "MUSC": ["https://music.umbc.edu/directory/"],
    "PHIL": ["https://philosophy.umbc.edu/facultystaff/"],
    "PHYS": ["https://physics.umbc.edu/people/faculty/"],
    "POLI": ["https://politicalscience.umbc.edu/faculty-1/"],
    "PSYC": ["https://psychology.umbc.edu/corefaculty/"],
    "PUB" : ["https://publicpolicy.umbc.edu/faculty/"],
    "SOCY": ["https://saph.umbc.edu/ftfaculty/","https://saph.umbc.edu/researchers/"],
    "SOWK": ["https://socialwork.umbc.edu/sowk-faculty-and-staff/faculty/"],
    "THTR": ["https://theatre.umbc.edu/about-us/faculty/"]
}


results = {}
async def main():
    
    result = await simple_crawl(umbc_faculty_lists["ENME"][0])
    print(result.markdown)
    with open("ENMEfac.json",'w') as file:
        json.dump(result.links,file)

    
    #for key in umbc_faculty_lists.keys():
    #    for url in umbc_faculty_lists[key]:
    #        result = await simple_crawl(url)
    #        print(result.links)

asyncio.run(main())