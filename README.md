
# Jira Form Builder

A tool to visually create Jira form configurations — including Issue Types, Custom Fields, Screens, and Screen Schemes — and fully automate their creation inside Jira Server/Data Center using a Groovy script with Scriptrunner.

- 🖥️ Built with Python + Streamlit (no frontend development needed)
- ⚙️ Generates YAML/JSON form specifications
- 🚀 Includes a Groovy script to automate importing configurations into Jira (fields, screens, issue types)
- 🔥 No manual Jira admin clicks
- 🆓 Free for personal use, non-profit, or internal non-commercial projects

---

## 🔥 Features

- Create Jira issue forms visually with a simple UI
- Define:
  - Issue Types
  - Custom Fields (text, textarea, select, checkbox, radio, date, number, user picker, project picker)
  - Screens and Screen Schemes
- Export as **YAML** or **JSON**
- Fully automate Jira configuration with an included **Groovy script for Scriptrunner**
- No Docker, no frontend coding, runs locally

---

## 📦 Tech Stack

| Layer | Stack |
|-------|-------|
| UI    | Python + Streamlit |
| Data  | YAML / JSON |
| Backend (Jira) | Groovy + Scriptrunner |
| Runtime | Python 3.8+ |

---

## 🚀 Installation

### Python App

```bash
# Clone the repository
git clone https://github.com/your-repo/jira-form-builder.git
cd jira-form-builder

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Groovy Script

- Place the YAML file in Jira's server directory (e.g., `/var/atlassian/application-data/jira/import/`).
- Open **Scriptrunner → Script Console** in Jira.
- Paste the Groovy script.
- Adjust the YAML file path and project key.
- Run — the script will create issue types, screens, custom fields, and apply them.

---

## 🛠️ Project Structure

```
jira-form-builder/
├── app.py
├── form_logic/
│   ├── __init__.py
│   ├── parser.py
│   ├── validator.py
│   └── schema.py
├── forms/                   # YAML/JSON files
│   └── example-form.yaml
├── scriptrunner/            # Groovy script
│   └── form_importer.groovy
├── requirements.txt
├── .pylintrc
└── README.md
```

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

## ⚠️ License

**Non-Commercial License**

This software is free for:
- Personal use
- Educational use
- Non-profit organizations
- Internal use in companies **only if not monetized**

**It is NOT free if:**
- Your company uses this tool as part of a commercial offering
- You offer this tool as a paid service or product
- You are generating revenue from services based on this tool

→ For commercial licenses, please contact the author.

---

## 📜 LICENSE

```text
Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), for 
personal, educational, or non-profit use, subject to the following conditions:

Commercial use is prohibited without explicit written permission. Commercial use 
includes offering the software or derivatives thereof as part of a product, 
service, consulting, SaaS, or any revenue-generating activity.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

## 🤝 Contact

For commercial licensing, issues, or contributions:  
**LinkedIn:** [https://www.linkedin.com/in/raniro](https://www.linkedin.com/in/raniro)  

---

## ⭐️ Contributions

- Issues, bug reports, and feature requests are welcome.
- Pull requests are welcome for non-commercial improvements.
