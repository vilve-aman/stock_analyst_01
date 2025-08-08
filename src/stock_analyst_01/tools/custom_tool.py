from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."



from src.stock_analyst_01.tools.search import SearchScreaner
from src.stock_analyst_01.tools.stock_details import GetStockDetailsFromScreaner
from src.stock_analyst_01.tools.news import NewsScraper

class SearchScreanerInput(BaseModel):
    query: str = Field(..., description="The Possible stock symbol, company name, industry synonymns, stock symbol or any other keyword to search for on screener.in")


class SearchScreanerTool(BaseTool):
    name: str = "SearchScreanerTool"
    description: str = "Search for a stock on screener.in, it will return a list of stocks(id, name, symbol, url[for getting more details]) that match the query"
    args_schema: Type[BaseModel] = SearchScreanerInput

    def _run(self, query: str) -> str:
        return SearchScreaner.search_facade(query)



# from tools.stock_details import GetStockDetailsFromScreaner

class GetStockDetailsFromScreanerInput(BaseModel):
    """
    input example: {'id': 3370, 'name': 'Tata Motors Ltd', 'symbol': 'TATAMOTORS', 'url': 'https://www.screener.in/company/TATAMOTORS/consolidated/'}
    """
    symbol: str = Field(..., description="The stock symbol to get details for")
    url: str = Field(..., description="The url of the stock to get details for")


class GetStockDetailsFromScreanerTool(BaseTool):
    name: str = "GetStockDetailsFromScreanerTool"
    description: str = "Get Comprehensive financial details for a stock from screener.in including Profit and Loss, Balance Sheet, Cash Flow, Ratios, Investors, etc."
    args_schema: Type[BaseModel] = GetStockDetailsFromScreanerInput

    def _run(self, symbol: str, url: str) -> str:
        all_data = GetStockDetailsFromScreaner.search(**{"symbol": symbol, "url": url})
        return {
            "About": all_data["base_info"]["About"],
            "Stats": all_data["base_info"]["Stats"],
            "Analysis": all_data["base_info"]["Analysis"],
            "ProfitAndLoss": {
                key: dict(zip(all_data["base_info"]["ProfitAndLoss"]["headers"], value))
                for key, value in all_data["base_info"]["ProfitAndLoss"]["rows"].items()
            },
            "BalanceSheet": {
                key: dict(zip(all_data["base_info"]["BalanceSheet"]["headers"], value))
                for key, value in all_data["base_info"]["BalanceSheet"]["rows"].items()
            },
            "CashFlow": {
                key: dict(zip(all_data["base_info"]["CashFlow"]["headers"], value))
                for key, value in all_data["base_info"]["CashFlow"]["rows"].items()
            },
            "Ratios": {
                key: dict(zip(all_data["base_info"]["Ratios"]["headers"], value))
                for key, value in all_data["base_info"]["Ratios"]["rows"].items()
            },
            "Investors": {
                key: dict(zip(all_data["base_info"]["Investors"]["headers"], value))
                for key, value in all_data["base_info"]["Investors"]["rows"].items()
            }

        }


class GetPeersDataFromScreanerTool(BaseTool):
    name: str = "GetPeersDataFromScreanerTool"
    description: str = "Get peers data for a stock from screener.in, it will return a list of peers and the median of the peers"
    args_schema: Type[BaseModel] = GetStockDetailsFromScreanerInput

    def _run(self, symbol: str, url: str) -> str:
        all_data = GetStockDetailsFromScreaner.search(**{"symbol": symbol, "url": url})
        
        return {
            "Peers": all_data["peers_data"]["rows"],
            "Median": all_data["peers_data"]["median"]
        }



class GetNewsDataFromScreanerInput(BaseModel):
    company_name: str = Field(..., description="The company name, industry synonymns, stock symbol or any other keyword to get news for")

class GetNewsDataFromScreanerTool(BaseTool):
    name: str = "GetNewsDataFromScreanerTool"
    description: str = "Get news data for a stock from screener.in"
    args_schema: Type[BaseModel] = GetNewsDataFromScreanerInput

    def _run(self, company_name: str) -> str:
        return NewsScraper.search_news(company_name)



if __name__ == "__main__":
    tool = SearchScreanerTool()
    res = tool.run(input=SearchScreanerInput(query="Tata"))
    print("res", res)

    stock_chossen = res[-1]
    print("stock_chossen", stock_chossen)
    t = GetStockDetailsFromScreanerTool()
    res = t.run(input=GetStockDetailsFromScreanerInput(**stock_chossen))
    print("res", res)


    t = GetPeersDataFromScreanerTool()
    res = t.run(input=GetStockDetailsFromScreanerInput(**stock_chossen))
    print("res", res)