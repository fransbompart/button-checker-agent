EVALUATE_CONTENT_TASK = """Click on the post item with title "content_preview_title" using the custom function click_post_item, the number of the post is previewNumber.
Then:
- If you are in the post page:
  - **Extract** the whole page.
  - Indicate if it is a blog or an audio/video, and provide a clear description of it. If certain details are unavailable, the response should still include as much relevant information as possible. For example:
    - This is a blog post. The topic appears to be about renewable energy, but the author and publication date are not available. The content discusses the benefits of solar power and wind energy.
    - This is a video file. The title and creator are not specified, but the video appears to be a tutorial on graphic design basics. The duration is not provided neither. 
- Else, if a dialog with message "¡Prueba Gratis 5 días!" appers, say it and end the task successfully.
---
**Important:**
- First, if a dialog about Calendario Lunar appears, close it on the x before continue.
- If you don't see the post item, DON'T SCROLL, use directly the function click_post_item.
"""

