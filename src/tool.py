from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os
import time

class SearchTool:
    def __init__(self):
        self.duckduckgosearch = DuckDuckGoSearchResults(max_results=5,output_format="list")
        self.wikipediaWrapper = WikipediaAPIWrapper(
                top_k_results=1, 
                doc_content_chars_max=500
            )
        self.wiki_tool = WikipediaQueryRun(api_wrapper=self.wikipediaWrapper)

    def duckduckgoSearch(self,query : str):
        return self.duckduckgosearch.invoke(query)

    def wikipediaSearch(self,query : str):
        try:
            retry = 3
            while retry > 0:
                try:
                    result = self.wiki_tool.run(query)
                    
                    return {
                        "page" : result.split("Summary")[0].replace("Page: ",""),
                        "summary" : result.split("Summary")[1].replace(":","").strip()
                    }
                except Exception as e:
                    retry -= 1
                    time.sleep(2)
            return None
        except Exception as e:
                return None


if __name__ == "__main__":
    st = SearchTool()
    result = st.wikipediaSearch("AWS Lambda")
    print(type(result))
    print(result)