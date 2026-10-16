import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_ALIASES = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "TypeScript": ["typescript"],
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb"],
    "SQLite": ["sqlite"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Streamlit": ["streamlit"],
    "React": ["react"],
    "Node.js": ["node.js", "nodejs"],
    "REST APIs": ["rest api", "rest apis", "restful api", "restful apis"],
    "HTML": ["html"],
    "CSS": ["css"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis"],
    "Data Visualization": ["data visualization"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Communication": ["communication", "communication skills"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Data Structures": ["data structures"],
    "Algorithms": ["algorithms", "algorithm"],
    "Object-Oriented Programming (OOP)": [
        "object oriented programming",
        "object-oriented programming",
        "oop",
    ],
    "Linux": ["linux"],
    "Excel": ["excel"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Agile": ["agile"],
    "Testing": ["testing", "software testing"],
    "Unit Testing": ["unit testing"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous delivery"],
    "Kubernetes": ["kubernetes"],
    "JWT": ["jwt", "json web token", "json web tokens"],
    "HTTP": ["http", "https"],
    "CRUD": ["crud", "create read update delete"],
}


def normalize(text: str) -> str:
    """Normalize punctuation and whitespace for phrase comparison."""
    text = text.lower().replace("-", " ")
    text = re.sub(r"[^a-z0-9+#./ ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def contains_phrase(text: str, phrase: str) -> bool:
    """Check a whole phrase rather than a partial word."""
    normalized_text = f" {normalize(text)} "
    normalized_phrase = f" {normalize(phrase)} "
    return normalized_phrase in normalized_text


def find_skills(text: str) -> list[str]:
    """Return each recognized skill once, using canonical names."""
    found = []

    for canonical_name, aliases in SKILL_ALIASES.items():
        if any(contains_phrase(text, alias) for alias in aliases):
            found.append(canonical_name)

    return found


def extract_keywords(job_description: str, limit: int = 25) -> list[str]:
    """Extract candidate keywords from the job description."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=100,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z+#.]{1,}\b",
    )

    try:
        matrix = vectorizer.fit_transform([job_description])
        terms = vectorizer.get_feature_names_out()
        weights = matrix.toarray()[0]
        ranked = sorted(
            zip(terms, weights),
            key=lambda item: (-item[1], item[0]),
        )
        return [term for term, _ in ranked[:limit]]
    except ValueError:
        return []


def analyze_match(resume_text: str, job_description: str) -> dict:
    """Compare resume text with a job description."""
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is required.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description is required.")

    resume = normalize(resume_text)
    job = normalize(job_description)

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=12000,
        )
        matrix = vectorizer.fit_transform([resume, job])
        score = float(
            cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        )
    except ValueError:
        score = 0.0

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)

    matched_skills = [
        skill for skill in job_skills if skill in resume_skills
    ]
    missing_skills = [
        skill for skill in job_skills if skill not in resume_skills
    ]

    keywords = extract_keywords(job_description)
    matched_keywords = [
        word for word in keywords if contains_phrase(resume_text, word)
    ]
    missing_keywords = [
        word for word in keywords if word not in matched_keywords
    ]

    return {
        "score": round(score * 100, 1),
        "job_skills": job_skills,
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }
