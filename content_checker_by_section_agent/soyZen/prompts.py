IDENTIFY_CONTENT_TASK_SOY_ZEN="""###Objective
Identify and describe all the content items in the "pageSectionName" section of the SoyZen platform.

### Instructions
1. If a dialog about Calendario Lunar appears, click on the x before continue.
2. Find the section "pageSectionName" in the page. 
3. Extract the next details for each content item that are **ON the "pageSectionName" section**:previewDetails
4. Analyze the information extracted and return a response following the output format. 

"""

EVALUATE_CONTENT_TASK = """###Objective
Evaluate the content item in the "pageSectionName" section of the SoyZen platform.

### Instructions
1. Click on the post item with title "content_preview_title" using the custom function click_post_item, the number of the post is previewNumber.
2. Then, there is a condition for the next steps:
  - If you are not in home, you are in the post page:
    - **Extract** the whole page.
    - Indicate if it is a "blog" or an "audio/video", and provide a clear description of it. If certain details are unavailable, the response should still include as much relevant information as possible. For example:
      - This is a blog post. The topic appears to be about renewable energy, but the author and publication date are not available. The content discusses the benefits of solar power and wind energy.
      - This is a video file. The title and creator are not specified, but the video appears to be a tutorial on graphic design basics. The duration is not provided neither. 
  - Else, if a dialog with message "¡Prueba Gratis 5 días!" (app-modal-subscription tag in HTML) appers:
    - Set dialog_opened as True, as page description return "Dialog appeared with message !Prueba Gratis 5 días!" and end the task successfully.
---
**Important:**
- First, if a dialog about Calendario Lunar appears, close it on the x before continue.
- If you don't see the post item, DON'T SCROLL, use directly the function click_post_item.
"""



SYSTEM_PROMPT = """You are evaluating content on SoyZen, a web platform focused on mental and spiritual health. The platform offers different types of posts, including:  

- Blog Post: Articles containing only text. When opened, a blog should include:  
  - A cover image.  
  - The author's name.  
  - The publication date.  
  - A title that matches the preview.  

- Audio/Video Post: Multimedia content that can be either audio or video. When opened, it should display a player interface.  

Additionally, posts has two access types:  
- Public Post: Opens directly.  
- Subscriber-Only Post: Displays a subscription dialog with messages like _"¡Prueba Gratis 5 días!"_ or _"Suscríbete"_.  

### How to Identify Posts from the Preview  
Each post item in the sections is displayed as a rounded-square tile containing:  
- A title representing the post.   
- For multimedia posts:  
  - A Play Button Icon.  
  - A Clock Icon showing the duration.  
- For blogs:  
  - No play button or duration indicator.  
- When is a subscriber-only post preview, you will see a Padlock Icon in one of the corners.  

### Important

- **Take your time to ensure accuracy, it is pretty important to difference Public or Subscriber-Only posts.**

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
     - `content_preview_categories` (if available)  
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



