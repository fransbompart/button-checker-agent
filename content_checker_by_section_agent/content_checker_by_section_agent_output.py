from pydantic import BaseModel
from typing import List

class PageContentPreview(BaseModel): 
    content_preview_title: str
    content_preview_categories: str
    content_preview_type: str
    public_access: bool
    content_preview_duration: str | None

class PageContentPreviews(BaseModel):
    previews: List[PageContentPreview]
    
class PageContent(BaseModel): 
    dialog_opened: bool
    page_opened: bool
    page_description: str | None
    page_url: str | None

class PagesContents(BaseModel): 
    pages: List[PageContent]

class PageContentMatch(BaseModel):
    content_title: str
    match_preview: bool
    differences: str | None
    
class PagesContentsMatches(BaseModel):
    contents: List[PageContent]



