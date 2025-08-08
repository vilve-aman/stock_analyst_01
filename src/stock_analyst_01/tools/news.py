"""
Search Tool For Agent
"""

import requests
import json
import re
import unicodedata

from bs4 import BeautifulSoup

class NewsScraper:


    def __init__(self):
        pass

    @classmethod
    def search_headlines(cls, query: str) -> str:


        url = f"https://economictimes.indiatimes.com/json_newssearch.cms?query={query}"

        payload = {}
        headers = {
        'Cookie': 'geoinfo=CC:IN, RC:HR, CT:GURGAON, CO:AS, GL:1'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        return response.text

    
    @classmethod
    def search_summary(cls, query: str) -> str:


        url = f"https://economictimes.indiatimes.com{query}"

        payload = {}
        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Cookie': '_grx_et=172246129140177122231879567; geoinfo=CC:IN, RC:HR, CT:GURGAON, CO:AS, GL:1; deviceid=ca3tfkv4wnz4cfpmhpl7perkl; lgc_deviceid=ca3tfkv4wnz4cfpmhpl7perkl; _iibeat_session=6ad46ed4-d0d6-4cff-99de-584bf9819d4d; _iibeat_vt=20250628; _hookShow=1; popout_autorefresh_open=true; rw_default=true; JSESSIONID=0A717CE43672226EFB8D16DE6B1D8DF6;'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        return response.text
    


    @classmethod
    def summary_parser(cls, html_content: str) -> list:
        
        text_parser = lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8')

        soup = BeautifulSoup(html_content, 'html.parser')
        data = {}

        # --- Extract Summary ID ---
        summary = soup.find('p', class_='summary')
        if not summary:
            summary = soup.find('h2', class_='artSyn').find('p')
        summary = text_parser(summary.text) if summary else ""
    
        return summary
 

    @classmethod
    def search_news(cls, query: str) -> list:

        headlines = NewsScraper.search_headlines(query=query)
        headlines = json.loads(headlines)

        for headline in headlines:
            details_html = NewsScraper.search_summary(headline['link'])
            summary = NewsScraper.summary_parser(details_html)
            headline['summary'] = summary

        return headlines

    


if __name__ == "__main__":
    # headlines = NewsScraper.search_headlines("au small finance bank")
    # headlines = json.loads(headlines)

    # for headline in headlines:
    #     details_html = NewsScraper.search_summary(headline['link'])
    #     summary = NewsScraper.summary_parser(details_html)
    #     headline['summary'] = summary

    news = NewsScraper.search_news("Axis Bank")

    print(json.dumps(news, indent=4))
    # print(news)