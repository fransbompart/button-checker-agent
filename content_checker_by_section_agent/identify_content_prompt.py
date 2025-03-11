# VidaFit
# IDENTIFY_CONTENT_TASK = """Identify and describe the content items in the "pageSectionName" section.

# ### Instructions
# 1. Find the section with the name "pageSectionName". If needed, scroll to locate it, but do it every 10 high, **SLOWLY**.
# 2. Identify **all content items** in "pageSectionName" section.
# 3. Extract the next details for each content item:previewDetails
# 4. Finish when you have checked **all the content items in the section**.
# """

# SoyZen
IDENTIFY_CONTENT_TASK="""### Instructions
1. Find the section "pageSectionName" in the page. 
2. Extract the next details for each content item that are **ON the "pageSectionName" section**:previewDetails 

---

**Important:**
- First, if a dialog about Calendario Lunar appears, close it on the x before continue.
"""