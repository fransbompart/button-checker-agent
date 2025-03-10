EVALUATE_CONTENT_TASK = """### Instructions:
1. Find the section with the name "pageSectionName".
2. Find the content item with the title "contentPreviewTitle" that **match exactly**. If you have to scroll because the content item is not in the visible area, do it **SLOWLY**.
3. Click on the content that has the title "contentPreviewTitle", use the custom function click_content_item, use the Page URL as parameter for the function.
4. Wait for the page of the content to load.
5. Check if the the content article matches with the details provided, also if there is any orthographic error.

---

### Important:
- Don't use the search bar to find the content, if you are not able to click on the item, end the task

---
"""


