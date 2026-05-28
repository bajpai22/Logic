import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Common stopwords to filter out from keyword suggestions
STOPWORDS = {
    "the", "and", "for", "with", "in", "a", "to", "of", "is", "are", "be",
    "as", "an", "at", "by", "we", "or", "on", "you", "it", "this", "that",
    "will", "have", "has", "had", "from", "not", "but", "all", "can", "our",
    "your", "their", "they", "who", "what", "how", "when", "where", "which",
    "its", "also", "more", "was", "were", "do", "does", "did", "would",
    "should", "could", "may", "might", "must", "any", "than", "into", "so",
    "up", "out", "about", "been", "both", "such", "if", "each", "these",
    "able", "within", "across", "using", "strong", "good", "well", "new",
    "high", "large", "great", "work", "works", "working", "role", "team",
    "skills", "skill", "experience", "experienced", "years", "year", "time",
    "knowledge", "understanding", "including", "plus", "bonus", "etc",
    "other", "including", "ability", "us"
}

# Tech-aware important terms (always keep these even if short)
ALWAYS_KEEP = {
    "ml", "ai", "dl", "cv", "nlp", "api", "sql", "aws", "gcp", "git",
    "ci", "cd", "oop", "llm", "etl", "bi"
}


def clean_text(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_match_score(resume_text: str, job_text: str) -> float:
    """
    Compute TF-IDF cosine similarity between resume and job description.
    Returns a score from 0 to 100.
    """
    cleaned = [clean_text(resume_text), clean_text(job_text)]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform(cleaned)
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score) * 100, 1)
    except Exception:
        return 0.0


def get_missing_keywords(resume_text: str, job_text: str, top_n: int = 20) -> list[str]:
    """
    Extract important keywords from the job description that are
    missing from the resume.
    """
    resume_words = set(clean_text(resume_text).split())
    job_words = set(clean_text(job_text).split())

    missing = []
    for word in job_words:
        if word in resume_words:
            continue
        if word in STOPWORDS:
            continue
        if word in ALWAYS_KEEP:
            missing.append(word)
            continue
        if len(word) <= 2:
            continue
        if word.isdigit():
            continue
        missing.append(word)

    # Sort alphabetically for consistent display
    missing.sort()
    return missing[:top_n]


def get_matching_keywords(resume_text: str, job_text: str, top_n: int = 15) -> list[str]:
    """
    Extract important keywords that appear in BOTH the resume and JD.
    """
    resume_words = set(clean_text(resume_text).split())
    job_words = set(clean_text(job_text).split())

    matching = []
    for word in job_words & resume_words:
        if word in STOPWORDS:
            continue
        if word in ALWAYS_KEEP:
            matching.append(word)
            continue
        if len(word) <= 3:
            continue
        if word.isdigit():
            continue
        matching.append(word)

    matching.sort()
    return matching[:top_n]


def get_score_label(score: float) -> tuple[str, str]:
    """Return a (label, colour_name) tuple based on score."""
    if score >= 70:
        return "Excellent match", "success"
    elif score >= 50:
        return "Good match", "info"
    elif score >= 30:
        return "Moderate match", "warning"
    else:
        return "Low match", "error"


def get_improvement_tips(score: float, missing_keywords: list[str]) -> list[str]:
    """Generate actionable improvement tips based on score and missing keywords."""
    tips = []

    if score < 40:
        tips.append("Your resume needs significant tailoring for this role.")
        tips.append("Rewrite your summary section to mirror the job description language.")

    if score < 60:
        tips.append("Add a dedicated Skills section listing relevant technical tools.")
        tips.append("Quantify achievements with numbers (e.g. 'Improved load time by 30%').")

    if missing_keywords:
        sample = ", ".join(missing_keywords[:5])
        tips.append(f"Weave in missing keywords naturally — e.g. {sample}.")

    tips.append("Mirror the exact job title in your resume headline if it fits your experience.")
    tips.append("Use bullet points starting with strong action verbs (Built, Designed, Optimised).")

    return tips