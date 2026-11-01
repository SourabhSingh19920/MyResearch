from pydantic import BaseModel,Field

class Planner(BaseModel):
    title : str = Field(title="Title of the research", default="Trending Topic",description="Takes the topic of interest to research.")
    required_search : bool = Field(title="Required Search",default=False, description="Will Decide whether the following topic requires an browser search or not.")
    search_term : str = Field(title = "Research Topic",default="",description="Research Topic in case if any search is required")
    required_scientific_search : bool = Field(title="Scientific Search",default=False, description="Will Decide whether the following topic requires an Scientific  search or not.")
    scientific_search_term : str = Field(title = "Scientific Search Topic",default="",description="Scientific Search Topic in case if any search is required")
