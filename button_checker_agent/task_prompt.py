STEP = """Identify all actionable elements (such as buttons, links, or interactive components) 
and assign to each one a meaningful name based on what it represents
(e.g., a profile icon should be labeled as "Profile Button").

**Important:**
- If a dialog appears, close it on the x icon, then you can start with the instruction of the task.
- Don't scroll, this task only have one step, just identify the elements that are visible on the current screen, then finish.
"""

STEP_1 = """**Instructions:**  
1. Identify all actionable elements on the current screen, such as icons, buttons, links, or interactive components.  
2. Assign a meaningful name to each element based on what it represents, **take your time to analize** them to be significant.
3. For each actionable element, return the name as a list of strings (e.g., button_name: ['Log In Button', 'Profile Icon', ...]).

**Important:**  
- If a dialog appears, close it on the x icon, then you can continue with the instructions of the task.
- Do not scroll, just identify the elements that are visible on the current screen, then finish.
- Exclude Logo Button from the list of buttons.

"""

STEP_2="""**Objective:**   
Click on the buttons listed below and analyze their interactions.  

---  

**Instructions:**  
1. Locate each button on the screen based on the names in the provided list.  
2. Click on the button.  
3. Observe the result of the action carefully. Take your time to analyze the UI changes. Wait for at least 5 seconds before proceeding to ensure all changes are fully loaded.  
4. Describe the result of the interaction in a significant way (e.g., "Navigated to the profile page", "Opened a dialog for login", "Displayed an error message", "The home change it, content related with Fashion is displayed on screen").
5. Determine if the result aligns with the button’s expected function:  
   - If the action matches the button’s name, set result_success = True.  
   - If the action does not match the button’s name, set result_success = False. 
6. If clicking an element generates one of these actions:
   - Navigates to a new page: Return to the previous one, use the custom function return_to_previous_page.
   - Opens a dialog: Close it, without scrolling.
7. Repeat the process for all remaining buttons in the list.  
8. Conclude the task once all buttons have been tested.
9. Return the results as a list of dictionaries, where each dictionary contains:
   - button_name: str
   - button_action_result_description: str
   - button_action_result_success: bool  

---

**Important:**  
- Do not make suggestions or assumptions in the description of the action result.  
- **If clicking a button navigates to a different page, always return to initial one using the custom function return_to_previous_page** before continuing.    
- Don't scroll, just evaluate the elements that are visible on the current screen, then finish.
- If a dialog appears, close it on x icon, then you can continue with the instructions of the task.
- **Do not click on any element that is not listed below.**
---  

**List of Buttons:**  
"""

