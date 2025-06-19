
# Jira Form Builder

A tool to visually create Jira form configurations — including Issue Types, Custom Fields, Screens, and Screen Schemes — and fully automate their creation inside Jira Server/Data Center using a Groovy script with Scriptrunner.

- 🖥️ Built with Python + Streamlit (zero frontend coding)
- ⚙️ Generates YAML/JSON form specifications
- 🚀 Includes a Groovy script to automate importing configurations into Jira (fields, screens, issue types)
- 🔥 No manual Jira admin clicks
- 🆓 Free for personal use, non-profit, or internal non-commercial projects

---

## 🎯 Goal

Internal tool for your team to easily create, visualize, and test Jira ticket forms.

The Governance team receives the form definition (YAML/JSON) and applies it into Jira using the provided **Groovy script with Scriptrunner**, automating the process.

---

## ✅ Features

- Create Jira form configurations:
  - Issue Types
  - Custom Fields: Text, Textarea, Select, Checkbox, Radio buttons, Number, Date, User Picker, Project Picker
  - Screens and Screen Schemes
- Visual Preview of forms
- Input validation (duplicate fields, empty names)
- Export to YAML and JSON
- Import from existing YAML
- Works locally — no Docker, no frontend stack
- Automation of Jira configurations via Groovy + Scriptrunner
- Extensible: clean backend modules for CLI, APIs, future expansions

---

## 🚀 Tech Stack

| Layer    | Stack                                  |
|----------|-----------------------------------------|
| UI       | Python + Streamlit                     |
| Data     | YAML / JSON                             |
| Backend  | Groovy + Scriptrunner (Jira DC)         |
| Utilities| Python modules (`parser`, `utils`, etc.)|
| Runtime  | Python 3.8+                             |

---

## 🏗️ Project Structure

```
jira-form-builder/
├── app.py
├── form_logic/
│   ├── __init__.py
│   ├── parser.py
│   ├── validator.py
│   ├── schema.py
│   └── utils.py
├── forms/
│   └── example-form.yaml
├── scriptrunner/
│   └── form_importer.groovy
├── requirements.txt
├── .pylintrc
├── README.md
└── LICENSE
```

---

## 🚦 Usage Workflow

1. Run the Python app with Streamlit
2. Create the form → name, issue type, fields
3. Export as YAML
4. The Governance team runs the Groovy script in Jira
5. Script creates the Issue Type, Custom Fields, Screen, and Screen Scheme

---

## 📄 Example YAML

```yaml
form_name: Access Request
issue_type: Access Request
fields:
  - name: Full Name
    type: text
    required: true
  - name: Department
    type: select
    required: true
    options: [IT, HR, Finance]
  - name: Request Date
    type: date
    required: false
screen: Access Request Screen
```

---

## 🔐 License

**License Type:** **Non-Commercial Custom License**  
This is not a standard OSI license. It permits:  
- Personal use  
- Non-profit organizations  
- Educational use  
- Internal company use if not monetized  

**Commercial use is prohibited without explicit written consent from the author.**

---

## 📜 LICENSE Summary

```text
Copyright (c) 2025 Raniro Coelho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), for 
personal, educational, or non-profit use, subject to the following conditions:

Commercial use is prohibited without explicit written permission. Commercial use 
includes offering the software or derivatives thereof as part of a product, 
service, consulting, SaaS, or any revenue-generating activity.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

## 📫 Contact

- **Email:** ranirocoelho@gmail.com  
- **GitHub:** [https://github.com/Errec](https://github.com/Errec)  
- **LinkedIn:** [https://linkedin.com/in/raniro](https://linkedin.com/in/raniro)  

---

## ⭐ Contributions

- Issues, feature requests, and pull requests are welcome for non-commercial improvements.

---

## 🏆 Status

✅ Production ready.  
→ Clean code, modular architecture, extensible for CLI or API automation.
