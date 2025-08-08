"""
Search Tool For Agent
"""

import requests
import json
import re

from bs4 import BeautifulSoup




class GetStockDetailsFromScreaner:


    def __init__(self):
        pass

    
    @classmethod
    def base_info(cls, stock_symbol: str) -> str:
        """
        Get the base information of the stock from the screener
        """
        import requests

        url = f"https://www.screener.in/company/{stock_symbol}/consolidated/"

        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en;q=0.7',
            'priority': 'u=0, i',
            'referer': 'https://www.screener.in/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Cookie': 'csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn; csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        return response.text

    @classmethod
    def base_info_v2(cls, url: str) -> str:
        """
        Get the base information of the stock from the screener
        """
        """
        Get the base information of the stock from the screener
        """
        import requests

        url = f"https://www.screener.in{url}"
        print("hitting_url", url)
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en;q=0.7',
            'priority': 'u=0, i',
            'referer': 'https://www.screener.in/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Cookie': 'csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn; csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        return response.text


    @classmethod
    def base_info_v3(cls, url: str) -> str:
        """
        Get the base information of the stock from the screener
        """
        """
        Get the base information of the stock from the screener
        """
        import requests

    
        print("hitting_url", url)
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en;q=0.7',
            'priority': 'u=0, i',
            'referer': 'https://www.screener.in/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Cookie': 'csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn; csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        return response.text


    @classmethod
    def parse_base_info(cls, html_content: str) -> dict:
        """
        Parse the base information of the stock from the screener
        """

        text_parser = lambda x: x.encode('latin1').decode('unicode_escape').replace("\\u00a0", " ")
        parse_inr = lambda x: x.replace("\u20b9", "INR ")

        soup = BeautifulSoup(html_content, 'html.parser')
        data = {}

        # --- Extract warehouse ID ---
        company_info = soup.find('div', id='company-info')
        if company_info and company_info.has_attr('data-warehouse-id'):
            data['warehouse_id'] = company_info['data-warehouse-id']



        # Extract About section
        about_section = soup.select_one(".about").get_text(separator=" ", strip=True)

        # Extract Key Points - Products and Brands
        more_about_company = soup.select_one(".always-show-more-box").get_text(separator=" ", strip=True).strip()


        # Extract Stats
        stats = {}
        stats_list = soup.select("#top-ratios li")
        for item in stats_list:
            key = item.select_one("span.name").get_text(strip=True)
            value = item.select_one("span.value").get_text(strip=True)
            stats[key] = parse_inr(value)

        data["About"]= f"{about_section} {more_about_company}"
        data["Stats"]= stats

        # --- Chart Section ---
        chart = soup.find('section', id='chart')
        if chart:
            days = [text_parser(btn.text.strip()) for btn in chart.select('#company-chart-days button')]
            metrics = [text_parser(btn.text.strip()) for btn in chart.select('#company-chart-metrics button') if 'More' not in btn.text]
            data['Chart'] = {
                "availableRanges": days,
                "metrics": metrics
            }

        # --- Analysis Section ---
        analysis = soup.find('section', id='analysis')
        if analysis:
            pros = [text_parser(li.text.strip()) for li in analysis.select('.pros ul li')]
            cons = [text_parser(li.text.strip()) for li in analysis.select('.cons ul li')]
            data['Analysis'] = {
                "Pros": pros,
                "Cons": cons
            }

        # --- Peers Section ---
        peers = soup.find('section', id='peers')
        if peers:
            benchmarks = [text_parser(a.text.strip()) for a in peers.select('#benchmarks a.tag')]
            data['Peers'] = {
                "Benchmarks": benchmarks
            }

        # --- Quarterly Results Section ---
        def parse_table(section_id):
            section = soup.find('section', id=section_id)
            if not section:
                return {}
            table = section.find('table')
            headers = [text_parser(th.text.strip()) for th in table.select('thead th')][1:]  # Skip first column
            rows = {}
            for tr in table.select('tbody tr'):
                label = tr.select_one('td.text')
                if not label:
                    continue
                label_text = text_parser(label.text.strip())
                values = [text_parser(td.text.strip()) for td in tr.select('td')[1:]]
                rows[label_text] = values
            return {"headers": headers, "rows": rows}

        data['Quarters'] = parse_table('quarters')
        data['ProfitAndLoss'] = parse_table('profit-loss')
        data['BalanceSheet'] = parse_table('balance-sheet')
        data['CashFlow'] = parse_table('cash-flow')
        data['Ratios'] = parse_table('ratios')
        data['Investors'] = parse_table('shareholding')
        # data['Documents'] = parse_table('documents')

        return data


    @classmethod
    def get_peers_info(cls, stock_id: str) -> str:
        """
        Parse the peers information of the stock from the screener
        """

        url = f"https://www.screener.in/api/company/{stock_id}/peers/"

        payload = {}
        headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.7',
        'priority': 'u=1, i',
        'referer': 'https://www.screener.in/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'Cookie': 'csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn; csrftoken=YK8kPeypE376xpi1FUQuEPlpgSTly8hn'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)
        return response.text



    @classmethod
    def parse_get_peers_info(cls, html_content: str) -> dict:
        """
        Parse the peers information of the stock from the screener
        """

        text_parser = lambda x: x.encode('latin1').decode('unicode_escape').replace("\\u00a0", " ")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.select_one("div[data-page-results] table")
        if not table:
            return {}

        rows = table.select("tbody tr")
        if not rows:
            return {}

        # Extract headers from the first row (using <th>)
        header_cells = rows[0].find_all("th")
        headers = [text_parser(cell.get_text(strip=True)) for cell in header_cells]

        data_rows = []
        for row in rows[1:]:
            cells = row.find_all("td")
            if not cells:
                continue
            row_data = {}
            for i in range(min(len(headers), len(cells))):
                row_data[headers[i]] = text_parser(cells[i].get_text(strip=True))
            data_rows.append(row_data)

        # Extract median row from tfoot
        median_row = {}
        tfoot = table.find("tfoot")
        if tfoot:
            median_cells = tfoot.find_all("td")
            for i in range(min(len(headers), len(median_cells))):
                median_row[headers[i]] = text_parser(median_cells[i].get_text(strip=True))

        return {
            "headers": headers,
            "rows": data_rows,
            "median": median_row
        }



    @classmethod
    def search(cls, **kwargs) -> dict:


        # response = GetStockDetailsFromScreaner.base_info(kwargs["stock_symbol"])
        print("kwargs", kwargs)
        response = GetStockDetailsFromScreaner.base_info_v3(kwargs["url"])
        base_info = GetStockDetailsFromScreaner.parse_base_info(response)
        response = GetStockDetailsFromScreaner.get_peers_info(base_info["warehouse_id"])
        peers_data = GetStockDetailsFromScreaner.parse_get_peers_info(response)
        # print(peers_data)
        return {
            "base_info": base_info,
            "peers_data": peers_data
        }



    


if __name__ == "__main__":


    # response = GetStockDetailsFromScreaner.base_info("AUBANK")
    # base_info = GetStockDetailsFromScreaner.parse_base_info(response)
    # response = GetStockDetailsFromScreaner.get_peers_info(base_info["warehouse_id"])
    # peers_data = GetStockDetailsFromScreaner.parse_get_peers_info(response)
    data = GetStockDetailsFromScreaner.search(**{"url": "https://www.screener.in/company/AUBANK/"})
    json.dump(data, open("data.json", "w"), indent=4)
    # print(data)