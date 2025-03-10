IDENTIFY_CONTENT_TASK = """Identify and describe the content items in the "pageSectionName" section.

### Instructions
1. Find the section with the name "pageSectionName". If needed, scroll to locate it, but do it every 10 high, **SLOWLY**.
2. Identify **all content items** in "pageSectionName" section. Only the ones that belongs to the "pageSectionName" section.
3. Keeping the horizontal order, for each content item:  
  - Extract the next details:previewDetails
4. Finish when you have checked all the content items in the section.

### Important
- **Don't return posts information not accurate** like the next example, it its better to left Unsatisfied the task:
  "- Example Post Details:
    - Title: title2
    - Categories: category2"

"""