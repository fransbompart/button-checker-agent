EVALUATE_CONTENT_TASK = """### Instructions:
1. Find the section with the name "pageSectionName".
2. Find the content item with the title "contentPreviewTitle" that **match exactly**. If you have to scroll because the content item is not in the visible area, do it **SLOWLY**.
3. Click on the content that has the title "contentPreviewTitle", use the custom function click_post_item.
4. If the content is Subscriber-only, a subscription dialog will appear. In this case, close the dialog and finish.
5. If the content is Public, wait for the page of the content to load.
6. Check if the the content article matches with the details provided, also if there is any orthographic error.

---

### Important:
- Don't use the search bar to find the content, if you are not able to click on the item, end the task

---
"""