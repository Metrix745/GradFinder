import csv

form_values = {
    "name": "",
    "email": "",
    "major": "",
    "research-interest-1": "",
    "research-interest-2": "",
    "research-interest-3": ""
}

display(f"Form values are: {form_values}", target="form-values")

# Create all the event handlers

def submit_handler(event=None):
    if event:
        event.preventDefault()
        print("Form submitted!")
        display(f"Form values are: {form_values}", target="form-values")

def reset_handler(event=None):
    if event:
        form_values.update({
            "name": "",
            "email": "",
            "major": "",
            "research-interest-1": "",
            "research-interest-2": "",
            "research-interest-3": ""
        })
        display(f"Form values are: {form_values}", target="form-values")

def name_input_handler(event=None):
    if event:
        form_values["name"] = event.target.value

def email_input_handler(event=None):
    if event:
        form_values["email"] = event.target.value

def major_input_handler(event=None):
    if event:
        form_values["major"] = event.target.value

def research_interest_1_input_handler(event=None):
    if event:
        form_values["research-interest-1"] = event.target.value

def research_interest_2_input_handler(event=None):
    if event:
        form_values["research-interest-2"] = event.target.value

def research_interest_3_input_handler(event=None):
    if event:
        form_values["research-interest-3"] = event.target.value

# Now map the event handlers to the elements

Element("name").element.oninput = name_input_handler
Element("email").element.oninput = email_input_handler
Element("major").element.oninput = major_input_handler
Element("research-interest-1").element.oninput = research_interest_1_input_handler
Element("research-interest-2").element.oninput = research_interest_2_input_handler
Element("research-interest-3").element.oninput = research_interest_3_input_handler
Element("form").element.onsubmit = submit_handler
Element("form").element.onreset = reset_handler