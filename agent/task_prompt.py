STEP = """**Instructions:**  
1. Identify all actionable elements on the current screen, such as buttons, links, or interactive components.  
2. Assign a meaningful name to each element based on what it represents. For example:  
   - A profile icon should be labeled as "Profile Button".  
   - A "Learn More" link should be labeled as "Learn More Link".  
3. List all identified elements with their assigned names.  

**Important:**  
- Do not scroll. This task is limited to the current screen.
"""

STEP_1 = """Identify all actionable elements (such as buttons, links, or interactive components) 
and assign to each one a meaningful name based on what it represents
(e.g., a profile icon should be labeled as "Profile Button").

**Important:**
- Don't scroll, this task only have one step, just identify the elements that are visible on the current screen, then finish.
"""

STEP_2="""**Objective:**   
Click on the buttons listed below and analyze their interactions.  

---  

**Instructions:**  
1. Locate each button on the screen based on the names in the provided list.  
2. Click on the button.  
3. Observe the result of the action carefully. Take your time to analyze the UI changes. Wait for at least 5 seconds before proceeding to ensure all changes are fully loaded.  
4. Summarize the result in a short description. For example:  
   - Example 1: "A pop-up opened showing the user profile options."  
   - Example 2: "The page navigated to a new screen displaying account settings."  
   - Example 3: "A dropdown menu appeared with additional options."  
5. Determine if the result aligns with the button’s expected function:  
   - If the action matches the button’s name, set result_success = True.  
   - If the action does not match the button’s name, set result_success = False.  
6. **If the button leads to a new page, use the custom function return_to_previous_page** to return to the original page before proceeding with the next button.  
7. Repeat the process for all remaining buttons in the list.  
8. Conclude the task once all buttons have been tested.  

---

**Important:**  
- Do not make suggestions or assumptions. Simply describe the observed result and determine if it aligns with the button’s expected function.  
- If clicking a button navigates to a different page, always return to the original page using the custom function return_to_previous_page before continuing.    

---  

**List of Buttons:**  
"""

