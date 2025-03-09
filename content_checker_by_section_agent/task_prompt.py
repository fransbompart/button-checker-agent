SYSTEM_PROMPT = """You are evaluating content on SoyZen, a web platform focused on mental and spiritual health. The platform offers different types of content, including:  

- Blog Content: Articles containing only text. When opened, a blog should include:  
  - A cover image.  
  - The author's name.  
  - The publication date.  
  - A title that matches the preview.  

- Audio/Video Content: Multimedia content that can be either audio or video. When opened, it should display a player interface.  

Additionally, content has two access types:  
- Public Content: Opens directly.  
- Subscriber-Only Content: Displays a subscription dialog with messages like _"¡Prueba Gratis 5 días!"_ or _"Suscríbete"_.  

### How to Identify Content from the Preview  
Each content item in the slider is displayed as a rounded-square tile containing:  
- A title representing the content.  
- Sometimes, a category label in one of the corners.  
- For multimedia content:  
  - A play button icon.  
  - A clock icon showing the duration.  
- For blogs:  
  - No play button or duration indicator.  
- For subscriber-only content:  
  - A padlock icon in one of the corners.  
  - If there is no padlock, the content is public.  

"""

TASK_PROMPT = """### Objective  
Verify that each content item in the pageSectionName has a preview that correctly matches its actual content when opened.  

### Steps
1. Find the section with the name pageSectionName.
2. Identify all content items in pageSectionName section.  
3. For each content item:  
   - **Extract** the preview details:  
     - `content_preview_title`  
     - `content_preview_type` (Blog, Audio/Video)  
     - `content_preview_category` (if available)  
     - `content_preview_access_type` (Public or Subscriber-Only)
     - `content_preview_duration` (if available)
     - `content_url` 
   - Click to open the content in a new tab. Here can be two scenarios base on content access type:  
    - Check if the opened content matches its preview, ensuring:  
      - The title remains the same (`content_title`).  
      - The type remains the same (`content_type`).  
      - If it’s a blog, it contains the expected elements (cover image, author, date, text).  
      - If it’s an audio/video, the player interface appears.  
    - If the content is subscriber-only, confirm that a subscription dialog appears, leave `content_title` and `content_type` empty in the output.  
4. Navigation after checking the content:  
   - If the content opened successfully, switch to tab 1 and continue with the next item.  
   - If a subscription dialog appeared, close it and return to the slider.  

---

### Important

- **Don't scroll out of the pageSectionName**, when you end checking all the content items, finish.
- If you encounter any issues or errors, save all_matches of the content item as False.
"""

IDENTIFY_CONTENT_TASK = """
### Objective  
Identify and describe the content items in the pageSectionName section.

### Instructions
1. Find the section with the name pageSectionName.
2. Identify all content items in pageSectionName section.  
3. For each content item:  
   - **Extract** the preview details:  
     - `content_preview_title`  
     - `content_preview_category` (if available)  
     - `content_url` 
4. Finish when you have checked all the content items.
"""

EVALUATE_CONTENT_TASK = """
1. Find the section with the name pageSectionName.
2. Find the content item with the title content_preview_title.
3. Click to open the content in a new tab.
4. Check if the opened content matches its preview, ensuring:  
   - The title remains the same (`content_title`).  
   - The type remains the same (`content_type`).  
   - If it’s a blog, it contains the expected elements (cover image, author, date, text).  
   - If it’s an audio/video, the player interface appears.
5. If everything match, end the task with True, else, end with False and indicate the differences.
"""