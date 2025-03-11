EVALUATE_CONTENT_TASK = """Click on the post item with title "content_preview_title" using the custom function click_post_item, the number of the post is previewNumber.
Then:
- If you are in the post page, **extract** and describe the whole page, include the page url on your response.
- Else, if a dialog with message "¡Prueba Gratis 5 días!" appers, say it and end the task successfully.
---
**Important:**
- First, if a dialog about Calendario Lunar appears, close it on the x before continue.
- If you don't see the post item, DON'T SCROLL, use directly the function click_post_item.
"""

