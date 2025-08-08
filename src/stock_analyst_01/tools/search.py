"""
Search Tool For Agent
"""

import requests
import json
import re



class SearchScreaner:


    def __init__(self):
        pass

    @classmethod
    def search(cls, query: str) -> str:


        url = f"https://www.screener.in/api/company/search/?q={query}&v=3&fts=1"

        payload = {}
        headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.7',
        'priority': 'u=1, i',
        'referer': 'https://www.screener.in/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Cookie': 'csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print("search response from screener", response.text)
        return response.text

    @classmethod
    def parse_search_response(cls, response: str) -> list:

        data = json.loads(response)

        parsed_data = []
        for item in data:

            if item["id"]:
                # symbol = re.search(r'company\/(.*)\/', item["url"])
                symbol = re.search(r'company\/([^\/]+)\/', item["url"])
                symbol = symbol.group(1) if symbol else None

                
                parsed_data.append({
                    "id": item["id"],
                    "name": item["name"],
                    "symbol": symbol,
                    "url": f'https://www.screener.in{item["url"]}'
                })

        return parsed_data


    @classmethod
    def search_facade(cls, query: str) -> list:
        response = cls.search(query)
        parsed_data = cls.parse_search_response(response)
        # print("parsed_data", parsed_data)
        return parsed_data




    


if __name__ == "__main__":
    response = SearchScreaner.search("au small finance bank")
    print(SearchScreaner.parse_search_response(response))