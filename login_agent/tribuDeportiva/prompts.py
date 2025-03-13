TRIBU_DEPORTIVA_EMAIL_LOGIN_TASK_PROMPT = """### Objective
Log in to the Tribu Deportiva app with the provided credentials, verify if the login was successful.

### Instructions

1. Write email_value in the email text field.
2. Write password_value in the password text field.
3. Click on the "Iniciar Sesión" button.
4. Verify that the login was successful by checking if the app redirects to the home page.
5. Click on the Profile Button and verify if the email email_value appears on the pop-up, if so, the login was successful.
"""

# Log in in the current app with the provided email and password.
# Then verify if the login was successful if the app redirects to the home page, you can click on the Profile Button too and check if the provided email appears on the pop-up.


TRIBU_DEPORTIVA_OPERATOR_LOGIN_TASK_PROMPT = """### Objective
Log in to the Tribu Deportiva app with the provided credentials and telephone operator name, verify if the login was successful.

### Instructions

1. **Click** on the button that has a **operator_name Logo Image**.
2. Write `telephone_number` in the telephone number text field.
3. Click on the selector (is an mat-form-field element) and select `telephone_code` value.
4. Close the selector, if not, you will not be able to continue.
5. Click on the "Iniciar Sesión" button.
6. Verify that the login was successful by checking if the app redirects to the home page.
7. Click on the Profile Button.
8. Verify if the value `username@tribudeportivaguest.com` appears on the profile pop-up displayed (is an mat-mdc-menu-content), if so, the login was successful.

### Important

- Don't click on TribuDeportiva Logo Image or any other button that is not specified in the instructions.
- Don't navigate to any other page that is not specified in the instructions.
"""
