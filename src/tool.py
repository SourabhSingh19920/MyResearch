from langchain_community.tools import DuckDuckGoSearchResults

class SearchTool:
    def __init__(self):
        self.duckduckgosearch = DuckDuckGoSearchResults(max_results=5,output_format="list")

    def duckduckgoSearch(self,query : str):
        return self.duckduckgosearch.invoke(query)