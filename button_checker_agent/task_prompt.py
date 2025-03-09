STEP = """Identify all actionable elements (such as buttons, links, or interactive components) 
and assign to each one a meaningful name based on what it represents
(e.g., a profile icon should be labeled as "Profile Button").

**Important:**
- Don't scroll, this task only have one step, just identify the elements that are visible on the current screen, then finish.
"""

STEP_1 = """**Instructions:**  
1. Identify all actionable elements on the current screen, such as icons, buttons, links, or interactive components.  
2. Assign a meaningful name to each element based on what it represents, take your time yo analize this to be significant.

**Important:**  
- If a dialog appears, close it with the custom function close_dialog, then you can start with the instructions of the task.
- Do not scroll, just identify the elements that are visible on the current screen, then finish.

"""

STEP_2="""**Objective:**   
Click on the buttons listed below and analyze their interactions.  

---  

**Instructions:**  
1. Locate each button on the screen based on the names in the provided list.  
2. Click on the button.  
3. Observe the result of the action carefully. Take your time to analyze the UI changes. Wait for at least 5 seconds before proceeding to ensure all changes are fully loaded.  
4. Describe the result of the interaction in a significant way.
5. Determine if the result aligns with the button’s expected function:  
   - If the action matches the button’s name, set result_success = True.  
   - If the action does not match the button’s name, set result_success = False. 
6. If clicking an element generates one of these actions:
   - Navigates to a new page: Return to the previous one, use the custom function return_to_previous_page.
   - Opens a dialog: Close it, without scrolling.
7. Repeat the process for all remaining buttons in the list.  
8. Conclude the task once all buttons have been tested.  

---

**Important:**  
- Do not make suggestions or assumptions in the description of the action result.  
- **If clicking a button navigates to a different page, always return to the original page using the custom function return_to_previous_page** before continuing.    
- Don't scroll, just evaluate the elements that are visible on the current screen, then finish.
- If a random dialog appears, close it, but don't scroll.
- **Do not click on any element that is not listed below.**
---  

**List of Buttons:**  
"""

