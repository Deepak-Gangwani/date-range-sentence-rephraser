Here’s your README updated with **ready-to-test API endpoints** for both local and PythonAnywhere deployment:

```markdown
# Date Range & Sentence Rephraser API

## 📄 API Documentation
This project provides two main functionalities:

1. **Date Range Generator** – Generates a list of dates based on a natural language date range keyword.  
2. **Sentence Rephraser** – Returns multiple rephrased or grammatically corrected versions of a given sentence.

**Base URL:**  
```

https\://<yourusername>.pythonanywhere.com

```

---

## 1️⃣ Date Range Generator API
Generates a list of dates based on a given keyword (e.g., `till_yesterday`, `last_7_days`). Useful for analytics, reporting, and dynamic date-based filters.

**Endpoint:**  
```

GET /api/date-range

```

**Query Parameters:**
| Parameter | Type   | Required | Allowed Values |
|-----------|--------|----------|----------------|
| range     | string | Yes      | `till_yesterday`, `till_tomorrow`, `next_month`, `last_7_days`, `this_week` |

**Example Local Test:**
```

[http://127.0.0.1:5000/api/date-range?range=last\_7\_days](http://127.0.0.1:5000/api/date-range?range=last_7_days)

```

**Example PythonAnywhere Test:**
```

https\://<yourusername>.pythonanywhere.com/api/date-range?range=last\_7\_days

````

**Example Response:**
```json
{
  "range": "last_7_days",
  "dates": [
    "2025-08-03",
    "2025-08-04",
    "2025-08-05",
    "2025-08-06",
    "2025-08-07",
    "2025-08-08",
    "2025-08-09"
  ]
}
````

---

## 2️⃣ Sentence Rephraser API

Takes a single sentence and returns 5 rephrased or grammatically corrected versions using basic NLP techniques.

**Endpoint:**

```
POST /api/rephrase
```

**Request Body:**

```json
{
  "sentence": "This is a sample sentence."
}
```

**Example Local Test (using curl):**

```bash
curl -X POST http://127.0.0.1:5000/api/rephrase \
     -H "Content-Type: application/json" \
     -d '{"sentence": "This is a sample sentence."}'
```

**Example PythonAnywhere Test:**

```bash
curl -X POST https://<yourusername>.pythonanywhere.com/api/rephrase \
     -H "Content-Type: application/json" \
     -d '{"sentence": "This is a sample sentence."}'
```

**Example Response:**

```json
{
  "original": "This is a sample sentence.",
  "rephrased": [
    "This sentence is just an example.",
    "Here is a sample sentence.",
    "This is simply an example sentence.",
    "This is a demonstration sentence.",
    "This sentence serves as an example."
  ]
}
```

---

## 🔐 Authentication

Currently, **no authentication** is required — all endpoints are public.
In production, you can add **JWT** or **API key-based** authentication.

---

## 📡 Status Codes

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 200  | ✅ Success                              |
| 400  | ❌ Bad request (missing/invalid params) |
| 500  | ⚠️ Server error                        |

---

## 🚀 Deployment on PythonAnywhere

1. Upload all `.py` files and `requirements.txt` to your PythonAnywhere account.
2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Download required **NLTK** data:

   ```bash
   python -m nltk.downloader punkt
   python -m nltk.downloader punkt_tab
   python -m nltk.downloader averaged_perceptron_tagger
   python -m nltk.downloader averaged_perceptron_tagger_eng
   ```
5. Configure your **WSGI** file to point to `app.py`.
6. Reload your web app from the PythonAnywhere dashboard.
7. Test the endpoints using the examples above.

---

## 📦 Installation & Requirements

Before running locally, ensure **Python 3.8+** is installed.

**Install dependencies:**

```bash
pip install flask
pip install flask_sqlalchemy
pip install python-dateutil
pip install textblob
pip install language_tool_python
pip install nltk
```

**Download NLTK Data:**

```bash
python -m nltk.downloader punkt
python -m nltk.downloader punkt_tab
python -m nltk.downloader averaged_perceptron_tagger
python -m nltk.downloader averaged_perceptron_tagger_eng
```

---

## 🛠 Example Local Run

```bash
export FLASK_APP=app.py
flask run
```

Access API locally at:

```
http://127.0.0.1:5000
```

```

If you want, I can also **add a “Try it in Postman” collection link** so anyone can test your API instantly without setting up anything locally. That would make the README even more developer-friendly.
```
