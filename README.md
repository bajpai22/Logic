# 📄 Resume Job Match Scorer

An ML-powered web app that scores how well your resume matches a job description — and tells you exactly what keywords to add to improve your chances.

**Live demo → [your-app.onrender.com](https://your-app.onrender.com)**

---

## What it does

- Computes a **match score (0–100%)** using TF-IDF vectorisation + cosine similarity
- Shows which **keywords you already have** from the job description
- Highlights **missing keywords** you should add to your resume
- Gives **actionable improvement tips** based on your score
- Lets you **download a full match report** as a text file

---

## Tech stack

| Layer | Tech |
|---|---|
| Language | Python 3.11+ |
| ML | Scikit-learn (TF-IDF, cosine similarity) |
| Data | Pandas |
| UI | Streamlit |
| Deployment | Render |
| Version control | Git + GitHub |

---

## How the ML works

1. Both texts (resume + JD) are cleaned and lowercased
2. A `TfidfVectorizer` converts them into numerical vectors
3. `cosine_similarity` measures the angle between those vectors
4. Score of 1.0 = perfect match, 0.0 = no overlap
5. Missing keywords are extracted by comparing word sets after filtering stopwords

---

## Run locally

```bash
# Clone the repo
git clone https://github.com/yourusername/resume-match-scorer.git
cd resume-match-scorer

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deploy on Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set the start command:

```
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

5. Done — Render will build and deploy automatically.

---

## Project structure

```
resume-match-scorer/
├── app.py              # Streamlit UI
├── scorer.py           # ML scoring logic
├── requirements.txt    # Dependencies
└── README.md
```

---

## Author

Built by [Your Name](https://linkedin.com/in/yourprofile) · CSE Graduate · Python & ML enthusiast

---

## License

MIT