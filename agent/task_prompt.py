TASK = """

### Prompt for Page Buttons Checker Agent 

**Objective:**
In the current view of the page, identify all actionable elements (such as buttons, links, or interactive components) and systematically test if they function as expected. For each element:

- Click it and observe the resulting change on the page.
- Provide a brief description of what happened after the interaction.
- Determine if the observed result aligns with the expected behavior based on the element’s label or appearance.

**Important:**
- If clicking an element navigates to a new page, return to the previous one.
- Ensure all interactions are performed without missing any identified elements.
- Maintain a structured record of interactions, including the element name, observed result, and success status (true/false).
- Don't scroll, just identify the elements that are visible on the current screen, then finish.

---

### Step 1: Identify Actionable Elements

- Scan the webpage and identify all clickable elements.
- Assign a meaningful name to each element based on what it represents (e.g., a profile icon should be labeled as "Profile Button").

---

### Step 2: Click Each Button and Analyze the Interaction

- Click on each identified button.
- Observe the result of the action and summarize it in a short description.
- Determine if the result aligns with the button's expected function:
 - If the action matches the button’s name, set result_success = True.
 - If the action does not match the button’s name, set result_success = False.
 - If the button leads to a new page, return to the previous page and continue checking the remaining buttons.
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
3. Observe the result of the action, take your time, then summarize it in a short description.  
4. Determine if the result aligns with the button’s expected function:  
   - If the action matches the button’s name, set **result_success = True**.  
   - If the action does not match the button’s name, set **result_success = False**.  
5. If the button leads to a new page, **return to the original page using the custom function return_to_previous_page** before proceeding with the next button.  
6. Repeat the process for all remaining buttons in the list.  
7. Conclude the task once all buttons have been tested.  

---  

**Important:**   
- If clicking a button navigates to a different page, **always return to the original page using the custom function return_to_previous_page** before continuing.    
---  

**List of Buttons:**  
"""

