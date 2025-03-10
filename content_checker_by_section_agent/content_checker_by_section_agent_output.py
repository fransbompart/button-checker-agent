from pydantic import BaseModel
from typing import List

class PageContentPreview(BaseModel): 
    content_preview_title: str
    content_preview_categories: str
    content_page_url: str
    content_preview_type: str
    public_access: bool
    content_preview_duration: str | None
    content_preview_index: int

class PageContentPreviews(BaseModel):
    previews: List[PageContentPreview]

class PageContentMatch(BaseModel):
    content_title: str
    match_preview: bool
    differences: str | None
    
class PagesContentsMatches(BaseModel):
    contents: List[PageContentMatch]



