import re

ROLE_KEYWORDS = [
    "engineer", "developer", "analyst", "manager", "designer",
    "scientist", "architect", "consultant", "director", "lead",
    "intern", "associate", "officer", "specialist", "administrator",
]

SKILL_KEYWORDS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go",
    "ruby", "php", "swift", "kotlin", "r",
    # Web / frontend
    "react", "angular", "vue", "html", "css", "node",
    # Data / ML
    "sql", "mysql", "postgresql", "mongodb", "pandas", "numpy",
    "tensorflow", "pytorch", "scikit", "keras",
    # Cloud / DevOps
    "aws", "azure", "gcp", "cloud", "docker", "kubernetes",
    "jenkins", "terraform", "git",
    # BI / reporting
    "power bi", "tableau", "excel", "spark",
    # Soft / management
    "jira", "agile", "scrum",
]


def extract_email(text: str) -> str:
    match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    match = re.search(
        r"(\+?\d{1,3}[\s\-.]?)?(\(?\d{3}\)?[\s\-.]?)(\d{3}[\s\-.]?\d{4})",
        text
    )
    return match.group(0).strip() if match else ""


def extract_name(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Skip lines with special characters or numbers
        if re.search(r"[^a-zA-Z\s]", line):
            continue
        words = line.split()
        if 2 <= len(words) <= 5:
            # Accept ALLCAPS or TitleCase lines
            if line.isupper() or all(w.istitle() for w in words):
                return line.title()
    return ""


def extract_role(text: str) -> str:
    """
    Return the first line that contains a recognised role keyword.
    Falls back to the keyword itself if no clean line is found.
    """
    lines = text.splitlines()
    for line in lines:
        lower = line.lower()
        for kw in ROLE_KEYWORDS:
            if kw in lower:
                # Return a cleaned version — strip digits and excess whitespace
                clean = re.sub(r"[^a-zA-Z\s/]", "", line).strip()
                if clean:
                    return clean.title()
    return ""


def extract_experience(text: str) -> str:
    match = re.search(
        r"(\d+)\s*\+?\s*(?:years?|yrs?)(?:\s+of\s+experience)?",
        text, re.IGNORECASE
    )
    return match.group(1) if match else ""


def extract_skills(text: str) -> str:
    lower_text = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if skill in lower_text and skill.title() not in found:
            found.append(skill.title())
    return ", ".join(found)


def parse_resume(text: str) -> dict:
    return {
        "Name":               extract_name(text),
        "Email":              extract_email(text),
        "Phone":              extract_phone(text),
        "Role":               extract_role(text),
        "Experience (Years)": extract_experience(text),
        "Skills":             extract_skills(text),
    }
