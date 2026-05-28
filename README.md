# 📄 Resume Job Match Scorer

An ML-powered web app that scores how well your resume matches a job description — and tells you exactly what keywords to add to improve your chances.

**GitHub Repo → https://github.com/bajpai22/Logic**

---

## 🚀 What it does

* Computes a **match score (0–100%)** using TF-IDF vectorisation + cosine similarity
* Shows which **keywords already exist** in the resume
* Highlights **missing keywords** to improve ATS compatibility
* Gives **actionable improvement tips**
* Lets users **download a full match report**

---

## 🛠 Tech Stack

| Layer           | Tech         |
| --------------- | ------------ |
| Language        | Python 3.12  |
| ML              | Scikit-learn |
| Data Processing | Pandas       |
| UI              | Streamlit    |
| Deployment      | Render       |
| Version Control | Git + GitHub |

---

## 🧠 How the ML Works

1. Resume and Job Description text are cleaned and normalized
2. TF-IDF vectorization converts text into numerical vectors
3. Cosine similarity calculates semantic overlap
4. Match score is generated between 0–100%
5. Missing keywords are extracted after stopword filtering

---

## ▶️ Run Locally

```bash
# Clone the repository
git clone https://github.com/bajpai22/Logic.git

# Open project
cd Logic

# Create virtual environment
python -m venv venv

# Activate environment
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

Open:

```bash
http://localhost:8501
```

---

## 🌐 Deployment

Deployed using Render.

Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 📁 Project Structure

```bash
resume-match-scorer/
├── app.py
├── scorer.py
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Author

Built by Aryan Bajpai
Python Developer • ML Enthusiast • CSE Student

GitHub:
https://github.com/bajpai22

---

