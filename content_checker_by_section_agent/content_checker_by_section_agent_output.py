from pydantic import BaseModel
from typing import List

class PageContentPreview(BaseModel): 
    content_preview_title: str
    content_preview_type: str
    content_preview_category: str
    content_preview_access_type: str
    content_url: str

class PageContentPreviews(BaseModel):
    previews: List[PageContentPreview]

class PageContentMatch(BaseModel):
    content_title: str
    match_preview: bool
    differences: str | None
    
class PagesContentsMatches(BaseModel):
    contents: List[PageContentMatch]



